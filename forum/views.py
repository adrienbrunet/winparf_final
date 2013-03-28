from django.core.urlresolvers import reverse
from django.conf import settings
from forum.models import Forum, Thread, Post
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from userwinparf.models import *
from datetime import * 


# def regular(func):
#     def wrapper(*args, **kwargs):
#         # Pre-traitement            
#         response = func(*args, **kwargs)
#         if request.user.is_authenticated():
#             u = request.user.get_profile
#             v=u.can_upload
#             if not v=="regular":
#                 return HttpResponseRedirect('/')
#         # Post-traitement
#         return response
#     return wrapper


# @login_required
# def access(request):

@login_required
def main(request):
    """Main listing."""
    # now = date.today()
    # u = request.user.get_profile()
    # v = u.date_joined
    # limit = datetime.timedelta(days=365)
    # delta = now-v
    # if delta.days  > limit:
    #     return HttpResponseRedirect('/permission')
            #---------------
    errors = []
    search = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            thread = Thread.objects.filter(title__icontains=q)
            nb_thread = len(list(thread))
            thread = mk_paginator(request, thread, 15)
            search = True
            return render_to_response('forum/search.html', add_csrf(request, thread=thread, query=q, search=search, errors=errors, nb_thread=nb_thread))
    #------------------
    forums = Forum.objects.all()
    return render_to_response("forum/list.html", dict(forums=forums, user=request.user, errors=errors, search=search))


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


@login_required
def forum(request, pk):
    """Listing of threads in a forum."""
    #---------------
    errors = []
    search = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            thread = Thread.objects.filter(title__icontains=q)
            nb_thread = len(list(thread))
            thread = mk_paginator(request, thread, 15)
            search = True
            return render_to_response('forum/search.html', add_csrf(request, thread=thread, query=q, search=search, errors=errors, nb_thread=nb_thread))
    #------------------
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = mk_paginator(request, threads, 20)
    threads_recommanded = Thread.objects.filter(forum=pk).order_by("-nbviews")
    threads_recommanded = mk_paginator(request, threads_recommanded, 3)

    return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk, errors=errors, search=search, threads_recommanded=threads_recommanded))


@login_required
def thread(request, pk):
    """Listing of posts in a thread."""
    t=Thread.objects.get(pk=pk)
    t.nbviews    = t.nbviews + 1
    t.save()
    posts = Post.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    title = Thread.objects.get(pk=pk).title
    t     = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title, forum_pk=t.forum.pk))


@login_required
def post(request, ptype, pk):
    u = request.user.get_profile()
    v=u.can_upload
    if v==False:
        return HttpResponseRedirect('/permission')
    """Display a post form."""
    action = reverse("forum.views.%s" % ptype, args=[pk])
    if ptype == "new_thread":
        title = "Start New Topic"
        subject = ''
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title
    return render_to_response("forum/post.html", add_csrf(request, subject=subject, action=action, title=title))


@login_required
def new_thread(request, pk):
    u = request.user.get_profile()
    v=u.can_upload
    if v==False:
        return HttpResponseRedirect('/permission')
        """Start a new thread."""
    p = request.POST
    if p["subject"] and p["body"]:
        forum = Forum.objects.get(pk=pk)
        thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
        Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
    return HttpResponseRedirect(reverse("forum.views.forum", args=[pk]))


@login_required
def reply(request, pk):
    u = request.user.get_profile()
    v=u.can_upload
    if v==False:
        return HttpResponseRedirect('/permission')
        """Reply to a thread."""
    p = request.POST
    if p["body"]:
        thread = Thread.objects.get(pk=pk)
        post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
    return HttpResponseRedirect(reverse("forum.views.thread", args=[pk]) + "?page=last")
