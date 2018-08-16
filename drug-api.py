
import argparse 
import urllib3
import json
import certifi
import re
import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom


Rxcui = '88014'
NUI = 'N0000152900'
ndc_prop = '0069-3150-83'
drug_name = 'cymbalta'
##NDFRT
id_type = 'RXCUI'
id_string = '161'
concept_name = 'morphine'
kind_name = 'DRUG_KIND'
concept_kind = 'pharmacokinetics_kind'
nui_all_info = 'N0000152900'
pharmacokinetics_kind = 'DRUG_KIND'
rxcui = '1234567890'


RxNav_base_url = 'https://rxnav.nlm.nih.gov/REST/'
FDA_base_url = 'https://api.fda.gov/drug/'
PUBMED_base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
term = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+20089[pdat]'
PUBMED_query = PUBMED_base_url + 'esearch.fcgi?db=pubmed&term=' + term + 'usehistory=y'

FDA_Adverse_Event =FDA_base_url +  'event.json?'
FDA_enforcement = FDA_base_url +'enforcement.json?'

adverse_search = FDA_Adverse_Event + 'search=patient.drug.openfda.pharm_class_epc:\"nonsteroidal+anti-inflammatory+drug\"&'
adverse_result_count = 'count=patient.reaction.reactionmeddrapt.exact'


RX_NORM_INFO = RxNav_base_url + '/RxTerms/'
RX_NORM_Drug_Interactions = RxNav_base_url + '/interaction/interaction.json?rxcui=' + Rxcui + '&sources=ONCHigh'
RX_NORM_AllProperties = RxNav_base_url + '/rxcui/' + rxcui + '/allProperties.json?prop=all'
## search=field:term



## DISEASE_KIND, DOSE_FORM_KIND, DRUG_KIND, INGREDIENT_KIND, MECHANISM_OF_ACTION_KIND
## PHARMACOKINETICS_KIND, PHYSIOLOGIC_EFFECT_KIND, THERAPEUTIC_CATEGORY_KIND

NDFRT_concept_by_id = RxNav_base_url + '/Ndfrt/id?idType='+ id_type + '&idString=' + id_string
NDFRT_search = RxNav_base_url + '/Ndfrt/search?conceptName=' + concept_name + '&kindName=' + kind_name
NDFRT_get_all_concepts = RxNav_base_url + '/Ndfrt/allconcepts?kind=' + pharmacokinetics_kind
NDFRT_all_info = RxNav_base_url + '/Ndfrt/allInfo.json?nui=' + nui_all_info
NDFRT_get_child_concepts = RxNav_base_url + '/Ndfrt/childConcepts?nui=' + nui_all_info + '&transitive=true'

DAILY_MED_DOWNLOADS = 'https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm'


class DrugAPI:
	def  __init__(self,type):
		parser = argparse.ArgumentParser(description='HTTP Client Example') 
		if type == 'rxnorm':
			parser.add_argument('--host', action="store",dest="host",  default=RxNav_base_url) 
		elif type == 'spl':
			parser.add_argument('--host', action="store",dest="host",  default=FDA_base_url) 
		elif type == 'pubmed':
			parser.add_argument('--host', action="store",dest="host",  default=PUBMED_base_url) 

		given_args = parser.parse_args()  
		self.host = given_args.host 
		self.http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where()) 

	def run_test(self):
		drugInteractions = getDrugInteractions(Rxcui)
		ndfrt_allinfo = get_NDFRT_allinfo()
		getAll_NDC_Properties = getAll_NDC_Properties(ndc_prop)
		get_drugs = getDrugInfo(drug_name)

	def do_query(http,query_type,params):

		http_string = ''
		if query_type == 'getAllRxNormInfo':
			http_string = getAllRxNormInfo(params)
		response = self.http.request('GET',http_string)
		drug_data = response.data.decode('utf-8')


	def getAllRxNormInfo(rxcuid):
		## returns
		##<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
		##<rxtermsdata>
		##<rxtermsProperties>
		##       <brandName></brandName>
		##       <displayName>Ondansetron (Oral Disintegrating)</displayName>
		##        <synonym></synonym>
		##        <fullName>Ondansetron 4 MG Disintegrating Oral Tablet</fullName>
		##        <fullGenericName>Ondansetron 4 MG Disintegrating Oral Tablet</fullGenericName>
		##         <strength>4 mg</strength>
		##         <rxtermsDoseForm>Tab</rxtermsDoseForm>
		##         <route>Oral Disintegrating</route>
		##         <termType>SCD</termType>
		##          <rxcui>104894</rxcui>
		##          <genericRxcui>0</genericRxcui>
		##           <rxnormDoseForm>Disintegrating Oral Tablet</rxnormDoseForm>
		##          <suppress></suppress></rxtermsProperties></rxtermsdata>

		get_rx_norm_info = RX_NORM_INFO + rxcuid + '/allinfo'
		return (get_rx_norm_info)

	def getRXNormDrugInfo(drug_name):
		get_drugs = 'drugs?name=' + drug_name
		http_string = RxNav_base_url+get_drugs

	def get_NDFRT_allinfo(NUI):
		ndfrt_allinfo = 'allInfo.json?nui='+NUI
		http_string = RxNav_base_url+ ndfrt_allinfo

	def getDrugInteractionsSources():
		getDrugInteractionSource = '/interaction/sources.json'
		http_string = RxNav_base_url+getDrugInteractionSource

	def getDrugInteractions(rxcui):
		drugInteractions = 'interaction/interaction.json?rxcui=' + rxcui +'&sources=ONCHigh'
		drugInteractionsList = 'interaction/list.json?rxcuis=' ##iterate and append array elem with rxcui
		http_string = RxNav_base_url+ drugInteractions

	def getAll_NDC_Properties(ndc_prop):
		## NDC 2 segment   67544-355
		## NDC 3 segment   0781-1506-10
		## NDC11                 00904629161
		## RxCUI                   213270
		## SPL_SET_ID          1C5BC1DD-E9EC-44C1-9281-67AD482315D9	
		getAll_NDC_Properties = 'ndcproperties?id=' + ndc_prop
		http_string = RxNav_base_url+ getAll_NDC_Properties






