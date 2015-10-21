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
# Create your views here.
from events.models import Event, Vendor


#access_token = '1705064953059017|42XOhVMYt9tJrftP-_btcBvQS5I'


events_page = 'OffTheGridSF/events'
r = requests.get('https://graph.facebook.com/' + events_page + '?access_token=1705064953059017|e3b4439e3577e83f7f6a095a875f3f74')
events = r.json()

#http://graph.facebook.com/endpoint?key=value&access_token=app_id|app_secret
#graph = facebook.GraphAPI(access_token)
#events = graph.get_object(events_page)
#print events['data']

#Vendor.objects.all().delete()
#Event.objects.all().delete()

event_list = [event for event in events['data'] \
				if parser.parse(event['start_time'].encode('ascii','ignore')) > timezone.now() ]

for event in events['data']:
	if not Event.objects.filter(event_id=event['id'].encode('ascii','ignore')):
		event_obj = Event()
		event_obj.name = event['name'].encode('ascii','ignore')
		event_obj.event_id = event['id'].encode('ascii','ignore')
		event_obj.date = parser.parse(event['start_time'].encode('ascii','ignore'))
		event_obj.description = event['description'].encode('ascii','ignore')
		#print event_obj.description
		event_obj.save()




vendors_page = requests.get('http://offthegridsf.com/vendors')
vendors_file = html.fromstring(vendors_page.text)
vendors = vendors_file.xpath('//a[@class="otg-vendor-name-link"]/text()')
vendors_list = set()
for vendor in vendors:
	if "(" in vendor:
		index = vendor.index('(')
		vendor = vendor[0:index]
	vendors_list.add(vendor)


for vendor in vendors_list:
	if not Vendor.objects.filter(name=vendor):
		vendor_obj = Vendor()
		vendor_obj.name = vendor
		vendor_obj.number_of_occurences = 0
		vendor_obj.save()


for event in Event.objects.filter(date__gte=timezone.now() - timedelta(days=30)):
	#print "yolo"
	for vendor in Vendor.objects.all():
		
		if vendor.name in event.description:
			vendor.events.add(event)			

for vendor in Vendor.objects.all():
	vendor.number_of_occurences = vendor.events.filter(date__gte=timezone.now() - timedelta(days=30)).count()
	vendor.save()


#if datetime.datetime.strptime(str(event['start_time']),'%Y-%m-%dT%H:%M:%S-0000') > datetime.datetime.now()]

def index(request):
	#context = { """'event_list' : event, 'vendors': vendors_list"""}
	return render(request, 'events/index.html')#, context)

def events(request):
	upcoming_events = Event.objects.filter(date__gte = timezone.now())
	context = { 'event_list' : upcoming_events, 'vendors': vendors_list}
	return render(request, 'events/events.html', context)

def event_detail(request, event_id):
	event = Event.objects.get(event_id=event_id)
#	for string in vendors_list:
#		if string in event.description:
#				event_vendors.append(string)

	event = event.vendor_set.all()			

	context = { 'event_vendors': event }

	return render(request, 'events/detail.html', context)

def vendor_detail(request, vendor_id):
	vendor = Vendor.objects.get(id=vendor_id)

	

	return HttpResponse(vendor.name + str(vendor.number_of_occurences))


def vendors(request):
	full_list = Vendor.objects.all().order_by('-number_of_occurences')
	context = {'vendors_list': full_list}
	return render(request, 'events/vendors.html', context)