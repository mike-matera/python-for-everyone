"""
Example code for the Wikipedia project
"""

import requests
import json 
import sys 
import pprint 


def get_wikipage(title) :
    '''Get a Wikipedia page.'''

    url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={title}'
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def main():
    
    if len(sys.argv) != 2: 
        print ('usage: {sys.argv[0]} <page_title>')
        quit(-1)
    
    data = get_wikipage(sys.argv[1])
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(data)


if __name__ == '__main__':
    main()
