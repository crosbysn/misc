import urllib.request
import bs4	
from requests_html import HTMLSession

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields
import csv
overwrite_data_toggle = True
import time

# see chinese run chcp 936 in cmd 


### test values
backend_string		= "adc555956ce5b91349b5ef351a08534c"
region_primary 		= "JS"
region_secondary 	= "320100"
page_list 				= range(40,250)
company_id_list = []
link_counter = 0


company_file = "qcc_company_pagelist.txt"
for page in page_list:
	if link_counter >= 20:
		print("20 Links pinged, sleeping for 2 minutes")
		time.sleep(120) 
		link_counter = 0
		print("Waking Up")
	link_counter += 1
	page = str(page)
	company_index_page 	= ''' https://www.qcc.com/g_{}_{}_{}'''.format(region_primary, region_secondary, page)
	print(company_index_page)	
	session = HTMLSession()
	res = session.get(company_index_page)
	soup = bs4.BeautifulSoup(res.html.html, 'html.parser')
	company_table = soup.find('table', class_="m_srchList")
	company_items = company_table.find_all('tr')
	count = 0
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
	f = open(company_file,"w+")
	for company_url in company_id_list:
		company_page_link 	= '''https://www.qcc.com/firm/{}.html'''.format(company_url)
		f.write(company_page_link + "\r\n")



