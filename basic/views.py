#-*- coding: utf-8 -*-
from django.shortcuts import render


def home(request):
    '''Redirect to the template for the Home page'''
    return render(request, 'basic/home.html',)


def about(request):
    ''' Redirect to the template for the About page'''
    return render(request, 'basic/about.html',)

def permission(request):
	''' Redirect to the template when you don't have the access to the content.'''
	return render(request, 'basic/permission.html')

def expired(request):
	''' Redirect to the template when your account has expired.'''
	return render(request, 'basic/expired.html')
