from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Name(models.Model):
	title=models.CharField(max_length=250)
	def __unicode__(self):
		return self.title
		