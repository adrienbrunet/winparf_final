from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from forum.models import *
from django.conf import settings
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from userwinparf.models import *

class RegisterTest(LiveServerTestCase):
    '''Navigate on the website testing all functionnalities'''
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.set_page_load_timeout(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_userwinparf_via_admin_site_loggin_and_see_the_forum(self):
        ''' Gertrude opens her web browser, and goes to the admin page to create a new user on the website extending the model User of Django'''
        self.browser.get(self.live_server_url + '/admin/')

        ''' She sees the familiar 'Django administration' heading'''
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        ''' She types in her username and passwords and hits return'''
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('winparf')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('winparf')
        password_field.send_keys(Keys.RETURN)

        ''' her username and password are accepted, and she is taken to
        the Site Administration page'''
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        ''' She now sees a hyperlink that says "Userbets"'''
        userbet_links = self.browser.find_elements_by_link_text('Userwinparfs')
        self.assertEquals(len(userbet_links), 1)

        ''' so she clicks it'''
        userbet_links[0].click()

        ''' She is taken to the userwinparf listing page, which shows she has
         no userbet yet'''
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 userwinparfs', body.text)

        ''' She sees a link to 'add' a new userwinparf, so she clicks it'''
        new_userbet_link = self.browser.find_element_by_link_text('Add userwinparf')
        new_userbet_link.click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        f = Forum.objects.create(title="forum")
        f2 = Forum.objects.create(title="forum2")
        f3 = Forum.objects.create(title="forum3")
        f4 = Forum.objects.create(title="forum4")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        u2 = User.objects.create_user("ak2", "ak2@abc.org", "pwd")
        u3 = User.objects.create_user("ak3", "ak3@abc.org", "pwd")
        Site.objects.create(domain="test.org", name="test.org")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        t2 = Thread.objects.create(title="thread2", creator=u2, forum=f2)
        t3 = Thread.objects.create(title="thread3", creator=u, forum=f3)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)
        p2 = Post.objects.create(title="post", body="body", creator=u, thread=t2)
        p3 = Post.objects.create(title="post", body="body", creator=u, thread=t3)
        p4 = Post.objects.create(title="post", body="body", creator=u, thread=t)

        userwinparf = Userwinparf.objects.create(user=u,name="ak", can_upload=True)

        self.browser.get(self.live_server_url + '/forum/')
        logout = self.browser.find_element_by_id('logout')
        logout.click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Winparf', body.text)

        self.browser.get(self.live_server_url + '/forum/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Username:', body.text)

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('ak')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('pwd')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('forum', body.text)

        