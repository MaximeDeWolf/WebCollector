import sys
import urllib3
import feature_extractor
import lxml.etree as ET

class webCollector:

    def __init__(self):
        self._http = urllib3.PoolManager()

    def listToSingle(function):
        def listHandler(self, url, *args, **kwargs):
            if isinstance(url, list):
                res = []
                for e in url:
                    res.append(function(self, e, *args, **kwargs))
                return res
            else:
                return function(self, url, *args, **kwargs)
        return listHandler

    def strToHTML(function):
        def converter(self, etree, *args, **kwargs):
            if isinstance(etree, ET._Element):
                return function(self, etree, *args, **kwargs)
            else:
                newEtree = ET.HTML(etree)
                return function(self, newEtree, *args, **kwargs)
        return converter

    @listToSingle
    def fetchPage(self, url):
        response = self._http.request('GET', url)
        return response.data.decode('utf-8')

    def fetchAndExtract(self, url, XPathExpression):
        page = self.fetchPage(url)
        data = self.extractData(page, XPathExpression)
        return data

    @listToSingle
    def extractData(self, page, XPathExpression):
        root = ET.HTML(page)
        data = root.xpath(XPathExpression)
        return data

    @listToSingle
    @strToHTML
    def extract(self, etree, pattern, strTransformer=lambda x:x):
        data = {}
        for key in pattern.keys():
            if isinstance(pattern[key], dict) or isinstance(pattern[key], list):
                data[key] = extract(etree, pattern[key])
            else:
                data[key] = strTransformer(etree.xpath(pattern[key]))
        return data
