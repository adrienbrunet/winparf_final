from django.conf.urls import patterns, url, include

 
urlpatterns = patterns('basic.views',
	url(r'^$', 'home'),

   
)