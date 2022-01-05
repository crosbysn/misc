
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

def debug_check(debug_message, debug_status=debug_status):
	if debug_status == True:
		print(debug_message)
	else:
		pass
def process_json_company(focused_company, qccfield_to_modelfield=qccfield_to_modelfield):

	found_keys = list(focused_company['meta'])
	try:
		company_obj = company.objects.get(backend_string = focused_company['meta']['backend_string'], 企业名称 = focused_company['meta']['企业名称'])
		print("Company matching {} ({}) found, updating existing entry.".format(company_obj.企业名称, company_obj.backend_string))
	except:
		company_obj = company(
			backend_string=focused_company['meta']['backend_string'],
			企业名称 = focused_company['meta']['企业名称'],
			)
		company_obj.save()
		print("No existing company record found, creating for {} ({}.".format(company_obj.企业名称, company_obj.backend_string))
	potential_model_fields = [f.name for f in company._meta.get_fields()]
	for key in found_keys:
		if key != '企业名称':
			if key[len(key)-1] == "\n":
				new_key = key[:len(key)-1]
				focused_company['meta'][new_key] = focused_company['meta'][key]
				focused_company['meta'].pop(key)
				key = new_key
			if key in potential_model_fields:
				setattr(company_obj, key, focused_company['meta'][key])
			else:
				debug_check("Key not found for: {}".format(key))
				if key in figure_fields: # will create duplicates if figure is listed in header information and detail information, need to scrape out duplicates in later step. better to keep extra than potentially lose data 
					debug_check("Adding to figure fields.")
					new_figure_dictionary = {}
					new_figure_dictionary['name'] = focused_company['meta'][key]
					new_figure_dictionary['position'] = key
					focused_company['operators'].append(new_figure_dictionary) 
	company_obj.save()
	try:
		company_obj.index_page_source = focused_company['index_page_source']
		company_obj.save()
	except:
		print("No index page source found, verify file predates recording index_pages.")
	operator_list = focused_company['operators']
	for operator in operator_list:
		try: 
			operator_name 		= operator['name']
			operator_position 	= operator['position']
			operator_id 		= operator['backend_string']
			try:
				operator_obj = individual.objects.get(backend_string=operator_id, name=operator_name)
				debug_check("Found individual matching {}, {}".format(operator_obj.backend_string, operator_obj.name))
			except:
				operator_obj = individual(
					backend_string = operator_id,
					name = operator_name)
				operator_obj.save()
			try:
				position_obj = position.objects.get(position_individual = operator_obj, position_company = company_obj, position_title = operator_position)
				debug_check("Found position matching {}, {}".format(position_obj.position_individual.operator_name, position_obj.position_company.backend_string))

			except:
				position_obj = position(
					position_individual = operator_obj,
					position_company = company_obj,
					position_title = operator_position )
				position_obj.save()

		except:
			if len(operator_name) != 0 :
				unlinked_position_figure_obj = unlinked_position_figure(
					name 				= operator_name,
					position_company  	= company_obj,
					position_title     	= operator_position)

				unlinked_position_figure_obj.save()
				debug_check("{} / {}".format(unlinked_position_figure_obj.name, unlinked_position_figure_obj.position_title))
				debug_check("Operator key is incomplete, info is retained in 'offline_json_raw' attribute of company object and as an 'unlinked_position_figure'.")
			else:
				debug_check("Operator key is majority incomplete, no object created. Info retained in the offline_json_raw element.")
	company_obj.offline_json_raw = focused_company
	company_obj.save()
	relation_field_keys = [f.name for f in company_relation._meta.get_fields()]
	qccfield_to_modelfield = qccfield_to_modelfield
	try:
		qccfield_to_modelfield.pop('Oper')
	except:
		debug_check("No operative found for company.")
	relations_function_list = ['getOwnershipStructure', 'getUltimateBeneficiaryNoPath', 'getEquityInvestment', 'getHoldingCompany']
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
			relation_object.save()


# only preset in the development version, otherwise will pull filenames from directory list function

from datetime import datetime, date
start = datetime.now()
def percentage_done(completed, total, start=start):
	completed = len(completed)
	total = len(total)
	progress = completed/total
	percent_progress = progress * 100 
	print()
	print()
	print()
	print("{}% Company Logs Finished. ({}/{})".format(percent_progress, completed, total))
	current = datetime.now()
	duration = current - start
	duration = duration.total_seconds()
	projected_duration = duration / progress
	projected_duration_minutes = projected_duration/60
	projected_duration_seconds = str(round(projected_duration, 2))
	projected_duration_minutes = str(round(projected_duration_minutes, 2))
	print("Process has taken {} seconds, expected to take another {} seconds ({} minutes).".format(duration, projected_duration_seconds, projected_duration_minutes))
	print()
	print()


single_mode = False
path = "C:\\Users\\Sam\\Documents\\qcc_index\\qcc_index\\"
company_jsons_subfolder_name = input("Input target folder path:")
company_jsons_directory = (os.path.join(path, company_jsons_subfolder_name))
potential_files = os.listdir(company_jsons_directory)
broken_json_filename = 'broken_jsons.txt'
finished_company_list = ['combined_company_json.txt', 'combined_company_json_2021_11_24_23_34_17.txt']
unadded_files = []
broken_json_txt = open(broken_json_filename, "r", encoding='utf-8')
broken_json_json = json.load(broken_json_txt)
for company_file in potential_files:
	if company_file not in finished_company_list and company_file not in list(broken_json_json):
		unadded_files.append(company_file)
if len(unadded_files) > 0:
	target_json = unadded_files[0]
	print("Working on {}, there are {} unprocessed files remaining.".format(target_json, len(unadded_files)))
else:
	target_json = False
	print("No remaining unprocessed files in directory. ")

if target_json != False:
	print()
	print("---Starting Pull---")
	time.sleep(2)
	print()
	try:
		full_file_loc 	= os.path.join(path, company_jsons_subfolder_name, target_json)
		full_file_json = open(full_file_loc, "r", encoding='utf-8')
		full_file_json = json.load(full_file_json)
		focused_company_list = []
		if single_mode == True:
			focused_company = list(full_file_json)[1]
			focused_company_id_list = [focused_company, ]
		else:
			focused_company_id_list = list(full_file_json)[1:]
		print("JSON Loaded Successfully")
		time.sleep(2)
		for company_id in focused_company_id_list:
			focused_company_list.append(full_file_json[company_id])
		for focused_company in focused_company_list:
			process_json_company(focused_company)
		print()
		print("All company IDs processed, file marked as completed.")
	except:
		try:
			broken_json_json[target_json] = focused_company #key paired with last company processed in the case a process breaks partway through, else pairs filename
			print("Process failed at company: {}".format(focused_company))
		except:
			broken_json_json[target_json] = target_json
			print("Process failed, JSON is broken. Marking as broken and terminating process.")
		with open(broken_json_filename, 'w', encoding='utf-8') as broken_json_file:
			json.dump(broken_json_file, broken_json_json, ensure_ascii=False)

