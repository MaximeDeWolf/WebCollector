import urllib3
import lxml.etree as ET

class webCollector:

    def __init__(self):
        self._http = urllib3.PoolManager()

    def listToSingle(function):
        """
        This function helps to threat a list as it was a single object.
        Designed to be used as a decorator.
        """
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
        """
        Ensure that a certain parameter is always an Xpath object
        """
        def converter(self, etree, *args, **kwargs):
            if isinstance(etree, ET._Element):
                return function(self, etree, *args, **kwargs)
            else:
                newEtree = ET.HTML(etree)
                return function(self, newEtree, *args, **kwargs)
        return converter

    @listToSingle
    def fetchPage(self, url):
        """
        Get the html code store at the 'url' address
        """
        response = self._http.request('GET', url)
        return response.data.decode('utf-8')

    def fetchAndExtract(self, url, XPathExpression):
        """
        Get the html code from 'url' and extract an Xpath object obtained
        thanks to 'XPathExpression'
        """
        page = self.fetchPage(url)
        data = self.extractData(page, XPathExpression)
        return data

    @listToSingle
    def extractData(self, page, XPathExpression):
        """
        Return the result of an 'XPathExpression' over a 'page'
        """
        root = ET.HTML(page)
        data = root.xpath(XPathExpression)
        return data

    @listToSingle
    @strToHTML
    def extract(self, etree, pattern, strTransformer=lambda x:x):
        """
        Browse a dictionnary and replace all the XPath expression it contains
        by the result it produces on the 'etree' Xpath object.

        For example:
        pattern = {'name': '//name/text()'},
        etree = <name>John Doe<\>

        will produce this result {'name': 'John Doe'}
        """
        data = {}
        for key in pattern.keys():
            if isinstance(pattern[key], dict) or isinstance(pattern[key], list):
                data[key] = extract(etree, pattern[key])
            else:
                data[key] = strTransformer(etree.xpath(pattern[key]))
        return data
