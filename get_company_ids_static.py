
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
import time
import hashlib
#import chinese_converter

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report

from functions.models import index_pages
from functions.views import function_field_dictionary, qccfield_to_modelfield

from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

#from proxy_request_dynamic import proxy_request
from new_proxy_tester import proxy_request

# variable setting #

overwrite_data_toggle = True


def get_ids(active_region=False):
	error_understood = False
	company_id_list = []
	page_to_index = "https://www.qcc.com{}".format(active_region)
	print(page_to_index)
	res = proxy_request(page_to_index)
	soup = bs4.BeautifulSoup(res, 'html.parser')
	try:
		company_table = soup.find('table', class_="m_srchList")
		company_items = company_table.find_all('tr')
	except:
		try:
			text_to_search = soup.text
			if (text_to_search.find("小查还没找到数据")) != -1:
				print("Pages exhausted for this region, marking as emptied and ending get_id loop.")
				error_understood = True
				active_region = False
		except:
			error_understood = False
	if error_understood == False:		
		for company_item in company_items:
			company_id 	= company_item.find_all('td')
			company_id 	= company_id[1]
			company_id 	= company_id.find("a")
			company_id 	= company_id['href']
			company_id 	= company_id.replace("/firm/", "")
			company_id 	= company_id.replace(".html", "")
			company_id_list.append(company_id)
	return([company_id_list, active_region])


