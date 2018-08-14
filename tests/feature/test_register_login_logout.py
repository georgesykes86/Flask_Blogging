import threading
import unittest
import time
from app import create_app, db, fake
from app.models import User, Role
from selenium import webdriver


class RegisterLoginLogoutTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.session.remove()
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            db.create_all()
            Role.insert_roles()
            fake.users(10)

            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin_user = User(email='admin@test.com', username='admin',
                              password='password', role=admin_role)
            db.session.add(admin_user)
            db.session.commit()

            cls.server_thread = threading.Thread(target=cls.app.run)
            cls.server_thread.start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass


    def test_registration_signin_signout(self):
        self.client.get("http:/localhost:5000/auth/login")
        self.client.find_element_by_link_text('Register here').click()
        self.assertTrue('<h1>Register</h1>' in self.client.page_source)
        self.client.find_element_by_name('email').send_keys('newUser@testing.com')
        self.client.find_element_by_name('username').send_keys('newUser')
        self.client.find_element_by_name('password').send_keys('password')
        self.client.find_element_by_name('passwordConf').send_keys('password')
        self.client.find_element_by_name('submit').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)
        self.client.find_element_by_name('email').send_keys('newUser@testing.com')
        self.client.find_element_by_name('password').send_keys('password')
        self.client.find_element_by_name('submit').click()
        self.assertTrue('newUser' in self.client.page_source)
        self.client.find_element_by_link_text('Sign Out').click()
        self.assertTrue('Sign In' in self.client.page_source)
