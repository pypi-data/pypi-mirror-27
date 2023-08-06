"""module for loading data from json file or from api"""
from __future__ import print_function

from os import environ
from time import sleep

import json
import requests


API_RETRY = 3

class GetData(dict):
    """load data from json file or api"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, url=None, file_name='output.json', source="file",
                 key_var="PCT_API_READ_KEY", silent=False):
        dict.__init__(self)
        self.url = url
        self.file_name = file_name
        self.source = source.lower()
        self.key_var = key_var
        self.silent = silent
        self.headers = None

        results = self.get_data()
        self.data = results['data']
        self.status_code = results['status_code']
        self.error_msg = results['error_msg']

    def __whisper(self, text):
        """print wrapper to check silent parameter"""
        if not self.silent:
            print(text)

    def get_data(self):
        """Load data from either a source file or the api"""

        #load from file
        if self.source == "file":
            self.__whisper("Loading File...")
            try:
                with open(self.file_name, 'rb') as stored_file:
                    data = json.loads(stored_file.read())
                    return {
                        'status_code': 200,
                        'error_msg': None,
                        'data': data
                    }
            #try api if file is missing
            except (IOError, ValueError) as error:
                if self.url:
                    if error.__class__.__name__ == "IOError":
                        self.__whisper("No file exists.  Pulling from api...")
                    elif error.__class__.__name__ == "ValueError":
                        self.__whisper("File isn't valid JSON.  Pulling from api...")
                    return self._api_load()
                self.__whisper("Bad file AND no url specified.  No data returned.")
                return {
                    'status_code': 404,
                    'error_msg': error,
                    'data': None
                }
        #load from api
        elif self.source == "api":
            return self._api_load()
        #bad source
        self.__whisper("Source paramater must be 'api' or 'file'")
        return {
            'status_code': 500,
            'error_msg': "Invalid source parameter.  Must be 'api' or 'file'",
            'data': None
        }

    def _api_load(self):
        """load data from api"""

        #get api_key or return 401 if missing.
        try:
            api_key = environ[self.key_var]
        except KeyError:
            self.__whisper(self.key_var + " could not be loaded.  Unauthorized")
            return {
                'status_code': 401,
                'error_msg': self.key_var + ' could not be loaded.  Unauthorized.',
                'data': None
            }

        #set headers and amde initial api_try.
        self.headers = {
            'x-api-key': api_key,
            'Cache-Control': 'no-cache'
        }
        return_request, resp_headers = self._api_try(None)
        if return_request['data'] is None:
            return return_request

        # Get page count, output if none or page count is 1
        try:
            page_count = int(resp_headers.get("x-pagination-page-count"))
            if page_count == 1:
                raise BaseException
            return_request['data'] = []
        except (KeyError, TypeError, BaseException):
            self.__whisper("No page count / One page specified.  Writing Single Page...")
            json_string = return_request['data']
            clean_json_string = '[' + json_string.lstrip('[').rstrip(']') + ']'
            return_request['data'] = json.loads(clean_json_string)
            self._write_data(json.loads(clean_json_string))
            return return_request

        #Download each page
        self.__whisper("%s pages to be downloaded" % page_count)
        for page in range(1, page_count+1):
            single_response, resp_headers = self._api_try(page)
            if single_response['data']:
                json_string = single_response['data']
                clean_json_string = '[' + json_string.lstrip('[').rstrip(']') + ']'
                return_request['data'] = return_request['data'] + json.loads(clean_json_string)
        self._write_data(return_request['data'])
        return return_request        

    def _write_data(self, data):
        with open(self.file_name, 'w') as output_file:
            output_file.write(json.dumps(data, sort_keys=True, indent=4))
            output_file.close()
        self.__whisper("File written successfully...")


    def _api_try(self, page):
        tries = 0
        self.__whisper("\nPage: %s" % page)
        while tries < API_RETRY:
            self.__whisper("Sending API request...")
            response, resp_headers = self._api_call(page)
            if response['error_msg']:
                self.__whisper(response['error_msg'])
            if response['status_code'] == 401 or response['status_code'] == 404:
                return response, None
            if response['data']:
                self.__whisper("Response returned successfully.")
                return response, resp_headers
            self.__whisper("Trying again in %s seconds\n" % ((tries+1)**2))
            sleep((tries+1)**2)
            self.__whisper("LET'S DO THIS!!!!")
            tries += 1
        response['error_msg'] = "Amount of Fails Exceeded.  The API doesn't want to talk to you today."
        return response, resp_headers


    def _api_call(self, page):
        return_request = {
            'status_code': 200,
            'data': None,
            'error_msg': None
        }

        temp_url = self.url
        if page is not None and "?" not in self.url:
            temp_url += "?Page=" + str(page)
        elif page is not None:
            temp_url += "&Page=" + str(page)
        try:
            self.__whisper("GET %s" % temp_url)
            req = requests.get(temp_url, headers=self.headers)
        except Exception:
            return_request['error_msg'] = 'API Server could not be reached'
            return_request['status_code'] = 404
            return return_request, None

        return_request['status_code'] = req.status_code
        if req.status_code != 200:
            self.__whisper("WARNING:  API call status code was %s" % req.status_code)
        if req.status_code == 401:
            return_request['error_msg'] = "Unauthorized.  Your API key isn't working..."
        elif req.status_code == 404:
            return_request['error_msg'] = "Not found.  Your url is probably wrong or you're not on VPN"
        elif req.status_code == 502:
            return_request['error_msg'] = "The response failed.  This happens from time to time."
        elif req.status_code == 503:
            return_request['error_msg'] = "Internal Server Error.  The API might be down."
        else:
            try:
                return_request['data'] = json.dumps(req.json())
            except ValueError:
                return_request['error_msg'] = 'Returned request could not be converted to json'

        return return_request, req.headers

