'''
This lambda script takes as input a website url and returns a prediction 
along with some metadata regarding whether or not the website is "newsworthy" 
or not.
'''
import time
import pickle
import requests
from bs4 import BeautifulSoup

from is_newsworthy import IsNewsWorthy


def handler(event, context):
    

    url = event.get('url')
    if not url:
        print('URL is None')
    
    inw = IsNewsWorthy(url)
    response = inw.is_newsworthy_response()
    
    return response


if __name__ == "__main__":
    import json

    event = {
        'url':'https://www.illinoisfoodpoisoningattorney.com/chicago-food-poison-lawyer/another-food-poisoning-case-shutters-chipotle-restaurant'
    }
    context = None

    response = handler(event, context)

    print(json.dumps(response, indent=4))
    