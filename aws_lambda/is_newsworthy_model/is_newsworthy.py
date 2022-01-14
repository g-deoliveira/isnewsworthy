'''
This lambda script takes as input a website url and returns a prediction 
along with some metadata regarding whether or not the website is "newsworthy" 
or not.
'''
import time
import pickle
import requests
from bs4 import BeautifulSoup
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

class IsNewsWorthy:
    '''
    For a given URL, this class downloads the source code that renders the website,
    scrapes the content to assemble the expected features, deserializes the machine learning
    model, runs the prediction, and returns the result along with processing times

    usage:
        inw = IsNewsWorthy(url)
        response = inw.is_newsworthy_response()
    
    '''

    def __init__(self, url, model_file_name='best_estimator.pickle'):

        self.url = url
        self.model_file_name = model_file_name

        # initialize an empty dictionary to store processing times
        self.compute_times = dict()

    
    def is_newsworthy_response(self):
        '''
        This method processes the URL and returns the prediction and associated metadata.
        '''
            
        self._get_website_source_code()
        self._scrape_source_code()
        self._load_model()
        self._run_prediction()

        response = {
            'prediction':str(self.prediction[0]),
            'times': self.compute_times
        }

        return response


    def _get_website_source_code(self, timeout=(15,15)):

        start = time.perf_counter()

        self.response = requests.get(self.url, timeout=timeout)

        request_time = time.perf_counter() - start
        self.compute_times['request_time'] = request_time
        logging.info(f'Requested article source (elapsed time {request_time:.3f})')
        

    def _scrape_source_code(self):

        start = time.perf_counter()

        raw_text = self.response.text
        soup = BeautifulSoup(raw_text, 'html.parser')

        links = [item.text for item in soup.find_all('a')]
        h1 = [item.text for item in soup.find_all('h1')]
        h2 = [item.text for item in soup.find_all('h2')]
        h3 = [item.text for item in soup.find_all('h3')]
        img = soup.find_all('img')

        # text:
        paragraphs = [item.text for item in soup.find_all('p')]
        paragraph_count = len(paragraphs)
        document = ' '.join(paragraphs)

        features = {
            'paragraph_count': paragraph_count,
            'link_count': len(links),
            'h1_count': len(h1),
            'h2_count': len(h2),
            'h3_count': len(h3),
            'img_count': len(img),
            'character_count': len(document),
            'document': document,
        }
        self.features = pd.DataFrame([features])

        scraped_time = time.perf_counter() - start
        self.compute_times['scraped_time'] = scraped_time
        logging.info(f'Scraped features (elsapsed time {scraped_time:.3f})')


    def _load_model(self):
        start = time.perf_counter()

        with open(self.model_file_name, "rb") as f:
            self.model = pickle.load(f)

        model_load_time = time.perf_counter() - start
        self.compute_times['model_load_time'] = model_load_time
        logging.info(f'Loaded model (elapsed time {model_load_time:.3f})')


    def _run_prediction(self):
        start = time.perf_counter()

        self.prediction = self.model.predict(self.features)

        prediction_time = time.perf_counter() - start
        self.compute_times['prediction_time'] = prediction_time
        logging.info(f'Computed prediction (elapsed time {prediction_time:.3f})')



if __name__ == "__main__":

    import json

    url = 'https://www.illinoisfoodpoisoningattorney.com/chicago-food-poison-lawyer/another-food-poisoning-case-shutters-chipotle-restaurant'
    
    inw = IsNewsWorthy(url)
    response = inw.is_newsworthy_response()

    print(json.dumps(response, indent=4))
    