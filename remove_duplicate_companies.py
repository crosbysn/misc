
import urllib.request
import bs4	

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from mainsite.models import company, individual, company_relation

for ping_company in company.objects.all():
	ping_string = ping_company.backend_string
	duplicate_check = company.objects.filter(backend_string=ping_string).all()
	if duplicate_check.count() > 1:
		duplicate_list = duplicate_check[:1]
		for duplicate in duplicate_list:
			duplicate.delete()
			print("Removed duplicate for {}".format(ping_string))