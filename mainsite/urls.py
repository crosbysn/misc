from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from . import views
from mainsite import views as core_views

urlpatterns = [
	path('company/<str:company_name>', views.company_detail, name='company_detail'),
	path('search', views.company_search, name='company_search'),
	path('', views.index_page, name='index_homepage'),
    
    ]