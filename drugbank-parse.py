import json
import csv
import re
from bs4 import BeautifulSoup
from nltk import ngrams
import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom
from DrugBankData import DrugBankInteraction
from DrugBankData import DrugBankAdverse
from DrugBankData import DrugBankProduct
from DrugBankData import DrugBankDosage
from DrugBankData import DrugBankFoodInteraction
from DrugBankData import DrugBank

drugbank_file = open('DrugBank.html','w')
global_drug_bank = {}
drug_bank_food = open('Drugbank-food-x.txt','w')
drug_bank_regex = open('Drugbank-regex.txt','w')
other_ddi_array = []

## ONTOLOGIES
symptom_ontology = {}
med_by_pharma = {}

def parse_drugbank():
	print('Parsing drugbank')
	item_count = 0
	parse_count = 0
	tree = etree.parse('./SourceProcessFiles/DrugBank-full-database.xml') 
	root = tree.getroot()
	for child in root:
		drug_bank_id_val = ''
		for elem in child:
			if elem.tag == '{http://www.drugbank.ca}drugbank-id':
				primary = elem.get('primary')
				if primary == 'true':
					drug_bank_id_val  = elem.text
					drug_bank_item = DrugBank(elem.text,child)
					global_drug_bank[drug_bank_item.unii] = drug_bank_item
					item_count = item_count + 1

	drug_bank_count =0
	master_effects_ontology = {}
	global_drug_bank_keys = global_drug_bank.keys()

	drugbank_file.write('<HTML>\n')
	drugbank_file.write('<head>\n')
	drugbank_file.write('<meta charset=\"utf-8\"/>')
	drugbank_file.write('<link rel=\"stylesheet\" type=\"text/css\" href=\"css/style.css\" />')
	drugbank_file.write('<script defer src=\"https://use.fontawesome.com/releases/v5.0.6/js/all.js\"></script>')
	drugbank_file.write('<title>MEDUCATE PHARMACEUTICAL GUIDE</title>')
	drugbank_file.write('</head>')
	drugbank_file.write('<BODY>\n')
	drugbank_file.write('<H1> DRUG BANK MEDS </H1>\n')


	for key in global_drug_bank_keys:
		drug_bank_obj = global_drug_bank[key]
		drug_bank_obj.regexDDI()
		drug_bank_obj.parse_indication(drug_bank_obj.indication)
		drug_bank_count = drug_bank_count + 1
		if drug_bank_item.parse == 'false':
			parse_count = parse_count + 1
	
	drugbank_file.write('</BODY>\n')
	drugbank_file.write('</HTML>\n')
	drugbank_file.close()

	physio_ont_file = open('Physiological-Ontology.txt','w')
	onto_keys = symptom_ontology.keys()
	for onto in onto_keys:
		print (onto + ':  ' + symptom_ontology[onto])
		physio_ont_file.write(onto+','+symptom_ontology[onto])
	physio_ont_file.close()



parse_drugbank()

