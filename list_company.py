
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

# see chinese run chcp 936 in cmd 

test_company = company.objects.get(backend_string='f625a5b661058ba5082ca508f99ffe1b', 企业名称="企查查科技有限公司")
print(test_company)
print(test_company.get_absolute_url())