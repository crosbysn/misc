

import urllib.request
import bs4	
from bs4 import BeautifulSoup, NavigableString
import requests 
import pandas as pd
import openpyxl
import io
def logout(session):
	session.get("https://tradeatlas.com/en/dashboard/logout")
	
def login():	
	login_url = "https://tradeatlas.com/en"
	session =requests.Session()
	login_page = session.get(login_url)
	login_soup = bs4.BeautifulSoup(login_page.text, 'html.parser')
	login_form = login_soup.find('form', class_="px-4 py-3")
	login_token = login_form.find('input', {'name' : '_token'}).get('value')
	login_destination = "https://tradeatlas.com/en/dashboard/login" 
	username 	= "dat.pull@protonmail.com"
	password 	= "crew_kruk6WHAL.rud"
	login_data = {
	       "_token"	: 	login_token,
	       "email"	:	username,
	       "password": 	password,           
	}
	session.post(login_destination, data=login_data)
	return(session)

def search(session, search_type, search_query, data_type, start_date, end_date, country):
	search_string = "https://tradeatlas.com/en/shipments-v2/{}?search={}&query={}&type={}&begin={}&end={}&page=1".format(country, search_type, query, data_type, start_date, end_date)
	search_response = session.get(search_string)
	return [search_string, search_response]

def excelify(download_content):
	file = download_content[0]
	response_filename = download_content[1]
	xlsx = io.BytesIO(file)
	wb = openpyxl.load_workbook(xlsx)
	ws = wb.create_sheet("datasheet")
	output = open('{}.xls'.format(response_filename), 'wb')
	output.write(file)
	output.close()

def download_data(session, search_string):
	download_url 		= search_string + "&download=xls&download-size=10000"
	session.headers.update({
		'accept-encoding': 'gzip, deflate, br',
		'authority': 'tradeatlas.com',
		'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'upgrade-insecure-requests': '1',
		'dnt': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'document',
		'referer': search_string,
		'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
		})
	download_response 	= session.get(download_url)
	download_content 	= download_response.content
	response_filename = download_response.headers['Content-Disposition']
	response_filename = response_filename.replace('''attachment; filename="''',"")
	response_filename = response_filename.replace('"', "")
	# if you want to set the filename based on the search terms used, just add another line here where you set the response_filename to some combination of the search term strings set for the whole file (below)
	return [download_content, response_filename]

search_type_dictionary = {
	"HS Code" : "hs-code",
	"Importer" : "importer-name",
	"Exporter" : "exporter-name",
	"Products" : "product-details",
	"Brand Name" : "brand-name",
}

def full_pipeline(country, search_type, data_type, start_date, end_date):
	print("----Logging in----")
	session = login()
	print()
	print("----Searching----")
	search_object = search(session, search_type, query, data_type, start_date, end_date, country)
	print("----Downloading----")
	download_content = download_data(session, search_object[0])
	print("----Excelifying----")
	excel_file = excelify(download_content)
	print("----Saved as {}----".format(download_content[1]))
	logout(session)

country 	= "all-countries"
search_type = search_type_dictionary['Exporter']
data_type 	= "import" #not sure what that is for, doesn't seem to ever change
start_date 	= "01-01-2015"
end_date 	= "17-11-2021"

print("Enter search query. Current settings are: country={}, search-type={}, and date range of {} to {}.  ".format(country, data_type, start_date, end_date))
query = input("")
full_pipeline(country, search_type, data_type, start_date, end_date)





