import sys
import web_collector as WC
import lxml.etree as ET

def excludeNonBasicSpells(XPathObject):
    root = ET.HTML(XPathObject)
    icons = root.xpath('//img[@class="opachover"]')
    return len(icons)==0

def makeShallow(list_):
    shallowList = []
    for elem in list_:
        if isinstance(elem, list):
            shallowList.extend(makeShallow(elem))
        else:
            shallowList.append(elem)
    return shallowList

def cleanData(data):
    if len(data) == 1 :
        newData = data[0]
        return newData.replace('\t', '').replace('\n', '').replace('\r', '')
    else:
        newData = []
        for i, string in enumerate(data):
            newData[i] = string.replace('\t', '').replace('\n', '').replace('\r', '')
        return newData

#'//div[@id="PageContentDiv"]'

pattern = {
    "spell" : '//h1[@class="pagetitle"]/text()'
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
    spellName = web_collector.extract(basicSpells, pattern, strTransformer=cleanData)
    print(spellName)
