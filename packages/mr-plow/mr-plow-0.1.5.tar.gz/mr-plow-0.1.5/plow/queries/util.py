"""widely-used SQL snippets"""

now_ntz = "CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP)::TIMESTAMP_NTZ"
timestamp_decl = 'TIMESTAMP_NTZ NOT NULL DEFAULT ' + now_ntz
