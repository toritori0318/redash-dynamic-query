## Redash Dynamic Query

A tool for executing dynamic query of redash.

## Install

```
pip install redash-dynamic-query
```

## SYNOPSIS

```python
from redash_dynamic_query import RedashDynamicQuery

redash = RedashDynamicQuery(
    endpoint='http://myredash-host',
    apikey='secret_apikey',
    data_source_id=2, # Optional, default auto fill
    max_age=0,  # Optional, default value is 0
    max_wait=60,  # Optional, default value is 60
)

query_id = 111
bind = {
    'start_date': '2017-01-01T00:00:00',
    'end_date': '2017-01-01T23:59:59',
}
result = redash.query(query_id, bind)
print(result['query_result']['data'])
# {
#     'rows': [
#         {'mydata': 'xxx'}
#     ],
#     'columns': [
#         {
#             'type': 'string',
#             'friendly_name': 'mydata',
#             'name': 'mydata'
#         }
#     ]
# }
```

## CLI

```
% rdq
```

```
% rdq --help

usage: rdq [-h] [-d N] [-a N] [-w N] [-k APIKEY] [-e ENDPOINT] -q QUERY_ID
           [-p QUERY_PARAMETERS] [-f {csv,tsv,json,redash_csv}]

Process some integers.

optional arguments:
  -h, --help            show this help message and exit
  -d N, --data-source-id N
                        an integer for the data_source_id
  -a N, --max-age N     an integer for the max_age
  -w N, --max-wait N    an integer for the max_wait(timeout)
  -k APIKEY, --apikey APIKEY
                        required: redash apikey (can also be specified using
                        REDASH_APIKEY environment variable)
  -e ENDPOINT, --endpoint ENDPOINT
                        required: redash endpoint (can also be specified using
                        REDASH_ENDPOINT environment variable)
  -q QUERY_ID, --query-id QUERY_ID
                        required: redash query id
  -p QUERY_PARAMETERS, --query-parameters QUERY_PARAMETERS
                        redash query parameters(eg. key1=val1,key2=val2)
  -f {csv,tsv,json,redash_csv}, --output-format {csv,tsv,json,redash_csv}
                        redash output format
```

```
# example
% rdq -e http://myredash-host -k secret_apikey -q 111 -p start_date=2017-01-01T00:00:00,end_date=2017-01-01T23:59:59 -f csv
```

## LICENSE

MIT
