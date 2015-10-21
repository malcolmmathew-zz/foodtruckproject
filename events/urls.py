from django.conf.urls import url
#from events import views

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^events/$', views.events, name='events'),
	url(r'^vendors/$', views.vendors, name='vendors'),
	url(r'^(?P<event_id>[0-9]+)/$', views.event_detail, name='event_detail'),
	url(r'^vendor/(?P<vendor_id>[0-9]+)/$', views.vendor_detail, name="vendor_detail")
]