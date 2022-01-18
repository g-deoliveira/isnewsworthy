import requests

import pandas as pd

import os
import json
from pathlib import Path, PurePath



def split(line):
    '''
    sample input:

        'True,https://ny.eater.com/2020/9/1/21408529/speedy-romeo-lower-east-side-closes\n'
        'False,https://www.theinfatuation.com/new-york/reviews/speedy-romeo\n'

    split the line into the True/False flag and url
    and remove the new-line character at the end of the url

    raise ValueError if unable to parse
    '''

    if line.startswith('True,'):

        return True, line[5:-1]

    elif line.startswith('False,'):

        return False, line[6:-1]

    elif line == '\n':

        return None, None

    else:

        raise ValueError(f'Problem parsing the data {line}')


class Response:
    '''
    The purpose of this class is to initialize an empty URL Get-Response object
    '''

    def __init__(self, text=None):
        self.text = text
        self.headers = None
        self.ok = False


class WebsiteSource:
    '''
    This class takes the URL of a website and the corresponding is_newsworthy label as input.

    It provides these methods:
        - make_http_request():
            make a call to the website using the requests package to obtain the source html code.

        - write_metadata_to_json(file_name):
            write the response info including headers as well as the URL and label to a metadata
            file in the data/parsed directory

        - write_html_source_to_file(file_name):
            write the html source code to an html file in the data/parsed directory
    '''

    def __init__(self, url, label, timeout=(19,19)):
        '''
        url: is the http URL of the website whose source code we are obtaining
        label: boolean field that denotes whether or not the website is newsworthy
        timeout: (int, int) contains the connect timeout and the read timeout
            - the connect timeout is the number of seconds Requests will wait
            for the client to establish a connection
            - the read timeout is the number of seconds the client will wait
            for the server to send a response
        '''
        self._url = url
        self._label = label
        self._timeout = timeout
        self._error = None

        # initialize an empty URL response
        self._response = Response()

    def make_http_request(self):
        '''
        Make a request for the URL
        Log any errors
        '''

        try:
            self._response = requests.get(self._url, timeout=self._timeout)
            self._response.raise_for_status()

        except requests.HTTPError as err:
            print(err)
            self._error = str(err)

        except requests.Timeout as err:
            print(err)
            self._error = str(err)

        except Exception as err:
            print(err)
            self._error = str(err)

    def write_metadata_to_json(self, pathlib_path):
        text = json.dumps(self.to_json(), indent=2)
        pathlib_path.write_text(text)

    def to_json(self):
        return {
            'url': self._url,
            'label': self._label,
            'ok': self.ok,
            'error': self._error,
            'headers': dict(self.headers if self.headers else {}),
        }

    def write_html_source_to_file(self, pathlib_path):
        pathlib_path.write_text(self.text if self.text else '')

    @property
    def ok(self):
        return self._response.ok

    @property
    def headers(self):
        return self._response.headers

    @property
    def error(self):
        return self._error

    @property
    def text(self):
        return self._response.text

    def __repr__(self):
        text = f'URL:{self._url}\nLABEL:{self._label}\nHEADERS:{self.headers}\nERROR:{self._error}\nSOURCE_LENGTH:{len(self._response.text)}'
        return text


if __name__ == '__main__':

    # this URL is successfully obtained
    url = 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/speedy-romeo'
    website_source = WebsiteSource(url, label=False, timeout=(4,4))
    website_source.make_http_request()

    assert website_source.ok == True
    assert website_source._error is None


    # this URL is forbidden and the source code cannot be obtained
    url = 'https://jerseybites.com/2021/12/myron-mixon-pitmaster-barbeque-opening-december-13-in-hoboken/'
    website_source = WebsiteSource(url, label=True, timeout=(4,4))
    website_source.make_http_request()

    assert website_source.ok == False
    assert website_source.error == '403 Client Error: Forbidden for url: https://jerseybites.com/2021/12/myron-mixon-pitmaster-barbeque-opening-december-13-in-hoboken/'


    # this generates a time-out error
    url = 'https://www.kansascity.com/news/business/biz-columns-blogs/cityscape/article256452921.html'
    website_source = WebsiteSource(url, label=True, timeout=(4,4))
    website_source.make_http_request()

    assert website_source.ok == False
    assert website_source.error == "HTTPSConnectionPool(host='www.kansascity.com', port=443): Read timed out. (read timeout=4)"

