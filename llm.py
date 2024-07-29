#!/usr/bin/env python

import sys
import os
import re
from pprint import pprint
import json

import cohere


def main(argv):
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    resp = co.chat(
      model="command-r-plus",
      message="Hoe ziet het bestuurlijke apparaat van NL er uit?",
      search_queries_only=True
    )
    pprint(dict(resp))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
