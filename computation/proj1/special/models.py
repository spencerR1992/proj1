from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
#json = JSONField()

# Create your models here.

class Company(models.Model):
	name = models.CharField(max_length=300)
	symbol = models.CharField(max_length=20,unique=True)
	stock_data = JSONField(null=True,blank=True)
	industry = models.ForeignKey('Industry', null=True)
	sector = models.ForeignKey('Sector', null=True)
	def __unicode__(self):
		return self.symbol

class Industry(models.Model):
	name = models.CharField(max_length=300,unique=True)
	def __unicode__(self):
		return self.name

class Sector(models.Model):
	name = models.CharField(max_length=500,unique=True)
	def __unicode__(self):
		return self.name




