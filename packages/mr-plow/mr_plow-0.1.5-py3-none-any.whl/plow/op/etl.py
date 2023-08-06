from .base import inject_config


def data_table_op(func_name, op_name):
    @inject_config()
    def wrapped(*, table, config):
        if not hasattr(table, op_name):
            raise ValueError(f'must provide a table'
                             ' (invalid: {table!r})')

        op = getattr(table, op_name)
        return op(config.snowflake().cursor())
    wrapped.__name__ = func_name
    return wrapped


create_table = data_table_op('create_table', 'do_create')
transform = data_table_op('transform', 'do_transform')
load = data_table_op('load', 'do_merge')
