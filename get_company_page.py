
import urllib.request
import bs4	
from requests_html import HTMLSession
from bs4 import BeautifulSoup, NavigableString
import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields
import time
overwrite_data_toggle = True
from proxy_request_dynamic import proxy_request




def remove_fluff(input_string, date_check):
	strings_to_remove = [
		'复制',
		'\n',
		'\t',
		'\r',
		'        ',
		'',
		':',
		'：',

	]	
	if type(input_string) != str:
		input_string = input_string.text
	for string in strings_to_remove:
		input_string = input_string.replace(string, '')
	input_string = input_string.replace("  ", " ")
	string_len 	 = len(input_string)
	if string_len > 1:
		if input_string[0] == " ":
			input_string = input_string[1:]
	string_len 	 = len(input_string)
	if string_len > 1:
		if input_string[string_len-1] == " ":
			input_string = input_string[:string_len-1]
	if date_check == True:
		input_string = input_string.replace("一", '-')
	else:
		input_string = input_string.replace("一", '')
		input_string = input_string.replace("-", '')

	return(input_string)
def standardize(input_string):
	input_string = input_string.text
	input_string = input_string.replace("  ", '')
	input_string = input_string.replace(" ", '')
	input_string = input_string.replace("(", '')
	input_string = input_string.replace(")", '')
	input_string = input_string.replace("一", '')

	return input_string
def check_individual(individual_list):
	individual_name = individual_list[0]
	id_string 	= individual_list[1]
	exist_check 	= individual.objects.filter(name=individual_name, backend_string=id_string).count()
	if exist_check == 0:
		new_figure = individual(
			name = individual_name,
			backend_string = id_string)
		new_figure.save()
		exist_boolean = 0
		print("Created page for new individual: {}".format(new_figure.name))
	else:
		new_figure = individual.objects.get(name=individual_name, backend_string=id_string)
		print("Object for individual ({}) already exists, linking company to existing individual.".format(new_figure.name))
		exist_boolean = 1
	return new_figure
def empty_check(test_key):
	try:
		test_result = type((row_pairs[test_key]))
		result = False
	except:
		result = True
	return result
def link_individual(individual_obj, company_obj, position_str):
	check_position = position.objects.filter(position_individual=individual_obj, position_company=company_obj, position_title=position_str)
	if check_position.count() == 1:
		response_text = "Position already exists"
	elif check_position.count() == 0:
		position_obj = position(
			position_individual=individual_obj, 
			position_company=company_obj, 
			position_title=position_str)
		position_obj.save()
		response_text = "Position created"
	else:
		for position_dup in check_position.all():
			position_dup.delete()
		position_obj = position(
			position_individual=individual_obj, 
			position_company=company_obj, 
			position_title=position_str)
		position_obj.save()
		response_text = "Position duplicates found. Deleted duplicates."
	return response_text
def subsidiary_company_check(company_name):
	company_check = company.objects.filter(企业名称=company_name)
	if company_check.count() == 1:
		parent_company = company_check.first()
	elif company_check.count() >1:
		for company_dup in company_check.all():
			company_dup.error_flag = True
			company_dup.save()
		parent_company = company_check.first()
	elif company_check.count() == 0:
		placeholder_company = company(
			企业名称=company_name)
		placeholder_company.save()
		parent_company = placeholder_company
	return(parent_company)


def get_company_page(id_string):

	print()
	print("--------")
	print("Parsing page for string: {}".format(id_string))
	company_page_link 	= '''https://www.qcc.com/firm/{}.html'''.format(id_string)
	print(company_page_link)
	res = proxy_request(company_page_link)
	soup = bs4.BeautifulSoup(res, 'html.parser')
	company_data_pairs = {}

	basic_info 	= soup.find('div', class_='contact-info')
	basic_info_lines = basic_info.find_all('div', class_="rline")

	delayed_meta_info = {
		'figures' : [],
		'company_info' : {},

	}

	company_name_div 	= soup.find('div', class_="title")
	company_name_div 	= company_name_div.find('h1')
	company_name_inst = remove_fluff(company_name_div, False)
	company_data_pairs['企业名称'] = company_name_inst
	formatted_name = company_data_pairs['企业名称']
	if company_name_inst[0] == " ":
		company_name_inst = company_name_inst[1:]
	if company_name_inst[len(company_name_inst)-1] == " ":
		company_name_inst = company_name_inst[:len(company_name_inst)-1]
	try:
		for basic_info_line in basic_info_lines:
			left_data_pair = basic_info_line.find('span')
			right_data_pair = left_data_pair.find_next_sibling('span')
			
			for data_pair in [left_data_pair, right_data_pair]:
				if data_pair is not None:

					inner_pair_list 	= []
					data_value 			= ''
					data_key 			= ''
					data_key_cleaned 	= ''
					data_value_cleaned  = ''
					
					for element in data_pair:
						if isinstance(element, NavigableString):
							data_key += element
						else: 
							inner_pair_list.append(element)
					data_key = remove_fluff(data_key, False)
					for char in data_key:
						if char.isalnum():
							data_key_cleaned += char

					data_location_found = False
					if data_key_cleaned in figure_fields:
						figure_name_cleaned= ''
						try:
							possible_data_value = data_pair.find_all('a')[0]
							figure_name 	= possible_data_value.text
							figure_link 	= possible_data_value['href']
						except:
							possible_data_value = data_pair.find('span', class_="cont")
							figure_name 	= possible_data_value.text
						for char in figure_name:
							if char.isalnum() or char == "*":
								figure_name_cleaned += char

						figure_id_string			= figure_link.replace("https://www.qcc.com/pl/", "")
						figure_id_string_cleaned 	= figure_id_string.replace(".htm", "")
						
						delayed_meta_info['figures'].append([figure_name_cleaned, figure_id_string_cleaned, data_key_cleaned])

					else:
						for possible_data_value in inner_pair_list:
							if data_location_found == False:
								if len(possible_data_value.text) > 0:
									data_value = possible_data_value.text
									data_location_found = True

						for char in data_value:
							if char.isalnum() or char == "*":
								data_value_cleaned += char
						data_value_cleaned = remove_fluff(data_value_cleaned, False)

					company_data_pairs[data_key_cleaned] = data_value_cleaned
				else:
					pass

		try:

			company_div = soup.find('div', class_="company-detail")
			try:
				main_data_section 	= company_div.find('section', {"id" : "cominfo"})
				main_data_table 	= main_data_section.find('table', class_='ntable') 
				main_data_rows 		= main_data_table.find_all('tr')
			except:
				try:
					main_data_section 	= company_div.find('section', {"id" : "kcbinfo"})
					main_data_table 	= main_data_section.find('table', class_='ntable') 
					main_data_rows 		= main_data_table.find_all('tr')
				except:
					main_data_section 	= company_div.find('section', {"id" : "hkBaseInfo"})
					main_data_table 	= main_data_section.find('table', class_='ntable') 
					main_data_rows 		= main_data_table.find_all('tr')
		except:
			company_div = soup.find('div', class_="company-data")
			try:
				main_data_section 	= company_div.find('div', {"id" : "cominfo"})
				main_data_table 	= main_data_section.find('table', class_='ntable') 
				main_data_rows 		= main_data_table.find_all('tr')
			except:
				try:
					main_data_section 	= company_div.find('div', {"id" : "kcbinfo"})
					main_data_table 	= main_data_section.find('table', class_='ntable') 
					main_data_rows 		= main_data_table.find_all('tr')
				except:
					main_data_section 	= company_div.find('div', {"id" : "hkBaseInfo"})
					main_data_table 	= main_data_section.find('table', class_='ntable') 
					main_data_rows 		= main_data_table.find_all('tr')


		row_pairs = {}
		for data_row in main_data_rows:
			data_columns = data_row.find_all('td')
			data_pairs = (len(data_columns))/2
			if data_pairs == 1 :
				row_pairs[standardize(data_columns[0])] = data_columns[1] 
			elif data_pairs == 2:
				row_pairs[standardize(data_columns[0])] = data_columns[1]
				row_pairs[standardize(data_columns[2])] = data_columns[3]

			elif data_pairs == 3:
				row_pairs[standardize(data_columns[0])] = data_columns[1]
				row_pairs[standardize(data_columns[2])] = data_columns[3]
				row_pairs[standardize(data_columns[4])] = data_columns[5]


	# row_pairs is dictionary with strings of all fields present on page.
		
		meta_info_list 	=  ['企业名称',] 
		try:
			company_obj = company.objects.get(backend_string=id_string,企业名称=formatted_name)
			print("Company with name/string pair {}/{} already exists, updating.".format(formatted_name, id_string))
		except:
			company_obj 	= company(backend_string = id_string, 企业名称 = formatted_name)
			company_obj.save()
			print("Company with name/string pair {}/{} not present, created object.".format(formatted_name, id_string))
		for row_pair in row_pairs:
			if row_pair in meta_info_list:
				pass
			elif row_pair in figure_fields:
				operator_link 		= row_pairs[row_pair].find('a')
				link_target 		= operator_link['href']
				individual_string	= link_target.replace("https://www.qcc.com/pl/", "")
				individual_string 	= individual_string.replace(".htm", "")
				individual_name 	= operator_link.text
				individual_obj 		= check_individual([individual_name, individual_string])
				linked_individual = (link_individual(individual_obj, company_obj, row_pair))
			else:
				if row_pair in date_fields:
					date_check = True
				else:
					date_check = False
				cleaned_row_value = remove_fluff(row_pairs[row_pair], date_check)
				company_data_pairs[row_pair] = cleaned_row_value
		company_data_pairs['backend_string'] = id_string

		for key in company_data_pairs.keys():
			setattr(company_obj, key, company_data_pairs[key])
			company_obj.save()

		# for now delayed_meta_info only contains an entry for figure, so I just skip directly to it, but leaving it as a dictionary entry in case other items need to be held similarly
		for individual_pair in delayed_meta_info['figures']:
			individual_obj 		= check_individual([individual_pair[0], individual_pair[1]])
			print(link_individual(individual_obj, company_obj, individual_pair[2]))
	except:
		try:
			company_obj = company.objects.get(backend_string=id_string,企业名称=formatted_name)
			print("Company with name/string pair {}/{} already exists, updating error flag.".format(formatted_name, id_string))
		except:
			company_obj 	= company(backend_string = id_string, 企业名称 = formatted_name)
			company_obj.save()
			print("Company with name/string pair {}/{} not present, created basic object with error flag.".format(formatted_name, id_string))
		company_obj.error_flag = True
		company_obj.save()
