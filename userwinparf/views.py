from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from userwinparf.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userwinparf.models import Userwinparf
from datetime import *
import pytz


def UserwinparfRegistration(request):
        '''Views that register the user in our database if the form is valid.'''
        if request.user.is_authenticated():
                return HttpResponseRedirect('/forum/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                        user.save()
                        userwinparf = Userwinparf(user=user, name=form.cleaned_data['name'], can_upload=False)
                        userwinparf.save()
                        return HttpResponseRedirect('/forum/')
                else:
                        return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render_to_response('register.html', context, context_instance=RequestContext(request))

def LoginRequest(request):
        ''' View to log in.'''

        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        userwinparf = authenticate(username=username, password=password)
                        if userwinparf is not None:
                                login(request, userwinparf)
                                now = datetime.today()
                                u = userwinparf
                                v = u.date_joined
                                limit = timedelta(days=365)
                                delta = now-v
                                if delta.days  > limit.days:
                                    logout(request)
                                    return HttpResponseRedirect('/expired')
                                return HttpResponseRedirect('/forum/')
                        else:
                                return render_to_response('login.html', {'form': form, 'error':'Invalid username and/or password'}, context_instance=RequestContext(request))
                else:

                    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
        '''View to log out.'''
        logout(request)
        return HttpResponseRedirect('/')

@login_required
def profile(request):
        ''' View to access the profiles.'''
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/login/')
        userwinparf = request.user.get_profile
        context = { 'userwinparf' : userwinparf}
        return render_to_response('profile_detail.html', context, context_instance=RequestContext(request))

