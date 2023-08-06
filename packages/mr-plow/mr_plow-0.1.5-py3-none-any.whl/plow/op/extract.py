import abc
import gzip
import sys

from botocore.exceptions import ClientError as BotoClientError
import requests

from ..config import Config
from .base import get_config, inject_config


class Extractor:
    """Class representing a spec for fetching data and storing it to S3.

    This is an abstract class. Implementing for a given data source means
    overriding the methods marked as abstract:

        * get_data() to actually retrieve the data;
        * encode_text() to convert the return value of get_data() to binary
          data for S3; and
        * postprocess_response() to inform the caller about pagination and
          follow-up.

    Many implementors will also override preprocess_args().

    Typical you can implement by subclassing and implementing the given values,
    but it is also permitted to just instantiate an Extractor and set the
    attributes directly to the desired methods:

        >>> extractor = Extractor()
        >>> extractor.postprocess_response = my_postprocess_function

    This implementation is extremely abstract. If your data source is a REST
    resource, we recommend using RestExtractor as a more fully-featured base
    class instead.
    """

    use_snowflake = False

    @abc.abstractmethod
    def postprocess_response(self, request, get_data_args):
        """Analyze request to inform caller about pagination and follow-up.

        :param request: the object returned by get_data().
        :param get_data_args: the args passed to get_data().
        :return:
            None indicates no need for follow up.
            Otherwise, the result is a new value of get_data_args for the next
            invocation.
        """
        return None

    @abc.abstractmethod
    def encode_text(self, request):
        """compress text and perform other transformations.

        :param request: the object returned by get_data().
        :return: gzipped binary data to store in the body of the S3 document
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_data(self, **kwargs):
        """Executes the API call to fetch data.

        Return value of None indicates the request returned no data. You can
        in theory pass such a request through; returning None allows callers
        to avoid writing null data to S3.
        """
        raise NotImplementedError

    def preprocess_args(self, config, get_data_args):
        """applies any necessary defaults to config and get_data_args.

        Recommend overriding this instead of extract() when possible.

        Config should not be altered in-place since it may be re-used for
        other operations; instead create a new one.

        Default implementation sets plow_data_source and enforces
        plow_s3_bucket. This must be called if overridden.

        :param config: a Config object
        :param get_data_args: see extract()
        :return: (config, get_data_args)
        """
        if hasattr(self, 'source') and config.plow_data_source is None:
            config = Config(config, plow_data_source=self.source)
        return get_config(config, 'plow_s3_bucket'), get_data_args

    # sentinel return value, do not override.
    NO_DATA = object()

    def extract(self, *, config, s3_key, overwrite_s3=False, **get_data_args):
        """Executes the extraction

        * calls the api
        * stores to S3
        * analyzes for necessary follow up

        :param config:
            consulted for AWS credentials, bucket name, etc
        :param overwrite_s3:
            By default we check whether s3 document is already present,
            and fail if it is. Pass True to override this behavior and
            write to S3 unconditionally.
        :param get_data_args: kwargs to be passed to get_data()
        :return:
            * Extractor.NO_DATA; this indicates the last request returned no
                data (i.e. get_data() returned None), so no further requests
                need to be made and nothing was written to S3.
            * the return value from postprocess_response(): either None (no
                follow-up) or a new dict of get_data_args.
            """
        config, get_data_args = self.preprocess_args(config, get_data_args)
        s3_obj = config.make_s3_bucket().Object(s3_key)
        if not overwrite_s3:
            try:
                s3_obj.load()
                # we expect this to result in 404, indicating the object isn't
                # present. If it loads without incident, an error is thrown;
                # if the error is anything other than 404, it gets rethrown.
                raise ValueError('S3 key %r already in use in bucket %r'
                                 % (s3_key, config.plow_s3_bucket))
            except BotoClientError as e:
                if e.response['Error']['Code'] != '404':
                    raise
        r = self.get_data(**get_data_args)
        if r is None:
            return self.NO_DATA
        # TODO(jp, rb, dg): should we make these async? in case
        # postprocess_response also takes a long time to get.
        s3_obj.put(Body=self.encode_text(r))
        return self.postprocess_response(r, get_data_args)

    @inject_config()
    def iterative_extract(self, *, config, overwrite_s3=False, make_s3_key,
                          verbose=True, iterations=None,
                          filename_callback=None, **get_data_args):
        """Executes extract() and automatically follows up.

        This uses the return value of extract(), hency that of
        postprocess_response, to determine when and how to make a follow-up
        request.

        :param config, overwrite_s3: passed directly to extract().
        :param make_s3_key: a function taking the same kwargs as get_data
            and returning an s3 key to save the file to.
        :param verbose: if true, logging is printed to stderr.
        :param filename_callback: if provided, a callable object taking one
            positional parameter, the key of an S3 object. It is called after
            a key has been successfully written to.
        :param iterations: instructions on how many times to execute extract().
            None indicates indefinite attempts.
        """
        keys = set()
        while get_data_args is not None and (
           iterations is None or iterations > 0):
            new_key = make_s3_key(**get_data_args)
            if new_key in keys:
                if verbose:
                    print(f'args {get_data_args!r} generated duplicate key',
                          file=sys.stderr, flush=True)
                raise KeyError(f's3_key {new_key!r} generated twice')
            keys.add(new_key)

            if verbose:
                print(f'Fetching with parameters {get_data_args!r}',
                      file=sys.stderr, flush=True)
            get_data_args = self.extract(config=config, s3_key=new_key,
                                         overwrite_s3=overwrite_s3,
                                         **get_data_args)
            if get_data_args is self.NO_DATA:
                get_data_args = None
            else:
                if filename_callback is not None:
                    filename_callback(new_key)
            if iterations is not None:
                iterations -= 1
        return get_data_args


class RestExtractor(Extractor):
    """use GET requests to fetch and persist a REST resource.

    This implements the abstract methods of Extractor. Subclasses will need to
    override preprocess_args to specify how this implementation of get_data()
    is called (e.g. providing a `url` argument), and postprocess_response() to
    interpret the fetched data in an iterative-extraction context.
    """

    def get_data(self, *, url, params=None, **kwargs):
        """Implementation that wraps requests.get(), checks for 2xx status"""
        r = requests.get(url, params=params, **kwargs)
        r.raise_for_status()
        return r

    def encode_text(self, request):
        """Implementation that gzips binary data from a `requests.Response`."""
        return gzip.compress(request.content)

    def postprocess_response(self, request, get_data_args):
        """Implementation that unconditionally ends iterative extraction."""
        return None
