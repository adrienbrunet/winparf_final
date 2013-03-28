from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from forum.models import *

class SimpleTest(TestCase):

    def setUp(self):
        f = Forum.objects.create(title="forum")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        Site.objects.create(domain="test.org", name="test.org")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)

    def test_all_urls(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")
        resp = self.client.get('/forum/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/about/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/forum/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/forum/1/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/thread/1/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/post/new_thread/1/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/post/reply/1/')
        self.assertEqual(resp.status_code, 200)

    def test_all_urls_admin(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/admin/forum/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/admin/forum/post/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/admin/forum/thread/')
        self.assertEqual(resp.status_code, 200)


