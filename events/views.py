from django.shortcuts import render
from django.http import HttpResponse

import requests
import json
from lxml import html

import datetime
from datetime import timedelta
from dateutil import parser
from django.utils import timezone 

from . import models
from events.models import Event, Vendor

#Accesses the facebook Graph API and parses the response object.
events_page = 'OffTheGridSF/events'
r = requests.get('https://graph.facebook.com/' + events_page + '?access_token=1705064953059017|e3b4439e3577e83f7f6a095a875f3f74')
events = r.json()

#Vendor.objects.all().delete()
#Event.objects.all().delete()

#Iterate through the events objects and save it if the object isn't 
#already in the database.
for event in events['data']:
	if not Event.objects.filter(event_id=event['id'].encode('ascii','ignore')):
		event_obj = Event()
		event_obj.name = event['name'].encode('ascii','ignore')
		event_obj.event_id = event['id'].encode('ascii','ignore')
		event_obj.date = parser.parse(event['start_time'].encode('ascii','ignore'))
		event_obj.description = event['description'].encode('ascii','ignore')
		event_obj.save()

#Scrape through the vendor site and gather a list of vendor names
vendors_page = requests.get('http://offthegridsf.com/vendors')
vendors_file = html.fromstring(vendors_page.text)
vendors = vendors_file.xpath('//a[@class="otg-vendor-name-link"]/text()')
vendors_list = set()

#Parse the vendor list for duplicate items of the form 'x (1)', 'x (20)'
#by stripping the values and adding it to a set which will not allow duplicates.
for vendor in vendors:
	if "(" in vendor:
		index = vendor.index('(')
		vendor = vendor[0:index]
	vendors_list.add(vendor)

#Iterate through the vendor set and if the object isn't already in the 
#database save the object.
for vendor in vendors_list:
	if not Vendor.objects.filter(name=vendor):
		vendor_obj = Vendor()
		vendor_obj.name = vendor
		vendor_obj.number_of_occurences = 0
		vendor_obj.save()

#Check all events from the past month and compare the event description string 
#with the list of vendors. If it matches then add the event to the respective vendor.
for event in Event.objects.all():
	for vendor in Vendor.objects.all():
		if vendor.name.lower() in event.description.encode('ascii','ignore').lower():
			vendor.events.add(event)			

#Iterate through vendor objects and calculate number of occurences by looking at
#related events
for vendor in Vendor.objects.all():
	vendor.number_of_occurences = vendor.events.filter(date__gte=timezone.now() - timedelta(days=30)).count()
	vendor.save()

#filter(date__gte=timezone.now() - timedelta(days=30))

#Home page that links to the events and vendors pages
def index(request):
	return render(request, 'events/index.html')

#Page that lists all upcoming events
def events(request):
	upcoming_events = Event.objects.filter(date__gte = timezone.now())
	context = { 'event_list' : upcoming_events, 'vendors': vendors_list}
	return render(request, 'events/events.html', context)

#Page that lists out vendors for a given event
def event_detail(request, event_id):
	event = Event.objects.get(event_id=event_id)

	event_vendors = event.vendor_set.all()			

	context = { 'event_vendors': event_vendors, 'event': event }

	return render(request, 'events/event_detail.html', context)

#Page that serves up Vendor details
def vendor_detail(request, vendor_id):
	vendor = Vendor.objects.get(id=vendor_id)

	#return HttpResponse(vendor.name + str(vendor.number_of_occurences))
	context = {'vendor': vendor}
	return render(request, 'events/vendor_detail.html', context)

#List of Vendors
def vendors(request):
	full_list = Vendor.objects.all().order_by('-number_of_occurences')
	context = {'vendors_list': full_list}
	return render(request, 'events/vendors.html', context)