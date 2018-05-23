import sys

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

def getSpellURL(spell):
    return spell['b']['i']['a']['@href']

def isBasicSpell(spell):
    return 'i' not in spell.keys()
