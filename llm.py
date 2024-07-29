#!/usr/bin/env python

import sys
import os
import re
from pprint import pprint
import json
import requests
from urllib.parse import urlencode, quote

import cohere

def get_bron_documents(query):
    params = {
        'query': query,
        'filter': 'source:openbesluitvorming,woo,poliflw',
        'excludes': '',
        'limit': 400
    }
    query_string = urlencode(params)
    url = 'https://api.bron.live/documents/search?' + query_string
    resp = requests.get(url)
    resp.raise_for_status()
    results = [
        {'title': i['_source']['title'], 'snippet': "\n".join(
            i['highlight'].get('description') or
            i['highlight'].get('title', ''))
        } for i in resp.json()['hits']['hits']
    ]
    return results

def main(argv):
    qst = "Hoe ziet het bestuurlijke apparaat van NL er uit?"
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    resp = co.chat(
      model="command-r-plus",
      message=qst,
      search_queries_only=True
    )
    pprint(dict(resp))
    all_documents = []
    for q in resp.search_queries:
        all_documents += get_bron_documents(q.text)
    pprint(all_documents)
    answer = co.chat(
      model="command-r-plus",
      message=qst,
      documents=all_documents)
    pprint(answer)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
