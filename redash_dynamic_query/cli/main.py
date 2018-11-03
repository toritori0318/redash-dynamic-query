# -*- coding: utf-8 -*-
import os
import sys
import csv
import json
import argparse
import urlparse
from redash_dynamic_query import RedashDynamicQuery

def rdq_main():
    args = args_proc()
    output(
        run(args),
        args['output_format'],
    )

def args_proc():
    parser = argparse.ArgumentParser(
            description='Process some integers.',
            add_help = True,
            )
    parser.add_argument(
        "-d", "--data-source-id", 
        metavar='N',
        type=int,
        help='an integer for the data_source_id'
    )
    parser.add_argument(
        "-a", "--max-age", 
        metavar='N',
        type=int,
        default=0,
        help='an integer for the max_age'
    )
    parser.add_argument(
        "-w", "--max-wait", 
        metavar='N',
        type=int,
        default=60,
        help='an integer for the max_wait(timeout)'
    )
    parser.add_argument(
        "-k", "--apikey", 
        help='required: redash apikey (can also be specified using REDASH_APIKEY environment variable)'
    )
    parser.add_argument(
        "-e", "--endpoint", 
        help='required: redash endpoint (can also be specified using REDASH_ENDPOINT environment variable)'
    )
    parser.add_argument(
        "-q", "--query-id", 
        required=True,
        help='required: redash query id'
    )
    parser.add_argument(
        "-p", "--query-parameters", 
        help='redash query parameters(eg. key1=val1,key2=val2)'
    )
    parser.add_argument(
        "-f", "--output-format", 
        default='csv',
        choices=['csv', 'tsv', 'json', 'redash_csv'],
        help='redash output format',
    )

    args = parser.parse_args()
    endpoint = args.endpoint or os.getenv('REDASH_ENDPOINT')
    apikey   = args.apikey or os.getenv('REDASH_APIKEY')
    if not endpoint:
        parser.print_help(sys.stderr)
        print ("rdq: error: argument -e/--endpoint (or REDASH_ENDPOINT) is required")
        exit(0)
    if not apikey:
        parser.print_help(sys.stderr)
        print ("rdq: error: argument -k/--apikey (or REDASH_APIKEY) is required")
        exit(0)

    query_parameters = args.query_parameters
    bind = {}
    if query_parameters:
        for row in query_parameters.split(","):
            key, value = row.split("=")
            if not key or not value:
                print """usage: main.py [-h] [-d n] [-a n] [-w n] [-k apikey] [-e endpoint] -q query_id
               [-p query_parameters] [-f output_format]
main.py: error: argument -p/--query-parameters is invalid. (eg. key1=val1,key2=val2)
"""
            bind[key] = value

    return {
        'endpoint': endpoint,
        'apikey': apikey,
        'data_source_id': args.data_source_id,
        'max_age': args.max_age,
        'max_wait': args.max_wait,
        'bind': bind,
        'query_id': args.query_id,
        'output_format': args.output_format,
    }

def output(result, output_format):
    if output_format == 'csv':
        output_csv(result)
    elif output_format == 'tsv':
        output_tsv(result)
    elif output_format == 'json':
        output_json(result)
    elif output_format == 'redash_csv':
        output_redash_csv(result)

def output_csv(result):
    columns = [x['name'] for x in result.get('query_result', {}).get('data', {}).get('columns', [])]
    print(",".join(['"%s"' % x for x in columns]))
    for row in result.get('query_result', {}).get('data', {}).get('rows', []):
        record = []
        for column in columns:
            record.append('"%s"' % (str(row.get(column)).replace('"', '""')))
        print(",".join(record).encode('utf-8'))
            
def output_tsv(result):
    columns = [x['name'] for x in result.get('query_result', {}).get('data', {}).get('columns', [])]
    print('\t'.join(columns))
    for row in result.get('query_result', {}).get('data', {}).get('rows', []):
        record = []
        for column in columns:
            record.append(row.get(column))
        print('\t'.join(record).encode('utf-8'))
            
def output_json(result):
    print(json.dumps(result.get('query_result', {}).get('data', {}).get('rows', [])))

def output_redash_csv(result):
    print(result.encode('utf-8'))

def run(args):
    as_csv = False
    if args.get('output_format') == 'redash_csv':
        as_csv = True

    redash = RedashDynamicQuery(
        endpoint=args.get('endpoint'),
        apikey=args.get('apikey'),
        data_source_id=args.get('data_source_id'),
        max_age=args.get('max_age'),
        max_wait=args.get('max_wait'),
    )
    query_id = args.get('query_id')
    bind = args.get('bind') or {}
    return redash.query(query_id, bind, as_csv=as_csv)
