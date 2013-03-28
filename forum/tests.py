from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import *

<<<<<<< HEAD

=======
>>>>>>> e0fb891d42881a91bf5afc1e1961cb3a12424c00
class SimpleTest(TestCase):
    def setUp(self):
        f = Forum.objects.create(title="forum")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        Site.objects.create(domain="test.org", name="test.org")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test(self):
<<<<<<< HEAD
        ''' Testing creation of forum and thread. '''
        self.c = Client()
        self.c.login(username="ak", password="pwd")

        self.content_test("/forum/", ['<a href="/forum/1/">forum</a>'])
        self.content_test("/forum/1/", ['<a href="/thread/1/">thread</a>', "ak - post"])
        self.content_test("/thread/1/", ['<tr style="border-collapse : collapse; border-spacing : 2px;" class="odd">', '<b>post</b><br>', '<i style="color:grey;">by ak |', '<td style="padding-left:20px;">body</td>'])
        # r = self.c.post("/post/new_thread/1/", {"subject": "thread2", "body": "body2", 'nbviews': '1'})
        # r = self.c.post("/post/reply/2/", {})
#       self.content_test("/thread/2/", ['<tr style="border-collapse : collapse; border-spacing : 2px;" class="odd">','<i style="color:grey;">by ak |','body2'])
        #     ' <td style="padding-left: 20px;">body3</td>'
=======
        self.c = Client()
        self.c.login(username="ak", password="pwd")

        self.content_test("/forum/", ['<a href="/forum/forum/1/">forum</a>'])
        self.content_test("/forum/forum/1/", ['<a href="/forum/thread/1/">thread</a>', "ak - post"])

        self.content_test("/forum/thread/1/", ['<div class="ttitle">thread</div>',
               '<span class="title">post</span>', 'body <br />', 'by ak |'])

        r = self.c.post("/forum/new_thread/1/", {"subject": "thread2", "body": "body2"})
        r = self.c.post("/forum/reply/2/", {"subject": "post2", "body": "body3"})
        self.content_test("/forum/thread/2/", ['<div class="ttitle">thread2</div>',
               '<span class="title">post2</span>', 'body2 <br />', 'body3 <br />'])
>>>>>>> e0fb891d42881a91bf5afc1e1961cb3a12424c00
