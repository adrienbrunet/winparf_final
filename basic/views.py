#-*- coding: utf-8 -*-
from django.shortcuts import render


def home(request):
    '''Redirect to the template for the Home page'''
    return render(request, 'basic/home.html',)


def about(request):
    ''' Redirect to the template for the About page'''
    return render(request, 'basic/about.html',)

def permission(request):
	return render(request, 'basic/permission.html')
