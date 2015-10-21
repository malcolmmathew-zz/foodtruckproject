from django.db import models

# Create your models here.

class Event(models.Model):
	date = models.DateTimeField()
	name = models.CharField(max_length=200)
	#location = models.CharField(max_length=350)
	event_id = models.IntegerField(default=0)
	description = models.TextField(max_length=1500, default="")

	def __str__(self):
		return self.name

class Vendor(models.Model):
	name = models.CharField(max_length=200)
	number_of_occurences = models.IntegerField(default=0)
	events = models.ManyToManyField(Event)

	def __str__(self):
		return self.name

