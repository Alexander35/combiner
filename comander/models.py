from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
# from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.

NOTIFYTYPE = (
	('warning', 'warning'),
	('error', 'error'),
	('debug', 'debug'),
	('info', 'info'),
	('critical', 'critical'),
	)

class Notify(models.Model):

	notify_type = models.CharField(max_length=100, choices=NOTIFYTYPE, default='info')
	data = JSONField()
	to =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)	

	def __str__(self):
		return '{}'.format(self.data)	

class Worker_Msg(models.Model):

	notify_type = models.CharField(max_length=100, choices=NOTIFYTYPE, default='info')
	data = JSONField()
	worker =  models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, default=1)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)	

	def __str__(self):
		return '{} :: {}'.format(self.worker.name, self.data)			

class Worker(models.Model):
	
	STATES = (
		('Just Added', 'Just Added'),
		('Processing', 'Processing'),
		('Ready', 'Ready'),
		)

	CAHRSET = (
		('cp866','cp866'),
		('cp1251','cp1251'),
		('utf-8','utf-8'),
		('latin-1','latin-1'),
		('ascii','ascii'),
		('koi8-r','koi8-r'),
		)

	STRENCODEERRORTYPE = (
		('strict','strict'),
		('ignore','ignore'),
		('replace','replace'),
		('xmlcharrefreplace','xmlcharrefreplace'),
		('backslashreplace','backslashreplace'),
		)

	WORKERTYPE = (
		('data_miner', 'data_miner'),
		('processor', 'processor'),
		('harvester', 'harvester'),
		)

	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=100, null=True, blank=True)
	input_params = models.CharField(max_length=100, blank=False, null=False)
	run_command = models.CharField(max_length=100)
	user = models.ManyToManyField(User)
	visibility = models.BooleanField(default=True, blank=False)
	status = models.CharField(max_length=100, choices=STATES, default='Just Added')
	char_set = models.CharField(max_length=100, choices=CAHRSET, default='utf-8')
	str_error_type = models.CharField(max_length=100, choices=STRENCODEERRORTYPE, default='backslashreplace')
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)	

	priority = models.CharField(max_length=100, choices=WORKERTYPE, default='data_miner')

	# project_sequence_number = models.ForeignKey('ProjectSequenceNumber', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return 'Name: {}, Run Command: {}, Input Params: {}'.format(self.name, self.run_command, self.input_params)

# class ProjectSequenceNumber(models.Model):

# 	project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
# 	worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True)
# 	sequence_number = models.IntegerField(default=0, validators=[MinValueValidator(0)])

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

	def __str__(self):
		return '{}'.format(self.data)	