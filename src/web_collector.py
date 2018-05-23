import sys
import urllib3
import xmltodict
import spell_collector

_http = urllib3.PoolManager();

def fetchPage(url):
    response = _http.request('GET', url)
    return response.data.decode('utf-8')

def parseToDict(page, index=0):
    try:
        return xmltodict.parse(page)
    except Exception as e:
        print("Exception au sort {}".format(index))

if __name__ == '__main__':
    url = 'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts.ashx'
    page = fetchPage(url)
    content = parseToDict(page)
    spells = spell_collector.preTreat(content)
    spellURLs = spell_collector.selectSpellsURL(spells)
    spellsFeatures = [parseToDict(fetchPage(url)) for url in spellURLs]
    """
    for i, url in enumerate(spellURLs):
        parseToDict(fetchPage(url), index=i)
    """
    print(spellURLs[16])
