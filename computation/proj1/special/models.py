from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
#json = JSONField()

# Create your models here.

class Company(models.Model):
	name = models.CharField(max_length=300)
	ticker_symbol = models.CharField(max_length=20,unique=True)
	stock_data = JSONField(null=True,blank=True)
	def __unicode__(self):
		return self.ticker_symbol
