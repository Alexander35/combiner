from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class Worker(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=100, null=True, blank=True)
	input_params = models.CharField(max_length=100, blank=False, null=False)
	run_command = models.CharField(max_length=100)
	user = models.ManyToManyField(User)
	visibility = models.BooleanField(default=True, blank=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)	

class Project(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=300)
	worker = models.ManyToManyField(Worker)
	user = models.ManyToManyField(User)
	visibility = models.BooleanField(default=True, blank=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)	

class Data(models.Model):
	from_worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True)
	data = JSONField()
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)		

	class Meta:
		verbose_name_plural = "data"