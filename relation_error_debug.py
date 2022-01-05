
import urllib.request
import bs4	
from requests_html import HTMLSession
from bs4 import BeautifulSoup, NavigableString
import requests
import time
import hashlib
#import chinese_converter
import sys
import eventlet
if sys.version_info[0]==2:
	import six
	from six.moves.urllib import request
if sys.version_info[0]==3:
	from eventlet.green.urllib import request
import random
import socket
import os
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report, unlinked_position_figure

from functions.models import index_pages, skipped_company
from functions.views import function_field_dictionary, qccfield_to_modelfield, check_individual, proxy_request, remove_fluff, standardize, empty_check, link_individual

from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

from functions.views import function_field_dictionary, qccfield_to_modelfield
import time
from functions.models import index_pages
from qcc_project.settings import subregion_codes
total_count = 0
debug_status = False

import json
def remove_currency_characters(target_dictionary):
	currency_field_list = [
	'ShouldCapi',
	'RegistCapi',
	]
	remove_dictionary = {
		'万元人民币' : '000',
		'万元'      : '000',
		'萬元'      : '000000',
		'亿元'      : '000000000',
		'人民幣'  : '',
		'元'      : ',',
		}
	for currency_field in currency_field_list:
		try:
			output_variable = target_dictionary[currency_field]
			for remove_target in list(remove_dictionary):
				output_variable = output_variable.replace(remove_target, remove_dictionary[remove_target])
			try:
				output_variable = float(output_variable)  
				target_dictionary[currency_field] = output_variable
			except:
				try:
					target_dictionary.pop(currency_field)
				except:
					pass
		except:
			pass
	return(target_dictionary)


broken_relation_test_loc = "broken_relation_testfile.txt"
broken_json_txt = open(broken_relation_test_loc, "r", encoding='utf-8')
broken_json_json = json.load(broken_json_txt)
focused_company = broken_json_json
relations_function_list = ['getOwnershipStructure', 'getUltimateBeneficiaryNoPath', 'getEquityInvestment', 'getHoldingCompany']

# ONLY FOR DEBUG REMOVE BELOW THIS FOR GOD SAKE 

company_obj = company.objects.first()

# ONLY FOR DEBUG REMOVE ABOVE THIS FOR GOD SAKE 
 

for relation_type in relations_function_list:
	print(relation_type)
	for company_key in list(focused_company[relation_type])[1:]:
		try:
			focused_relation = focused_company[relation_type][company_key]['raw']
			depreceated_structure = False
			target_company_id = focused_company['KeyNo']
			target_company_name = focused_company['Name']
		except:
			focused_relation = focused_company[relation_type][company_key]
			depreceated_structure = True
			target_company_id = company_key
			target_company_name = focused_relation['name']



		relation_object = company_relation(
			relation_type = relation_type,
			origin_company = company_obj,
			original_response = focused_relation,
			)
		
		try:
			target_company = company.objects.get(backend_string=target_company_id, 企业名称=target_company_name)
			print("Company exists to link with relation company ({} ({})".format(target_company.backend_string, target_company.企业名称))
		except:
			target_company = company(
				backend_string=target_company_id, 
				企业名称=target_company_name
				)
			
			print("Company created to link with relation company ({} ({})".format(target_company.backend_string, target_company.企业名称))
		relation_object.target_company = target_company


		focused_relation = remove_currency_characters(focused_relation)
		for percent_key in ['Percent', 'PercentTotal']:
			if percent_key in list(focused_relation):
				if type(focused_relation[percent_key]) != float or int:
					if len(focused_relation[percent_key]) != 0: #do not trunacte to an if ~ and statement, len of key depends on key existing
						focused_relation[percent_key] = float((focused_relation[percent_key].replace("%", "")))
		try:
			if len(focused_relation['Tags']) > 0:
				relation_object.tags_raw = focused_relation['Tags']
			focused_relation.pop('Tags')
		except:
			try: 
				if len(focused_relation['tags']) > 0:
					relation_object.tags_raw = focused_relation['tags']
				focused_relation.pop('tags')
			except:
				pass

		if depreceated_structure == False:
			for key in list(qccfield_to_modelfield):
				try: 
					if type(focused_relation[key]) == float or int: 
						print("{} saved for key '{}'".format(focused_relation[key], qccfield_to_modelfield[key]))
						setattr(relation_object, qccfield_to_modelfield[key], focused_relation[key])
					elif len(focused_relation[key]) > 0:
						print("{} saved for key '{}'".format(focused_relation[key], qccfield_to_modelfield[key]))
						setattr(relation_object, qccfield_to_modelfield[key], focused_relation[key])
					else:
						print("Empty field in relation for {}".format(key))
				except:
					print("No entry in relation for {}.".format(key))
		if depreceated_structure == True:
			for key in list(focused_relation):
				if type(focused_relation[key]) == float or int:
					print("{} saved for key '{}'".format(focused_relation[key], key))
					setattr(relation_object, key, focused_relation[key])

				elif len(focused_relation[key]) > 0:
					print("{} saved for key '{}'".format(focused_relation[key], key))
					setattr(relation_object, key, focused_relation[key])

		relation_object_check = company_relation.objects.filter(relation_type=relation_type, origin_company=company_obj, target_company=target_company).all()
		if len(relation_object_check) == 1:
			print("Relation duplicate exists, replacing with current relation information.")
			relation_object_check.delete()
		elif len(relation_object_check) > 1:
			print("Multiple duplicate relations existed, potential substantial error.")
			for relation_dup in relation_object_check:
				relation_dup.delete()