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

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report

from functions.models import index_pages, skipped_company
from functions.views import function_field_dictionary, qccfield_to_modelfield, check_individual, proxy_request, remove_fluff, standardize, empty_check, link_individual

from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

from get_company_ids_static import get_ids #function to return index page of companies that hasn't been reviewed yet
from get_company_page import get_company_page
from get_company_backend import get_company_backend
from offline_company_page import get_company_page as offline_company_page
from offline_company_backend import get_company_backend as offline_company_backend
from functions.views import function_field_dictionary, qccfield_to_modelfield
import time
from functions.models import index_pages
from proxy_request_bee import proxy_request as proxy_request_bee
from new_proxy_tester import proxy_request
from qcc_project.settings import subregion_codes
total_count = 0





grandfathered_list = [
"/g_HB_130500", 
"/g_HB_130300", 
"/g_HB_130100", 
"/g_HB_130200", 
"/g_HAIN_469000", 
"/g_HAIN_460200", 
"/g_HAIN_460300", 
"/g_HAIN_460100", 
"/g_HAIN_460400", 
"/g_AH_340600", 
"/g_AH_340500", 
"/g_GZ_522700", 
"/g_GZ_522300", 
"/g_GZ_520200", 
"/g_GZ_520600", 
"/g_GZ_520400", 
"/g_GZ_522600", 
"/g_GZ_520100",
"/g_AH_340100",
"/g_AH_340200",
"/g_AH_340300",
"/g_AH_340500",
"/g_AH_340600",
"/g_AH_340800",
"/g_AH_341800",
"/g_BJ_110116",
"/g_CQ_500110",
"/g_CQ_500153",
"/g_CQ_500241",
"/g_GD_440100",
"/g_GD_441600",
"/g_GD_445200",
"/g_GD_445300",
"/g_GS_620200",
"/g_GX_450100",
"/g_GX_450200",
"/g_GX_450300",
"/g_GX_450400",
"/g_GX_450500",
"/g_GX_450600",
"/g_GX_450700",
"/g_GZ_520100",
"/g_GZ_520200",
"/g_GZ_520300",
"/g_GZ_520400",
"/g_GZ_520600",
"/g_GZ_522300",
"/g_GZ_522600",
"/g_GZ_522700",
"/g_HAIN_460100",
"/g_HAIN_460200",
"/g_HAIN_460300",
"/g_HAIN_460400",
"/g_HAIN_469000",
"/g_HB_130100",
"/g_HB_130200",
"/g_HB_130300",
"/g_HB_130500"]


print(index_pages.objects.filter(checked_out=True).count())
print(index_pages.objects.count())
    