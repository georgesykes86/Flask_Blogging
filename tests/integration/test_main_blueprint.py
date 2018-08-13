import unittest
from flask import url_for
from flask_login import current_user
from app import create_app, db
from app.models import User, Role

class MainBlueprintClientTestCase(unittest.TestCase):
    def create_user_helper(self):
        self.user_email = 'testuser@example.com'
        user = User(email=self.user_email, password='password', username='testuser')
        db.session.add(user)

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.create_user_helper()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Welcome to G-Blog' in response.get_data(as_text=True))

    def test_not_logged_in(self):
        user_id = User.query.filter_by(email=self.user_email).first().id
        response = self.client.get(url_for('main.user', id=user_id), follow_redirects=True)
        self.assertTrue('Login' in response.get_data(as_text=True))
