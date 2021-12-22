from requests_html import HTMLSession
import requests
import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report, figure_relation
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields
import hashlib
#import chinese_converter
from functions.views import function_field_dictionary, qccfield_to_modelfield


from proxy_request_dynamic import proxy_request


def get_company_backend(firm_string):
  multiple_pull_mode = False #set to true if you want to itterate through several. Leaving this in case bulk / error fixing pulls are needed later. 
  query_list = []
  def remove_currency_characters(target_dictionary):
    currency_field_list = [
    'ShouldCapi',
    'RegistCapi',
    ]
    remove_dictionary = {
      '万元人民币' : '000',
      '万元'      : '000',
      '萬元'      : '000000',
      '亿元'      : '000000000',
      '人民幣'  : '',
      '元'      : ',',
    }
    for currency_field in currency_field_list:
        try:
          output_variable = target_dictionary[currency_field]
          for remove_target in list(remove_dictionary):
            output_variable = output_variable.replace(remove_target, remove_dictionary[remove_target])
          try:
            output_variable = float(output_variable)  
            target_dictionary[currency_field] = output_variable
          except:
            try:
              target_dictionary.pop(currency_field)
            except:
              pass
        except:
          pass
    return(target_dictionary)
  total_relations = 0
  origin_company = company.objects.filter(backend_string=firm_string).all()[0]

  function_options = {
   'getOwnershipStructure'              : 'https://www.qcc.com/api/charts/getOwnershipStructure', 
   'getUltimateBeneficiaryNoPath'       : 'https://www.qcc.com/api/charts/getUltimateBeneficiaryNoPath',  
   'getEquityInvestment'              : 'https://www.qcc.com/api/charts/getEquityInvestment',
   'getHoldingCompany'                  : 'https://www.qcc.com/api/charts/getHoldingCompany',  
   #'getEnterpriseOverview'              : 'https://www.qcc.com/api/charts/getEnterpriseOverview',  
   #'getSuspectedActualControllerNoPath' : 'https://www.qcc.com/api/charts/getSuspectedActualControllerNoPath',
   }  
  company_relation_dict = {
    'getOwnershipStructure'             : 'Parent Company',
    'getEquityInvestment'               : 'Child Company',
    'getUltimateBeneficiaryNoPath'      : 'Ultimate Beneficiary',
    'getHoldingCompany'                 : 'Holding Company',
    }
  response_key = {
    'getOwnershipStructure'             : 'EquityShareDetail',
    'getEquityInvestment'               : 'EquityShareDetail',
    'getUltimateBeneficiaryNoPath'      : 'Names',
    'getHoldingCompany'                 : 'Names',
    #'getSuspectedActualControllerNoPath': 'ControllerData',
    #'getEnterpriseOverview'             : 'Oper',}
    }

  for function in list(response_key):
    function_fields = function_field_dictionary[function]
    url = (function_options[function])
    response = proxy_request(url, firm_string)
    if json.loads(response)['Status'] == 200:
      error_status = False
    else:
      new_error = error_report(
        model_type  = "company_relation",
        model_inst  = firm_string,
        error_type  = "RELATION_PULL_ERROR",
        text        = json.loads(response)['Status'])
      print(new_error.model_type)
      print(new_error.model_inst)
      print(new_error.error_type)
      print(new_error.text)
      new_error.save()
      error_status = True
    if error_status == True:
      print("Error occured ({}/{}), report filed. Moving to next company.".format(new_error.error_type, new_error.text))
    else:
      response_payload   = json.loads(response)['Result']
      response_lookup_value = response_key[function]
      company_list  = response_payload[response_lookup_value]
      list_len = len(company_list)
      list_pos = 0
      print()
      print("---{}---".format(function))
      first_key = list(company_list[0])[0]
      try:
        force_compute_value = (company_list[0][first_key])
        print("Function returned {} entities. Debugcheck returned first company with ID: {}.".format(list_len, force_compute_value))
        function_pull_possible = True
      except:
        function_pull_possible = False
      if function_pull_possible == False:
        print("No returnable values for {} using {}. Creating error report with type 'CHART_FUNCTION'".format(origin_company.企业名称, function))
        new_error = error_report(
            model_type    = 'company',
            model_inst    = firm_string,
            error_type    = 'CHART_FUNCTION',
            text          = response)
        new_error.save()
        origin_company.relations_check = True
        company_inst.save()
      else:
        for result_item in company_list:
          if function != "getUltimateBeneficiaryNoPath":
            list_pos += 1
            company_results_dict = {}
            company_results_dict_cleaned = {}
            company_results_keys = list(result_item)
            for function_key in function_fields:
              if function_key in company_results_keys:
                if len(str(result_item[function_key])) > 0:
                  company_results_dict[function_key] = result_item[function_key]
            for key in company_results_dict:
              if type(company_results_dict[key]) == str:
                company_results_dict_cleaned[key] = company_results_dict[key]
                
                #standardized_string = chinese_converter.to_simplified(company_results_dict[key])
                #company_results_dict_cleaned[key] = standardized_string
              else:
                company_results_dict_cleaned[key] = company_results_dict[key]
            company_results_dict = company_results_dict_cleaned        
            for percent_key in ['Percent', 'PercentTotal']:
              if percent_key in list(company_results_dict):
                company_results_dict[percent_key] = float((company_results_dict[percent_key].replace("%", "")))
            company_results_dict = remove_currency_characters(company_results_dict)
            try:
              linked_company = company.objects.get(backend_string = firm_string, 企业名称 = company_results_dict['Name'])
              company_found = True
            except:
              linked_company = company(
                backend_string = firm_string,
                企业名称 = company_results_dict['Name'],
                placeholder = True,
                )
              linked_company.save()
              company_found = False
            if company_found == True:
              link_message = "Company exists to link!"
            else:
              link_message = "Company did not exist, creating and linking!"
            print("{}/{}. {}".format(list_pos, list_len, link_message))
            for existing_relation in company_relation.objects.filter(relation_type=function,origin_company=origin_company,target_company=linked_company).all():
              existing_relation.delete()

            relation_inst = company_relation(
              relation_type   = company_relation_dict[function],
              origin_company  = origin_company,
              target_company   = linked_company)
            relation_inst.save()
            total_relations += 1
            try:
              company_results_dict.pop('KeyNo')
            except:
              pass
            company_results_dict.pop('Name')
            if 'Tags' in function_fields:
              for tag in company_results_dict['Tags']:
                #tag_name = chinese_converter.to_simplified(tag['Name'])
                tag_name = tag['Name']
                tag_inst = relation_tag_sub(
                  type_tag              = tag['Type'],
                  name                  = tag_name,
                  original_response     = tag
                  )
                tag_inst.save()
                relation_inst.tags.add(tag_inst)
                relation_inst.save()
              company_results_dict.pop('Tags')  
            for key in list(company_results_dict):
              print("{} : {}".format(key, company_results_dict[key]))
              setattr(relation_inst, qccfield_to_modelfield[key], company_results_dict[key])
              relation_inst.save()
          else:
            list_pos += 1
            company_results_dict = {}
            company_results_dict_cleaned = {}
            company_results_keys = list(result_item)
            for function_key in function_fields:
              if function_key in company_results_keys:
                if len(str(result_item[function_key])) > 0:
                  company_results_dict[function_key] = result_item[function_key]
            for key in company_results_dict:
              if type(company_results_dict[key]) == str:
                #standardized_string = chinese_converter.to_simplified(company_results_dict[key])
                #company_results_dict_cleaned[key] = standardized_string
                company_results_dict_cleaned[key] = company_results_dict[key]
              else:
                company_results_dict_cleaned[key] = company_results_dict[key]
            company_results_dict = company_results_dict_cleaned        
            for percent_key in ['Percent', 'PercentTotal']:
              if percent_key in list(company_results_dict):
                company_results_dict[percent_key] = float((company_results_dict[percent_key].replace("%", "")))
            company_results_dict = remove_currency_characters(company_results_dict)
            try:
              linked_figure = individual.figure_relation.get(backend_string = firm_string, name = company_results_dict['Name'])
              company_found = True
            except:
              linked_figure = individual(
                backend_string = firm_string,
                name = company_results_dict['Name'],
                )
              linked_figure.save()
              company_found = False
            if company_found == True:
              link_message = "Figure exists to link!"
            else:
              link_message = "Figure did not exist, creating and linking!"
            print("{}/{}. {}".format(list_pos, list_len, link_message))
            for existing_relation in figure_relation.objects.filter(relation_type=function,origin_company=origin_company,target_figure=linked_figure).all():
              existing_relation.delete()

            relation_inst = figure_relation(
              relation_type   = company_relation_dict[function],
              origin_company  = origin_company,
              target_figure   = linked_figure)
            relation_inst.save()
            total_relations += 1
            try:
              company_results_dict.pop('KeyNo')
            except:
              pass
            company_results_dict.pop('Name')
            if 'Tags' in function_fields:
              for tag in company_results_dict['Tags']:
                #tag_name = chinese_converter.to_simplified(tag['Name'])
                tag_name = tag['Name']
                tag_inst = relation_tag_sub(
                  type_tag              = tag['Type'],
                  name                  = tag_name,
                  original_response     = tag
                  )
                tag_inst.save()
                relation_inst.tags.add(tag_inst)
                relation_inst.save()
              company_results_dict.pop('Tags')  
            for key in list(company_results_dict):
              print("{} : {}".format(key, company_results_dict[key]))
              setattr(relation_inst, qccfield_to_modelfield[key], company_results_dict[key])
              relation_inst.save()



  print("Company has a total of {} recorded relationships vs. {} recieved in this pull.".format(total_relations, company_relation.objects.filter(origin_company=origin_company).count()))
  origin_company.relations_check = True
  origin_company.save()










