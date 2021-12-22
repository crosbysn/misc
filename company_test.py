
import urllib.request
import bs4	

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from mainsite.models import company, individual

#string_pull = inout("String: ")
string_pull = "92320117MA272EDW0K"
company_obj = company.objects.get(统社会信用代码=string_pull)


print(company_obj.企业名称)
print(company_obj.注册资本万元)