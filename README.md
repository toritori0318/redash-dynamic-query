## Redash Dynamic Query

A tool for executing dynamic query of redash.

## Install

```
pip install git+https://github.com/toritori0318/redash-dynamic-query
```

## SYNOPSIS

```python
from redash_dynamic_query import RedashDynamicQuery

redash = RedashDynamicQuery(
    endpoint='http://myredash-host',
    apikey='secret_apikey',
    data_source_id=2,
    #max_age=0,  # option
    )

query_id = 111
bind = {
    "start_date":  '2017-01-01T00:00:00',
    "end_date":  '2017-01-01T23:59:59',
}
result = redash.query(query_id, bind)
print result['query_result']['data']
# {
#    'rows': [
#       {'mydata': 'xxx'}
#    ], 
#    'columns': [
#        {
#            'type': 'string', 
#            'friendly_name': 'mydata',
#            'name': 'mydata'
#        }
#    ]
#}

## LICENSE

MIT

```
