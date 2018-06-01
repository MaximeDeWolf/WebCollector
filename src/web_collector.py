import sys
import urllib3
import spell_url_collector
import lxml.etree as ET


_http = urllib3.PoolManager();

def fetchPage(url):
    response = _http.request('GET', url)
    return response.data.decode('utf-8')

def excludeNonBasicSpells(spell):
    root = ET.HTML(spell)
    icons = root.xpath('//img[@class="opachover"]')
    return len(icons)==0

"""
class="opachover" permet de discalifier les sorts qui ne sont pas de base
"""
#<img title="Source : Ultimate Magic/Art de la Magie" class="opachover" src="http://www.pathfinder-fr.org/Wiki/public/Upload/Illustrations/Logos/logoUM.gif" style="opacity: 0.7" loop="infinite" />

"""
<div id="PageContentDiv"> pour travailler sur portion utile (perfomance)
"""

if __name__ == '__main__':
    url = 'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts.ashx'
    page = fetchPage(url)
    spellsURL = spell_url_collector.extractSpellsURL(page)
    #print(spellsURL)
    spells = [fetchPage(url) for url in spellsURL]
    #print(spells[0])
    filter(excludeNonBasicSpells, spells)
