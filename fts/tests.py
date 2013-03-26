from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class RegisterTest(LiveServerTestCase):
    fixtures = ['admin_user.json']


    def setUp(self):
    	self.browser = webdriver.Firefox()
    	self.browser.implicitly_wait(3)
    	self.browser.set_page_load_timeout(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_userbet_via_admin_site(self):
        # Gertrude opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        
        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('winparf')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('winparf')
        password_field.send_keys(Keys.RETURN)

        # her username and password are accepted, and she is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She now sees a hyperlink that says "Userbets"
        userbet_links = self.browser.find_elements_by_link_text('Userwinparfs')
        self.assertEquals(len(userbet_links), 1)

    	# so she clicks it
    	userbet_links[0].click()

    	# She is taken to the userbets listing page, which shows she has
    	# no userbet yet
    	body = self.browser.find_element_by_tag_name('body')
    	self.assertIn('0 userwinparfs', body.text)

    	# She sees a link to 'add' a new poll, so she clicks it
    	new_userbet_link = self.browser.find_element_by_link_text('Add userwinparf')
    	new_userbet_link.click()

    	body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # TODO: Gertrude uses the admin site to create a new userbet
        #self.fail('todo: finish tests')
