import sys
import lxml.etree as ET

def extractData(page, XPathExpression):
    root = ET.HTML(page)
    data = root.xpath(XPathExpression)
    return data
