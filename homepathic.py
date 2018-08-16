
import os
import pathlib
from lxml import etree



files_to_parse = []
xml_file = []

def getFileList():
	current_dir = os.getcwd()
	files = os.listdir('.')
	for file in files:

		full_dir = os.path.join(current_dir,file)
		if os.path.isdir(full_dir):
			med_dir_list = os.listdir(full_dir)
			for med_dir in med_dir_list:
				file_parse = os.path.join(full_dir,med_dir)
				files_to_parse.append(file_parse)


	for file in files_to_parse:
		f, ext = os.path.splitext(file)
		if ext == '.xml':
			xml_file.append(file)


def parse_section_text(section_text):
	for para in section_text: 
		if para.tag == '{urn:hl7-org:v3}paragraph':
			print (str(para.text))

def parse_section(section):
	for sect in section:
		print ('parse section: ' + sect.tag)
		if sect.tag == '{urn:hl7-org:v3}title':
			print ('                section title: ' + sect.text)

def parse_subject(subject):

	for subj in subject:
		if subj.tag == '{urn:hl7-org:v3}manufacturedProduct':
			manu = subj.getchildren()
			for man in manu:
				if man == '{urn:hl7-org:v3}manufacturedProduct':
					attributes = man.getchildren()
					for attrib in attributes:
						if attrib == '{urn:hl7-org:v3}name':
							print ('                 HOMEO NAME: ' + attrib.text)
						elif attrib == '{urn:hl7-org:v3}asEntityWithGeneric':
							print (attrib.tag)


def parse_component(component):

	for part in component:
		if part.tag == '{urn:hl7-org:v3}section':
			section_items = part.getchildren()
			for item in section_items:
				if item.tag == '{urn:hl7-org:v3}title':
					print ('-------' + str(item.text) + '---------------')
				elif item.tag == '{urn:hl7-org:v3}text':
					parse_section_text(item.getchildren());
				##elif item.tag == '{urn:hl7-org:v3}id':
				##elif item.tag == '{urn:hl7-org:v3}code':
					


				

def parse_homeopathic():
	rx_count = 0
	otc_count = 0 
	no_name_count = 0;
	for xml_f in xml_file:
		doc = etree.parse(xml_f)
		root = doc.getroot()
		drug_name = ''
		drug_type = ''
		drug_id = ''
		med_type = ''
		print ('\n#########################################HOMEPATHIC DRUG PROFILE---------\n')
		for elt in root.getiterator():
			if elt.tag == '{urn:hl7-org:v3}document':
				elem = elt.getchildren()
				for e in elem:
					if e.tag == '{urn:hl7-org:v3}component':
						components = e.getchildren()
						for component in components:
							if component.tag == '{urn:hl7-org:v3}structuredBody':
								structBodyComp = component.getchildren()
								for struct_comp in structBodyComp:
									if struct_comp.tag == '{urn:hl7-org:v3}component':
										comp_parts = struct_comp.getchildren()
										parse_component(comp_parts)
										
getFileList()
parse_homeopathic()
