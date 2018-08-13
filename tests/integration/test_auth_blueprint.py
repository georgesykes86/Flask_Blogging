import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role

class AuthBlueprintClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login_logout(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'password',
            'passwordConf': 'password'
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@test.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertTrue('Index' in response.get_data(as_text=True))
        self.assertTrue('test' in response.get_data(as_text=True))
        response = self.client.post(url_for('auth.logout'))
        self.assertFalse('test' in response.get_data(as_text=True))
