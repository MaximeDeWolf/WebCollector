import sys
import web_collector as WC
import lxml.etree as ET

"""
This file is an example of how to use this library
"""

def excludeNonBasicSpells(XPathObject):
    """
    Analyse an XPath element and return true iff it matches a spell which make
    parts of the basic rule book of Pathfinder.
    """
    root = ET.HTML(XPathObject)
    icons = root.xpath('//img[@class="opachover"]')
    return len(icons)==0

def makeShallow(list_):
    """
    Browse a list and roll up all its items in order to place them at the same depth.
    For example, the list [a, [b, [c, d, e]], [[[f]]] ] will become [a, b, c, d, e, f].
    """
    shallowList = []
    for elem in list_:
        if isinstance(elem, list):
            shallowList.extend(makeShallow(elem))
        else:
            shallowList.append(elem)
    return shallowList

def cleanData(data):
    """
    Remowe all the special from the 'data'
    """
    newData = []
    for string in data:
        newData.append(string.replace('\t', '').replace('\n', '').replace('\r', ''))
    return newData

#'//div[@id="PageContentDiv"]'

spellPattern = {
    "name" : '//h1[@class="pagetitle"]/text()',
    "school" : '//div[@id="PageContentDiv"]//b[1]/following-sibling::a[1]/text()',
    "class" : '//div[@id="PageContentDiv"]/child::node()[following::node()[text()="Temps d\'incantation"][preceding::node()[text()="Niveau"]]/text()',
    #"level" : '//div[@id="PageContentDiv"]//b[2]/following-sibling::text()[position() < count(//div[@id="PageContentDiv"]//b[3]/preceding-sibling::text())-1]',
    "time" : '//h1[@class="pagetitle"]/text()',
    "component" : '//h1[@class="pagetitle"]/text()',
    "range": '//h1[@class="pagetitle"]/text()',
    "target": '//h1[@class="pagetitle"]/text()',
    "duration": '//h1[@class="pagetitle"]/text()',
    "JS": '//h1[@class="pagetitle"]/text()',
    "RM": '//h1[@class="pagetitle"]/text()',
    "effect": '//h1[@class="pagetitle"]/text()'
}

if __name__ == '__main__':
    url = 'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts.ashx'
    base_url = 'http://www.pathfinder-fr.org/Wiki/'
    XPathExpression = '//li/b/i/a[@class="pagelink"]/@href'
    web_collector = WC.webCollector()
    spellsURL = web_collector.fetchAndExtract(url, XPathExpression)
    for i in range(len(spellsURL)):
            spellsURL[i] = base_url + spellsURL[i]
    spellsInfo = web_collector.fetchPage(spellsURL[0:10])
    #spellsInfo = makeShallow(spellsInfo)
    basicSpells = list(filter(excludeNonBasicSpells, spellsInfo))
    spellName = web_collector.extract(basicSpells, spellPattern, strTransformer=cleanData)
    #spellName = web_collector.extract(basicSpells, spellPattern)
    root = ET.HTML(basicSpells[0])
    res = root.xpath('//div[@id="PageContentDiv"]/b[3]/preceding-sibling::node()')
    print(res)
    #test = ET.tostring(res, pretty_print=True)
    #print(test)
    print(spellName[0]["class"])
