
import urllib.request
import bs4	
#from requests_html import HTMLSession

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

overwrite_data_toggle = True

# see chinese run chcp 936 in cmd 


### test values
backend_string		= "adc555956ce5b91349b5ef351a08534c"
region_primary 		= "JS"
region_secondary 	= "320100"
page 				= "1"

#company_index_page 	= ''' https://www.qcc.com/g_{}_{}_{}'''.format(region_primary, region_secondary, page)


def remove_fluff(input_string, date_check):
	strings_to_remove = [
		'复制',
		'\n',
		'\t',
		'\r',
		'        ',
		'',
	]	
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

def create_company(unified_social_score, company_name_企业名称):
	exist_check_first = 0
	exist_check_second = 0
	exist_check_third = 0
	if unified_social_score != company_empty_string:
		exist_check_first 	= company.objects.filter(统社会信用代码=unified_social_score).count()
	if company_name_企业名称 != company_empty_string:
		exist_check_second 	= company.objects.filter(企业名称=company_name_企业名称).count()

	if exist_check_first == 1:
		new_company = company.objects.filter(统社会信用代码=unified_social_score).first()
		exist_boolean = 1
	elif exist_check_second == 1:
		new_company = company.objects.filter(企业名称=company_name_企业名称).first()
		exist_boolean = 1

	else:
		if len(unified_social_score) > 1 and len(company_name_企业名称) > 1:
			new_company = company(统社会信用代码 = unified_social_score, 企业名称 = company_name_企业名称)
		elif len(unified_social_score) > 1:
			new_company = company(统社会信用代码 = unified_social_score)
		elif len(company_name_企业名称) > 1:
			new_company = company(企业名称 = company_name_企业名称)
		new_company.save()
		exist_boolean = 0
	if exist_boolean == 1:
		print("Company Exists!")
	return new_company

def check_individual(individual_list):
	individual_name = individual_list[0]
	backend_string 	= individual_list[1]
	exist_check 	= individual.objects.filter(name=individual_name, backend_string=backend_string).count()
	if exist_check == 0:
		new_figure = individual(
			name = individual_name,
			backend_string = backend_string)
		new_figure.save()
		exist_boolean = 0
		print("Created page for new individual: {}".format(new_figure.name))
	else:
		new_figure = individual.objects.get(name=individual_name, backend_string=backend_string)
		print("Object for individual ({}) already exists, linking company to existing individual.".format(new_figure.name))
		exist_boolean = 1
	return  

'''
session = HTMLSession()
res = session.get(company_index_page)
soup = bs4.BeautifulSoup(res.html.html, 'html.parser')
company_table = soup.find('table', class_="m_srchList")
company_items = company_table.find_all('tr')
count = 0
company_id_list = []
for company_item in company_items:
	company_id 	= company_item.find_all('td')
	company_id 	= company_id[1]
	company_id 	= company_id.find("a")
	company_id 	= company_id['href']
	company_id 	= company_id.replace("/firm/", "")
	company_id 	= company_id.replace(".html", "")
	#print(company_id)
	count += 1 
	company_id_list.append(company_id)
	#print(count)
'''
company_id_list = ['0b3db80f2b34a612b75139e8f37916d7',]
for backend_string in company_id_list:
	print()
	print("--------")
	print("Parsing page for string: {}".format(backend_string))
	company_page_link 	= '''C:/Users/Sam/Desktop/qcc_project/qcc_company_pages/qcc_20{}.html'''.format(backend_string)

	#session = HTMLSession()
	#res = session.get(company_page_link)
	soup = bs4.BeautifulSoup(company_page_link, 'html.parser')
	print(soup)
	company_div = soup.find('div', class_="company-detail")
	main_data_section 	= company_div.find('section', {"id" : "cominfo"})
	main_data_table 	= main_data_section.find('table', class_='ntable') 
	main_data_rows 		= main_data_table.find_all('tr')
	
	company_data_pairs = {}
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

	for row_pair in row_pairs:
		if row_pair in figure_fields:
			operator_link 		= row_pairs[row_pair].find('a')
			link_target 		= operator_link['href']
			individual_string	= link_target.replace("https://www.qcc.com/pl/", "")
			individual_string 	= individual_string.replace(".htm", "")
			individual_name 	= operator_link.text
			cleaned_row_value 	= [individual_name, individual_string]
		else:
			if row_pair in date_fields:
				date_check = True
			else:
				date_check = False
			cleaned_row_value = remove_fluff(row_pairs[row_pair], date_check)
		if len(cleaned_row_value) != 0:
			if row_pair in company_model_translations:
				company_data_pairs[row_pair] = cleaned_row_value 
			else:
				print("Model is missing field for {} on this company page.".format(row_pair))
		#row_type_field = company._meta.get_field()
	for possible_field in company_model_translations:
		try:
			field_value = company_data_pairs[possible_field]
			#print("{} : {}".format(possible_field, field_value))
		except:
			company_data_pairs[possible_field] = "NULL"
			#print("{} : {}".format(possible_field, company_data_pairs[possible_field]))
	for figure_field in figure_fields:
		try:
			figure_field_rowpair 	= company_data_pairs[figure_field]
			if figure_field_rowpair != "NULL":
				figure_field_type 		= company._meta.get_field(figure_field)	
				figure_field_object 	= check_individual(figure_field_rowpair)
				company_data_pairs[figure_field] = figure_field_object
		except:
			pass

	lengthofstring = (len(company_data_pairs['统社会信用代码']))
	company_object = create_company(company_data_pairs['统社会信用代码'], company_data_pairs['企业名称'])



	for key in company_data_pairs.keys():
		if company_data_pairs[key] != "NULL":
			if overwrite_data_toggle == True:
				setattr(company_object, key, company_data_pairs[key])
			else:
				if len(company_object.model_field) == 0:
					setattr(company_object, key, company_data_pairs[key])
	company_object.save()