# coding=utf-8
from django.db import models

class Mysite(models.Model):
	title = models.CharField(max_length=100)
	url = models.URLField()
	author = models.CharField(max_length=100)
	num = models.IntegerField(max_length=10)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['num'] # 默认按照num进行排序

class Book(models.Model):
	name = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)