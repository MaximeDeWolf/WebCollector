import sys
import urllib3
import data_extractor
import feature_extractor
import lxml.etree as ET

class webCollector:

    def __init__(self):
        self._http = urllib3.PoolManager()

    def _fetchPage(self, url):
        response = self._http.request('GET', url)
        return response.data.decode('utf-8')

    def listToSingle(function):
        def listHandler(self, url, expression):
            if isinstance(url, list):
                res = []
                for e in url:
                    res.append(function(self, e, expression))
                return res
            else:
                return function(self, url, expression)
        return listHandler

    @listToSingle
    def fetchAndExtract(self, url, XPathExpression):
        page = self._fetchPage(url)
        data = data_extractor.extractData(page, XPathExpression)
        return data
