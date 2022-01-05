from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import strip_tags
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.core.paginator import Paginator 
import django.contrib.sessions
from qcc_project.settings import company_field_names, searchform_null
from mainsite.models import company, individual, position,company_relation

link_text = '''https://uploads-ssl.webflow.com/6101e896e784d553fe534908/css/china-nlp.webflow.9eb1fed3c.css'''


def company_detail(request, company_name):
	company_object 		= company.objects.get(企业名称__icontains=company_name)
	related_positions 	= position.objects.filter(position_company=company_object).all()
	company_links 		= company_relation.objects.filter(origin_company=company_object).all()
	company_links_target= company_relation.objects.filter(target_company=company_object).all()

	context = {
		'company_links' 	: company_links,
		'related_positions' : related_positions,
		'company_object' 	: company_object,
		'style_sheet'       : link_text,
		'company_field_names' : company_field_names,

	}
	return render(request, 'company_detail.html', context)

def index_page(request):
	context = {
		'style_sheet'       : link_text,
	}
	return render(request, 'index.html', context)

def company_search(request):
	if request.method == "POST":
		query_construction = company.objects.all()
		
		search_variables = ['企业名称__icontains', 'backend_string', '英文名__icontains'] 
		search_codex	= {} 	
		for search_variable in search_variables:
			if type(request.POST.get(search_variable)) is not None:
				if len(request.POST.get(search_variable)) != 0 and request.POST.get(search_variable) != searchform_null:
					search_codex[search_variable] = request.POST.get(search_variable)   
		for key in list(search_codex):
			query_construction = query_construction.filter(**{key: search_codex[key]})
			print("Added query constraint {} = {}".format(key, search_codex[key]))
		search_results = query_construction.all()

				

	context = {
		'style_sheet'       : link_text,
		'result_item_list' 	: search_results,
	}
	return render(request, 'search_results.html', context)