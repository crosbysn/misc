
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
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields, subregion_codes
import time
from functions.models import index_pages

for code_page in index_pages.objects.all():
	code_page.delete()
for code_key in subregion_codes:
	for link_key in subregion_codes[code_key]:
		new_region = index_pages(
			index_code = link_key)
		new_region.save()


print(index_pages.objects.all().count())