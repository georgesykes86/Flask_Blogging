import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User(password = 'somepassword')
        self.assertTrue(user.password_hash is not None)

    def test_password_getter(self):
        user = User(password = 'password')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification_correct(self):
        user = User(password = 'password')
        self.assertTrue(user.verify_password('password'))

    def test_password_verification_incorrect(self):
        user = User(password = 'password')
        self.assertFalse(user.verify_password('notpassword'))

    def test_random_password_salting(self):
        user = User(password = 'password')
        otherUser = User(password = 'otherpassword')
        self.assertTrue(user.password_hash != otherUser.password_hash)
