import sys
import lxml.etree as ET

def extractSpellCarac(spell):
    root = ET.HTML(page)
    spellsList = root.xpath('//li/b/i/a[@class="pagelink"]/@href')
