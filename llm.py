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
        #'filter': 'source:openbesluitvorming,woo,poliflw',
        'filter': 'source:openbesluitvorming,woo,poliflw',
        'excludes': '',
        'limit': 350,
        'default_operator': 'and'
    }
    query_string = urlencode(params)
    url = 'https://api.bron.live/documents/search?' + query_string
    resp = requests.get(url)
    resp.raise_for_status()

    results = []
    for i in resp.json()['hits']['hits']:
            results += [{
                'title': i['_source']['title'],
                'snippet': d
            } for d in i['highlight'].get('description', [])]
    # results = [
    #     {'title': i['_source']['title'], 'snippet': "\n".join(
    #         i['highlight'].get('description') or
    #         i['highlight'].get('title', ''))
    #     } for i in resp.json()['hits']['hits']
    # ]
    return results

def main(argv):
    #qst = "Hoe ziet het bestuurlijke apparaat van NL er uit?"
    #qst = "Hoe worden vluchtelingen opgevangen de respectievelijke gemeenten?"
    #qst = "Hoe gaan gemeenten om met windmolens en andere vormen van schone energie?"
    #qst = "hoe staat het met de parken in almelo?"
    qst = 'x'
    chat_history = []
    chat_history_incl = []
    while qst != 'exit':
        qst = input('Geef een vraag warop je het antwoord wil weten : ')
        if qst.strip() == '':
            qst = "Om vluchtelingen beter op te vangen worden er in gemeenten lokale voorzieningen getroffen om vluchtelingen te helpen. Welke voorzieningen voor vluchtelingen zijn er in almelo?"
        co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

        print(f"Vraag: {qst}")

        if qst.strip() == 'exit':
            continue

        resp = co.chat(
          model="command-r-plus",
          message=qst,
          chat_history=chat_history,
          search_queries_only=True
        )
        #pprint(dict(resp))
        all_documents = []
        print("Genegereerde queries:")
        for q in resp.search_queries:
            print(q.text)
            all_documents += get_bron_documents(q.text)
        print("%d documenten meegestuurd" % (len(all_documents,)))
        pprint(all_documents)
        #all_documents=[]

        for event in co.chat_stream(
          model="command-r-plus",
          message=qst,
          chat_history=chat_history,
          documents=all_documents,
          prompt_truncation='AUTO'
        ):
            if event.event_type == "text-generation":
                sys.stdout.write(event.text)
            elif event.event_type == "stream-end":
                print()
                chat_history = [dict(e) for e in event.response.chat_history]
            elif event.event_type == 'citation-generation':
                sys.stdout.write(str(event) + "\n")
            else:
                print(event.event_type)
        print("Chat history:")
        print("----------------------------------")
        print(chat_history)
        print("----------------------------------")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
