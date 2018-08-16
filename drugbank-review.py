import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom
import csv
import re
from bs4 import BeautifulSoup


tree = etree.parse('../DrugBank-full-database.xml') 
root = tree.getroot()
drug_count = 0
for child in root:
	drug_bank_id_val = ''
	for elem in child:
		if elem.tag == '{http://www.drugbank.ca}drugbank-id':
			drug_count = drug_count + 1

print ('Total drug bank count: ' + str(drug_count))
