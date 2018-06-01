import sys
import xmltodict
import lxml.etree as ET

base_url = 'http://www.pathfinder-fr.org/Wiki/'

def preTreat(data):
    dataList = data['html']['body']['form']['table']['tr'][0]['td'][1]['div'][1]['div']['div'][1]['div']['div'][3]['ul'][0]['li']
    return dataList

def selectSpellsURL(spells):
    basicSpells = []
    for spell in spells:
        if isBasicSpell(spell):
            spellURL = getSpellURL(spell)
            basicSpells.append(base_url + spellURL)
    return basicSpells

"""def getSpellURL(spellList):
    spellLinks = []
    for spell in spellList:
        dict_ = xmltodict(spell)
        try:
            spellLinks.append(dict_['b']['i']['a']['@href'])
    return None"""

def isBasicSpell(spell):
    return 'i' not in spell.keys()

def extractSpellsURL(page):
    root = ET.HTML(page)
    spellsList = root.xpath('//li/b/i/a[@class="pagelink"]/@href')
    for i in range(len(spellsList)):
        spellsList[i] = base_url + spellsList[i]
    return spellsList

"""def spellFilter(tag):
    return tag.find(class="pagelink") not None"""
