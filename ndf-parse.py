import json
import csv
import re
import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom
from spldataNDF import  NDFElement
from spldataNDF import SNOMED
from spldataNDF import SNOMED_MAP
from spldataNDF import  RXNNORM
from spldataNDF import  RXNREL


## NDF Files
ndfrt_file = open('ndfrt-format.txt','w')
ndfrt_meta = open('./TextOutput/NDF/NDFRT-Therapeutic-Class','w')
NDF_term_objects = []
ndc_keys = []
ndf_objects = {}
NDF_rxcui_dict = {}


ndf_kind_definition = {}
ndf_role_definition = {}
ndf_property_definition = {}
ndf_association_definition = {}
ndf_qualifier_definition = {}


disease_kinds = {}
physiological_kinds = {}
therapeutic_kinds = {}
dose_kinds = {}
mechanism_of_action_kinds = {}
pharmacokinetics_kinds = {}
ingredient_kinds = {}
drug_kinds = {}

ndf_va_class_level = {}
ndf_ingredient_level = {}
ndf_product_level = {}

definitions_all = {} 

fda_unii = {}
	
ndf_file_definitions = open('./TextOutput/NDF/ndf_definitions.txt','w')
ndf_moa_file = open('./TextOutput/NDF/moa.txt','w')
ndf_disease_file = open('./TextOutput/NDF/disease.txt','w')
ndf_ingredient_file= open('./TextOutput/NDF/ingredient.txt','w')
ndf_drug_file = open('./TextOutput/NDF/drug.text','w')

ndf_prop_file_def = open('./TextOutput/NDF/ndf_props.txt','w')
ndf_role_file_def = open('./TextOutput/NDF/ndf_roles.txt','w')
ndf_kind_file_def = open('./TextOutput/NDF/ndf_kind.txt','w')
ndf_assoc_file_def = open('./TextOutput/NDF/ndf_assoc.txt','w')
ndf_qual_file_def = open('./TextOutput/NDF/ndf_qual.txt','w')
ndf_other_file_def = open('./TextOutput/NDF/ndf_text_other.txt','w')



def read_ndfrt():
	ndf_code_dict_count = {}
	tree = etree.parse('./SourceProcessFiles/NDFRT_Public_2017.11.06/NDFRT_Public_2017.11.06_TDE.xml') 
	root = tree.getroot()
	parse_out_ndf_global_property_def(root)
	name = ''
	codeID = ''

	for child in root:
		if child.tag != 'propertyDef' and child.tag != 'roleDef' and child.tag != 'kindDef' and child.tag != 'associationDef' and child.tag != 'qualifierDef':

			code = ''
			med_id = ''
			namespace = ''
			primitive = ''
			kind = ''
			level = ''
			role_properties = {}
			concept_properties = {}
			item_properties = {}
			association_properties = {}
			qualifier_properties = {}

			for elem in child:
				if elem.tag == 'name':
					name = elem.text
				elif elem.tag == 'code':
					code = elem.text
				elif elem.tag == 'id':
					med_id = elem.text
				elif elem.tag == 'namespace':
					namespace = elem.text
				elif elem.tag == 'primitive':
					primitive = elem.text
				elif elem.tag == 'kind':
					kind = elem.text
					kind_text = ndf_kind_definition[kind]
					
				elif elem.tag == 'definingConcepts':
					concepts = list(elem)
					if kind_text == 'DRUG_KIND':
						ndfrt_file.write('\n-----[CONCEPTS] ------\n')
					for concept in concepts:
						text_concept = concept.text
						final_name = lookupRole(concept.text)
						concept_properties[final_name] = concept.text
						if kind_text == 'DRUG_KIND':
							ndfrt_file.write(final_name + '\n')
				elif elem.tag == 'definingRoles':
					defining_roles=list(elem)

					defining_name = 'NO VALUE'
					defining_val = 'NO VALUE'

					for role in defining_roles:
						if role.tag == 'role':
							role_list = list(role)
							for role_item in role_list: 
								if role_item.tag == 'name':
									defining_name = lookupRole(role_item.text)
								elif role_item.tag == 'value':
									defining_val = lookupRole(role_item.text)
									role_properties[defining_name] = defining_val
									defining_name = 'NO VALUE'
									defining_val = 'NO VALUE'					
				elif elem.tag == 'properties':
					properties = list(elem)
					if kind_text == 'DRUG_KIND':
						ndfrt_file.write('\n------PROPERTIES------\n')
					propName = 'NO VALUE'
					val = 'NO VALUE'
					
					for props in properties:
						if props.tag == 'property':
							theProps = list(props)
							
							for prop in theProps:
								if prop.tag == 'name':
									propName = lookupRole(prop.text)
								elif prop.tag == 'value':
									val = lookupRole(prop.text)
									if kind_text == 'DRUG_KIND':
										ndfrt_file.write('-------------------------------------' + name + '-------------------------------------\n\n')
										ndfrt_file.write('Code: ' + code + '\n')
										ndfrt_file.write('Med ID: ' + med_id + '\n')
										ndfrt_file.write('Kind: ' + kind_text + '\n')
										ndfrt_file.write(propName + ': ' + val + '\n')
										if len(role_properties) > 0:
											ndfrt_file.write('\n-----[DEFINING ROLES] ------\n')
										for r in role_properties:
											if kind_text == 'DRUG_KIND':
												ndfrt_file.write (r + ': ' + role_properties[r] + '\n')

										if propName == 'FDA_UNII':
											if val in fda_unii:
												fda_count = int(fda_unii[val])
												fda_count = fda_count + 1
												fda_unii[val] = str(fda_count)
										else:
											fda_unii[val] = '1'


									if propName != '' and val != '':
										if propName == 'Level':
											level = val
										item_properties[propName] = val

									
									propName = 'NO VALUE'
									val = 'NO VALUE'
				elif elem.tag == 'associations':
					associations = list(elem)
					if kind_text == 'DRUG_KIND':
						ndfrt_file.write('\n------ASSOCIATION------\n')
					for assoc in associations:
						if assoc.tag == 'association':
							assoc_items = list(assoc)
							name_assoc = 'NONE'
							value_assoc = 'NONE'

							for assoc_item in assoc_items:
								if assoc_item.tag == 'name':
									name_assoc = lookupRole(assoc_item.text)
								elif assoc_item.tag == 'value':
									value_assoc = assoc_item.text
									name_convert = lookupRole(name_assoc)
									value_convert = lookupRole(value_assoc)
									if kind_text == 'DRUG_KIND':
										ndfrt_file.write ('[A] '+ name_convert + ': ' + value_convert  + '\n')
									name_assoc = 'NONE'
									value_assoc = 'NONE'
								elif assoc_item.tag == 'qualifiers':
									qualifiers = list(assoc_item)
									for qual in qualifiers:

										q = list(qual)
										q_name = 'NONE'
										q_val = 'NONE'

										for qq in q:
											if qq.tag == 'name':
												q_name = lookupRole(qq.text)
											elif qq.tag == 'value':
												q_val = lookupRole(qq.text)
												if kind_text == 'DRUG_KIND':
													ndfrt_file.write('  --[Q] ' + q_name + ' --[V] ' + q_val + '\n')
												q_name = 'NONE'
												q_val = 'NONE'



			propObj = NDFElement(name,code,med_id,level,kind,item_properties,role_properties,concept_properties)
			propObj.add_roles_concepts(role_properties, concept_properties)
			##print ('*******************************************************************************************')
			##print (propObj.name)
			##print (propObj.kind)
			##print ('*******************************************************************************************')


			##print ('PROPERTIES')
			##print ('---------------')
			##for prop in propObj.properties:
			##	print (prop + ': ' + propObj.properties[prop])

			##print ('ROLES')
			##print ('---------------')
			##for role in propObj.role_properties:
			##	print (role + ': ' + propObj.role_properties[role])

			##print ('CONCEPTS')
			##print ('---------------')
			##for concept in propObj.concept_properties:
			##	print (concept + ': ' + propObj.concept_properties[concept])


			drug_kinds[propObj.code] = propObj
			NDF_term_objects.append(propObj)

			if propObj.rxcui != None and propObj.level != None and propObj.level  != 'VA Class':
				if propObj.rxcui in NDF_rxcui_dict:
					ndf_array = NDF_rxcui_dict[propObj.rxcui]
					ndf_array.append(propObj)
					NDF_rxcui_dict[propObj.rxcui] = ndf_array
				else:
					ndf_array = []
					ndf_array.append(propObj)
					NDF_rxcui_dict[propObj.rxcui] = ndf_array

			if propObj.level == 'None':
				if propObj.kind == 'DISEASE':
					disease_kinds[propObj.code] = propObj
				elif propObj.kind == 'PHYSIOLOGICAL_EFFECT':
					physiological_kinds[propObj.code] = propObj
				elif propObj.kind == 'THERAPEUTIC':
					therapeutic_kinds[propObj.code] = propObj
				elif propObj.kind == 'DOSE':
					dose_kinds[propObj.code] = propObj
				elif propObj.kind == 'MECHANISM_OF_ACTION':
					mechanism_of_action_kinds[propObj.code] = propObj
				elif propObj.kind == 'PHARMACOKINETICS':
					pharmacokinetics_kinds[propObj.code] = propObj
				elif propObj.kind == 'INGREDIENT':
					ingredient_kinds[propObj.code]= propObj

			elif propObj.level  == 'VA Class':
				ndf_va_class_level[propObj.code] = propObj

			elif propObj.level == 'Ingredient':
				ndf_ingredient_level[propObj.code] = propObj

			elif propObj.level == 'VA Product':
				ndf_product_level[propObj.code] = propObj



	for child in root:
		level = ''
		kind = ''
		name = ''
		local_code_id = ''
		local_name = ''
		kind_convert = ''

		prop_dict = {}

		for elem in child:	
			if elem.tag == 'name':
				name = elem.text
				local_name = name
			elif elem.tag == 'kind':
				kind = elem.text
				kind_convert = lookupRole(kind)
			elif elem.tag == 'code':
				codeID = elem.text
				definitions_all[codeID] = name
				local_code_id = codeID
				name = ''
				codeID = ''
			elif elem.tag == 'properties':
				properties = list(elem)
				for props in properties:
					if props.tag == 'property':
						theProps = list(props)
						for prop in theProps:
							if prop.tag == 'name':
								propName = lookupRole(prop.text)
							elif prop.tag == 'value':
								val = lookupRole(prop.text)

								prop_key = str(propName)
								##print ('Prop name: ' + propName + ', Val: ' + val)
								prop_dict[prop_key] = str(val)
								if propName == 'Level' and val == 'VA Product':
									level = 'VA Product'

		##print (local_name + ' --> ' + local_code_id + ' ' + kind + ' '  +level)

		if kind_convert == 'DRUG_KIND':
			ndf_drug_file.write('----------------------\nName: ' + local_name + ' --> ' + local_code_id + '\n      Kind: ' + kind_convert+ '\n      Level:'  +level + '\n')
			for prop in prop_dict:
				ndf_drug_file.write('Prop: ' + prop + ' --> ' + prop_dict[prop] + '\n')
		elif kind_convert == 'MECHANISM_OF_ACTION_KIND':
			ndf_moa_file.write('----------------------\nName: ' + local_name + ' --> ' + local_code_id + '\n      Kind: ' + kind_convert+ '\n      Level:'  +level + '\n')
			for prop in prop_dict:
				ndf_moa_file.write('Prop: ' + prop + ' --> ' + prop_dict[prop] + '\n')
		elif kind_convert == 'INGREDIENT_KIND':
			ndf_ingredient_file.write('----------------------\nName: ' + local_name + ' --> ' + local_code_id + '\n      Kind: ' + kind_convert+ '\n      Level:'  +level + '\n')
			for prop in prop_dict:
				ndf_ingredient_file.write('Prop: ' + prop + ' --> ' + prop_dict[prop] + '\n')
		elif kind_convert == 'DISEASE_KIND':
			ndf_disease_file.write('----------------------\nName: ' + local_name + ' --> ' + local_code_id + '\n      Kind: ' + kind_convert+ '\n      Level:'  +level + '\n')
			for prop in prop_dict:
				ndf_disease_file.write('Prop: ' + prop + ' --> ' + prop_dict[prop] + '\n')
		ndf_file_definitions.write('----------------------\nName: ' + local_name + ' --> ' + local_code_id + '\n      Kind: ' + kind_convert+ '\n      Level:'  +level + '\n')



	##print ('--------------------------PRODUCTS--------------------------')

	prod_level_keys = ndf_product_level.keys()
	for key in prod_level_keys:
		prodobj = ndf_product_level[key]
		print ('--------------------------')
		print (str(prodobj.name))
		print (str(prodobj.kind))

	##print ('\n\n\n\n\n\n\n\n\n\n\n\n--------------------------INGREDIENTS--------------------------')
	ingredient_level_keys = ndf_ingredient_level.keys()
	for key in ingredient_level_keys:
		prodobj = ndf_ingredient_level[key]
		print ('--------------------------')
		print (str(prodobj.name))
		print (str(prodobj.kind))

	##print ('\n\n\n\n\n\n\n\n\n\n\n\n--------------------------VA CLASS--------------------------')
	va_level_keys = ndf_va_class_level.keys()
	for key in ndf_va_class_level:
		prodobj = ndf_va_class_level[key]
		print ('--------------------------')
		print (str(prodobj.name))
		print (str(prodobj.kind))
	

	rx_cui_ndf_keys = NDF_rxcui_dict.keys()

	for key in rx_cui_ndf_keys:
		ndf_elem_array = NDF_rxcui_dict[key]
		ndf_array_copy = []
		for NDF_element in ndf_elem_array:
			for concept in NDF_element.concepts:
				if concept in ndf_va_class_level:
					ndf_concept_match = ndf_va_class_level[concept]
					NDF_element.concepts[concept] = ndf_concept_match.name
			ndf_array_copy.append(NDF_element)
		NDF_rxcui_dict[key] = ndf_array_copy

def lookupRole(term):
	if term in definitions_all:
		defining_val = definitions_all[term]
		return defining_val
	else:
		return term

def writeDefinitions():
	ndfrt_meta.write('Property Definitions\n\n')
	for pDef in ndf_property_definition:
		ndfrt_meta.write(pDef + ': ' + ndf_property_definition[pDef] + '\n')
	
	ndfrt_meta.write('\nRole Definitions\n\n')
	for rDef in ndf_role_definition:
		ndfrt_meta.write(rDef + ': ' + ndf_role_definition[rDef] + '\n')

	ndfrt_meta.write('\nKind Definitions\n\n')
	for kDef in ndf_kind_definition:
		ndfrt_meta.write(kDef + ': ' + ndf_kind_definition[kDef] + '\n')

	ndfrt_meta.write('\nAssociation Definitions\n\n')
	for assocDef in ndf_association_definition:
		ndfrt_meta.write(assocDef + ': ' + ndf_association_definition[assocDef]+'\n')

	ndfrt_meta.write('\nQualifier Definitions\n\n')
	for qualDef in ndf_qualifier_definition:
		ndfrt_meta.write(qualDef + ': ' + ndf_qualifier_definition[qualDef] + '\n')

def convertPropCodeToText(code_number):
	if code_number in ndf_property_definition:
		code_text = ndf_property_definition[code_number]
		return code_text
	elif code_number in ndf_role_definition:
		code_text = ndf_role_definition[code_number]
		return code_text
	elif code_number in ndf_association_definition:
		code_text = ndf_association_definition[code_number]
		code_text = code_text
		return code_text
	elif code_number in ndf_qualifier_definition:
		code_text = ndf_qualifier_definition[code_number]
		code_text = code_text 
		return code_text		
	elif code_number in ndf_kind_definition:
		code_text = ndf_kind_definition[code_number]
	else:
		return code_number

def parse_out_ndf_global_property_def(root):
	for child in root:
		if child.tag == 'propertyDef' or child.tag == 'roleDef' or child.tag == 'kindDef' or child.tag == 'associationDef' or child.tag == 'qualifierDef':
			meta = child.getchildren()
			code_key = ''
			name_key = ''
			for meta_item in meta:
				if meta_item.tag == 'name':
					name_key = meta_item.text
				elif meta_item.tag == 'code':
					code_key = meta_item.text
			if child.tag == 'propertyDef':
				ndf_property_definition[code_key] = name_key
				ndf_prop_file_def.write(ndf_property_definition[code_key] + ' --> ' + name_key + '\n')
			elif child.tag == 'roleDef':
				ndf_role_definition[code_key] = name_key
				ndf_role_file_def.write(ndf_role_definition[code_key] + ' --> ' + name_key + '\n')
			elif child.tag == 'kindDef':
				ndf_kind_definition[code_key] = name_key
				ndf_kind_file_def.write(ndf_kind_definition[code_key] + ' --> ' + name_key + '\n')
			elif child.tag == 'associationDef':
				ndf_association_definition[code_key] = name_key
				ndf_assoc_file_def.write(ndf_association_definition[code_key] + ' --> ' + name_key + '\n')
			elif child.tag  == 'qualifierDef':
				ndf_qualifier_definition[code_key] = name_key
				ndf_qual_file_def.write(ndf_qualifier_definition[code_key] + ' --> ' + name_key + '\n')
			else:
				ndf_other_file_def.write(code_key + ' --> ' + name_key + '\n')
	
	ndf_prop_file_def.close()
	ndf_role_file_def.close()
	ndf_kind_file_def.close()
	ndf_assoc_file_def.close()
	ndf_qual_file_def.close()
	ndf_other_file_def.close()

	writeDefinitions()

def write_ndf_concept(ndf_obj):
	ndfrt_file.write('\n\n---------------------------------------------------------------')
	print('\n\n---------------------------------------------------------------')
	ndfrt_file.write ('\nName: ' + ndf_obj.name + ' ---> ' + ndf_obj.code + ' [Kind:' +ndf_obj.kind+']\n')
	print ('\nName: ' + ndf_obj.name + ' ---> ' + ndf_obj.code + ' [Kind:' +ndf_obj.kind+']\n')
	ndfrt_file.write('-----------------------------------------------------------------\n')
	ndfrt_file.write('May treat: ' + ndf_obj.treat_mesh_def + '\n')
	ndfrt_file.write('Effect: ' + ndf_obj.physiological_mesh_def + '\n')
	ndfrt_file.write('--------item properties------------\n')
	for item in ndf_obj.properties:
		ndfrt_file.write(item + ',  ' + ndf_obj.properties[item] + '\n')
	for mProp in ndf_obj.med_properties:
		ndfrt_file.write(mProp + ': ' + ndf_obj.med_properties[mProp])
	for r in ndf_obj.roles:
		ndfrt_file.write(r + ',  ' + ndf_obj.roles[r] + '\n')
	for concept in ndf_obj.concepts:
		ndfrt_file.write('CONCEPT: ' + concept + ',  ' + ndf_obj.concepts[concept] + '\n')


read_ndfrt()



##write_ndf_concept()