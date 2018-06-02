import sys
import web_collector as WC
import lxml.etree as ET

def excludeNonBasicSpells(XPathObject):
    root = XPathObject
    icons = root.xpath('//img[@class="opachover"]')
    return len(icons)==0

if __name__ == '__main__':
    url = 'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts.ashx'
    base_url = 'http://www.pathfinder-fr.org/Wiki/'
    XPathExpression = '//li/b/i/a[@class="pagelink"]/@href'
    web_collector = WC.webCollector()
    spellsURL = web_collector.fetchAndExtract(url, XPathExpression)
    for i in range(len(spellsURL)):
            spellsURL[i] = base_url + spellsURL[i]
    spellsInfo = web_collector.fetchAndExtract(spellsURL, '//div[@id="PageContentDiv"]')
    basicSpells = list(filter(excludeNonBasicSpells, spellsInfo))
    print(ET.tostring(basicSpells[0], pretty_print=True))
