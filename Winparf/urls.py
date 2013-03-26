# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('basic.urls')),
    url(r'^about/$','basic.views.about'),
    (r'^register/$', 'userwinparf.views.UserwinparfRegistration'),
    (r'^login/$', 'userwinparf.views.LoginRequest'),
    (r'^logout/$', 'userwinparf.views.LogoutRequest'),
    (r'^profiles/', include('profiles.urls')),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r"^forum/(\d+)/$", "forum.views.forum"),
    (r"^forum/$", "forum.views.main"),
    (r"^thread/(\d+)/$", "forum.views.thread"),
    (r"^post/(new_thread|reply)/(\d+)/$", "forum.views.post"),
    (r"^reply/(\d+)/$", "forum.views.reply"),
    (r"^new_thread/(\d+)/$", "forum.views.new_thread"),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^search-form/$', "forum.views.search_form"),
    (r'^search/$', "forum.views.search"),
  )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
