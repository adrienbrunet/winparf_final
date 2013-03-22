#-*- coding: utf-8 -*-
from django.shortcuts import render
 
def home(request):
    return render(request, 'basic/home.html',)

def about(request):
	return render(request, 'basic/about.html',)