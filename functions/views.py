from django.shortcuts import render
import requests




# ----- notes and values below this line, mostly scrap but kept in case it is useful later and to prevent losses / having to dig old copies out of repo
function_field_dictionary = {
  'getEquityInvestment'                 : ['KeyNo', 'Name','CompanyCode','EconKind','Percent','PercentTotal','Org','ShouldCapi','StockRightNum','DetailCount','ShortStatus','StockType','InvestType','RegistCapi','Tags','DetailList'],
  'getOwnershipStructure'               : ['KeyNo', 'Name', 'CompanyCode', 'EconKind', 'Percent', 'PercentTotal', 'Org', 'ShouldCapi', 'StockRightNum', 'DetailCount', 'ShortStatus', 'StockType', 'InvestType', 'RegistCapi', 'Tags', 'DetailList'],
  'getHoldingCompany'                   : ['KeyNo', 'Name', 'Percent', 'PercentTotal', 'Org', 'Oper', 'ShortStatus', 'RegistCapi', 'Type', 'EconKind'],  
  'getUltimateBeneficiaryNoPath'        : ['KeyNo', 'Name', 'Percent', 'PercentTotal', 'Org'],
  }

qccfield_to_modelfield = {
  #'KeyNo'         : ,
  #'Name'          : ,      Name and KeyNo tabbed out because they are used in all cases to generate a company object to link 
  'CompanyCode'   : 'company_code',
  'EconKind'      : 'econ_kind',
  'Percent'       : 'percent',
  'PercentTotal'  : 'percent_total',
  'Org'           : 'org',
  'ShouldCapi'    : 'shouldcapi',
  'StockRightNum' : 'stockrightnum',
  'DetailCount'   : 'detailcount',
  'ShortStatus'   : 'shortstatus',
  'StockType'     : 'stocktype',
  'InvestType'    : 'investtype',
  'RegistCapi'    : 'registered_cap',
  #'Tags'          : ,    Tags are also an object of their own that is linked, not directly entered into company / company_relation
  'DetailList'    : 'detaillist', 
  'Oper'          : 'figure_raw_string',
  'Type' 		  : 'type',
}

def proxy_request(target_url):
    s = requests.Session()
    r = s.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'K5UPOMMS2EJLHRDXLS743G02C6GEM4YV0XFEJW8P8JUIEATU9Y5QIJGJKJ2J7XZ2047N1KEDIO3VB465',
            'url': target_url, 
            'render_js': 'false', 
        },
        
    )
    return(r)
def remove_fluff(input_string, date_check):
  strings_to_remove = [
    '复制',
    '\n',
    '\t',
    '\r',
    '        ',
    '',
    ':',
    '：',

  ] 
  if type(input_string) != str:
    input_string = input_string.text
  for string in strings_to_remove:
    input_string = input_string.replace(string, '')
  input_string = input_string.replace("  ", " ")
  string_len   = len(input_string)
  if string_len > 1:
    if input_string[0] == " ":
      input_string = input_string[1:]
  string_len   = len(input_string)
  if string_len > 1:
    if input_string[string_len-1] == " ":
      input_string = input_string[:string_len-1]
  if date_check == True:
    input_string = input_string.replace("一", '-')
  else:
    input_string = input_string.replace("一", '')
    input_string = input_string.replace("-", '')

  return(input_string)
def standardize(input_string):
  input_string = input_string.text
  input_string = input_string.replace("  ", '')
  input_string = input_string.replace(" ", '')
  input_string = input_string.replace("(", '')
  input_string = input_string.replace(")", '')
  input_string = input_string.replace("一", '')

  return input_string
def check_individual(individual_list):
  individual_name = individual_list[0]
  id_string   = individual_list[1]
  exist_check   = individual.objects.filter(name=individual_name, backend_string=id_string).count()
  if exist_check == 0:
    new_figure = individual(
      name = individual_name,
      backend_string = id_string)
    new_figure.save()
    exist_boolean = 0
    print("Created page for new individual: {}".format(new_figure.name))
  else:
    new_figure = individual.objects.get(name=individual_name, backend_string=id_string)
    print("Object for individual ({}) already exists, linking company to existing individual.".format(new_figure.name))
    exist_boolean = 1
  return new_figure
def empty_check(test_key):
  try:
    test_result = type((row_pairs[test_key]))
    result = False
  except:
    result = True
  return result
def link_individual(individual_obj, company_obj, position_str):
  check_position = position.objects.filter(position_individual=individual_obj, position_company=company_obj, position_title=position_str)
  if check_position.count() == 1:
    response_text = "Position already exists"
  elif check_position.count() == 0:
    position_obj = position(
      position_individual=individual_obj, 
      position_company=company_obj, 
      position_title=position_str)
    position_obj.save()
    response_text = "Position created"
  else:
    for position_dup in check_position.all():
      position_dup.delete()
    position_obj = position(
      position_individual=individual_obj, 
      position_company=company_obj, 
      position_title=position_str)
    position_obj.save()
    response_text = "Position duplicates found. Deleted duplicates."
  return response_text