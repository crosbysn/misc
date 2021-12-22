from django.db import models
from django.urls import reverse

company_model_translations = {
	'统社会信用代码' 		: 	'Unified Social Credit Code',
	'企业名称'			: 	'Company Name',
	'法定代表人'			: 	'Legal Representative',
	'登记状态'			: 	'Registration status',
	'成立日期'			: 	'Date of establishment',
	'注册资本'			: 	'Registered capital',
	'实缴资本'			: 	'Paid-in capital',
	'核准日期'			: 	'Approved date',
	'组织机构代码' 		: 	'Organization Code',
	'工商注册号'			: 	'Business Registration Number',
	'纳税人识别号'		: 	'Taxpayer Identification Number	',
	'企业类型'			: 	'Type of enterprise',
	'营业期限'			: 	'Operating period',
	'纳税人资质'			: 	'Taxpayer qualification',
	'所属行业'			: 	'Industry',
	'所属地区'			: 	'District belong to	',
	'登记机关'			: 	'Registration authority',
	'人员规模'			: 	'Staff size',
	'参保人数'			: 	'Number of participants',
	'曾用名'				: 	'Former name',
	'英文名'				: 	'English Name',
	'进出口企业代码'		: 	'Import and export enterprise code',
	'注册地址'			: 	'Registered Address',
	'经营范围'			: 	'Business Scope',
	
}

class company(models.Model):
	backend_string 	= models.CharField(max_length=40) #only actually needs 32, but doesn't hurt to have more space in case system changes. 
	统社会信用代码  	= models.CharField(max_length=200,default="NULL")
	注册资本			= models.CharField(max_length=200,default="NULL")
	组织机构代码 		= models.CharField(max_length=200,default="NULL")
	企业类型			= models.CharField(max_length=200,default="NULL")
	所属行业			= models.CharField(max_length=200,default="NULL")
	人员规模			= models.CharField(max_length=200,default="NULL")
	英文名			= models.CharField(max_length=200,default="NULL")
	注册地址			= models.CharField(max_length=200,default="NULL")
	经营范围			= models.TextField(max_length=1000,default="NULL")
	企业名称			= models.CharField(max_length=200,default="NULL")
	登记状态			= models.CharField(max_length=200,default="NULL")
	实缴资本			= models.CharField(max_length=200,default="NULL")
	工商注册号		= models.CharField(max_length=200,default="NULL")
	营业期限			= models.CharField(max_length=200,default="NULL")
	所属地区			= models.CharField(max_length=200,default="NULL")
	参保人数			= models.CharField(max_length=200, default="NULL")
	成立日期			= models.DateField(null=True, blank=True)
	核准日期			= models.DateField(null=True, blank=True)
	纳税人识别号		= models.CharField(max_length=200, default="NULL")
	纳税人资质		= models.CharField(max_length=200, default="NULL")
	登记机关			= models.CharField(max_length=200, default="NULL")
	曾用名			= models.CharField(max_length=200, default="NULL")
	进出口企业代码	= models.CharField(max_length=200, default="NULL")
	主办券商 		= models.CharField(max_length=200, default="NULL")
	企业网址 		= models.CharField(max_length=200, default="NULL")
	会计事务所 		= models.CharField(max_length=200, default="NULL")
	做市商 			= models.CharField(max_length=200, default="NULL")
	公司传真 		= models.CharField(max_length=200, default="NULL")
	公司注册地址 		= models.CharField(max_length=200, default="NULL")
	公司电子邮箱		= models.CharField(max_length=200, default="NULL")
	公司电话			= models.CharField(max_length=200, default="NULL")
	办公地址 		= models.CharField(max_length=200, default="NULL")
	办公地址邮编 		= models.CharField(max_length=200, default="NULL")
	币种				= models.CharField(max_length=200, default="NULL")
	律师事务所 		= models.CharField(max_length=200, default="NULL")
	总经理 			= models.CharField(max_length=200, default="NULL")
	挂牌日期 		= models.CharField(max_length=200, default="NULL")
	是否上市 		= models.CharField(max_length=200, default="NULL")
	机构名称 		= models.CharField(max_length=200, default="NULL")
	机构状态 		= models.CharField(max_length=200, default="NULL")
	机构简称 		= models.CharField(max_length=200, default="NULL")
	机构类型大类 		= models.CharField(max_length=200, default="NULL")
	机构类型小类 		= models.CharField(max_length=200, default="NULL")
	注册地址邮编		= models.CharField(max_length=200, default="NULL")
	注册资本万元 		= models.CharField(max_length=200, default="NULL")
	职工人数 		= models.CharField(max_length=200, default="NULL")
	英文全称 		= models.CharField(max_length=200, default="NULL")
	英文简称 		= models.CharField(max_length=200, default="NULL")
	董事会秘书 		= models.CharField(max_length=200, default="NULL")
	董事长 			= models.CharField(max_length=200, default="NULL")
	董秘传真 		= models.CharField(max_length=200, default="NULL")
	董秘联系电话 		= models.CharField(max_length=200, default="NULL")
	董秘邮箱 		= models.CharField(max_length=200, default="NULL")
	证券代表 		= models.CharField(max_length=200, default="NULL")
	证券代表传真		= models.CharField(max_length=200, default="NULL")
	证券代表电话 		= models.CharField(max_length=200, default="NULL")
	证券代表邮箱 		= models.CharField(max_length=200, default="NULL")
	电话 			= models.CharField(max_length=20, default="NULL")
	邮箱 			= models.CharField(max_length=200, default="NULL")
	官网 			= models.CharField(max_length=200, default="NULL")
	地址 			= models.CharField(max_length=200, default="NULL")
	简介 			= models.TextField(max_length=5000, default="NULL")
	error_flag 		= models.BooleanField(default=False)
	last_updated 	= models.DateField(auto_now=True)
	relations_check = models.BooleanField(default=False)
	placeholder 	= models.BooleanField(default=False)
	def __str__(self):
		return self.backend_string

	def get_english(field_name):
		try:
			return company_model_translations[field_name]
		except:
			return "ERROR NO MATCH"
	def get_absolute_url(self):
		return (reverse('company_detail', args=[str(self.企业名称)])) 

class individual(models.Model):
	name 			= models.CharField(max_length=50)
	backend_string 	= models.CharField(max_length=100) 

	def __str__(self):
		return self.name

class position(models.Model):	
	position_individual 	= models.ForeignKey(individual, related_name="position_individual", on_delete=models.CASCADE, blank=False, null=False)
	position_company 		= models.ForeignKey(company, related_name="position_company", on_delete=models.CASCADE, blank=False, null=False)
	法定代表人 	= "法定代表人"  
	经营者     	= "经营者"

	position_title_choices = [
		(法定代表人, "法定代表人"),
		(经营者, 	"经营者"),
		]

	position_title     = models.CharField(
		choices=position_title_choices,
		default=法定代表人,
		max_length=20
		)

	def __str__(self):
		self.position_individual.name


#equity is what company owns, ownership is who owns them (equity is down, ownership is up)

class relation_tag_sub(models.Model): # need to come back to tags because it appears they are different depending on type? adding a field that just captures the full dictionary result of each tag for now to prevent data loss, will come back to this later if info is needed
	type_tag					= models.IntegerField(default='NULL')
	name 						= models.CharField(max_length=200, default='NULL')
	shortname 					= models.CharField(max_length=200, default='NULL')
	dataextend 			 		= models.CharField(max_length=200, default='NULL')
	tradingplacecode 			= models.CharField(max_length=200, default='NULL')
	tradingplacename			= models.CharField(max_length=200, default='NULL')
	original_response 			= models.CharField(max_length=500, default="NULL")	

class company_relation(models.Model):
	relation_type  	= models.CharField(max_length=200)
	origin_company 	= models.ForeignKey(company, related_name='Parent', on_delete=models.CASCADE) 
	target_company 	= models.ForeignKey(company, related_name='Child', on_delete=models.CASCADE)
	econ_kind 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	percent 		= models.DecimalField(default=0,decimal_places = 5, max_digits=8, blank=True, null=True)
	percent_total 	= models.DecimalField(help_text="Value listed in QCC API response, carried over for data completeness.",blank=True, null=True,decimal_places = 5, max_digits=8)
	org 			= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.",default=0)
	company_code 	= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.",default=0)
	shouldcapi  	= models.DecimalField(blank=True, null=True, decimal_places = 6, max_digits=21)
	stockrightnum	= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	detailcount 	= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.", default=0)
	shortstatus 	= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="在业")
	stocktype 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	investtype 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	registered_cap 	= models.DecimalField(blank=True, null=True, decimal_places = 3, max_digits=21)
	tags 	 		= models.ManyToManyField(relation_tag_sub)
	detaillist 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	type 			= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	pulled_date		= models.DateField(auto_now_add=True)

	def __str__(self):
		self_string = "{}-({})".format(self.target_company, self.origin_company)
		return self_string

class error_report(models.Model):
	model_type 		= models.CharField(max_length=200)
	model_inst 		= models.CharField(max_length=200)
	error_type 		= models.CharField(max_length=50) 
	date 	 		= models.DateField(auto_now_add=True)
	text 			= models.TextField(max_length=5000, default='NULL')

	def __str__(self):
		self_string = "{}/{}({})-{}".format(self.model_type, self.model_inst, self.date, self.text)
		return self_string

class figure_relation(models.Model):
	relation_type  	= models.CharField(max_length=200)
	origin_company 	= models.ForeignKey(company, related_name='Company', on_delete=models.CASCADE) 
	target_figure 	= models.ForeignKey(individual, related_name='Figure', on_delete=models.CASCADE)
	econ_kind 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	percent 		= models.DecimalField(default=0,decimal_places = 5, max_digits=8, blank=True, null=True)
	percent_total 	= models.DecimalField(help_text="Value listed in QCC API response, carried over for data completeness.",blank=True, null=True,decimal_places = 5, max_digits=8)
	org 			= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.",default=0)
	company_code 	= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.",default=0)
	shouldcapi  	= models.DecimalField(blank=True, null=True, decimal_places = 6, max_digits=21)
	stockrightnum	= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	detailcount 	= models.IntegerField(help_text="Value listed in QCC API response, carried over for data completeness.", default=0)
	shortstatus 	= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="在业")
	stocktype 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	investtype 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	registered_cap 	= models.DecimalField(blank=True, null=True, decimal_places = 3, max_digits=21)
	tags 	 		= models.ManyToManyField(relation_tag_sub)
	detaillist 		= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	type 			= models.CharField(max_length=200, help_text="Value listed in QCC API response, carried over for data completeness.", default="NULL")
	pulled_date		= models.DateField(auto_now_add=True)

	def __str__(self):
		self_string = "{}-({})".format(self.target_company, self.origin_company)
		return self_string