from django.db import models

# Create your models here.


class index_pages(models.Model):
	index_code			= models.CharField(max_length=15,default="NULL")
	emptied 			= models.BooleanField(default=False)
	next_page 			= models.IntegerField(default=0)
	checked_out 		= models.BooleanField(default=False)


class skipped_company(models.Model):
	backend_string 		= models.CharField(max_length=40) #only actually needs 32, but doesn't hurt to have more space in case system changes. 
	error_date 			= models.DateField(auto_now_add=True)