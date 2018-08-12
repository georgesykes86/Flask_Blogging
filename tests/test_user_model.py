import unittest
from unittest.mock import Mock
from app.models import User, Role, Permission, AnonymousUser

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.userrole = Role(name="User")
        self.userrole.permissions = Permission.FOLLOW | \
                                    Permission.COMMENT | \
                                    Permission.WRITE_POSTS
        self.user = User(email='testuser@example.com', password='password', role=self.userrole)
        self.otherUser = User(email='othertestuser@example.com', password='password', role=self.userrole)

    def test_password_setter(self):
        self.assertTrue(self.user.password_hash is not None)

    def test_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification_correct(self):
        self.assertTrue(self.user.verify_password('password'))

    def test_password_verification_incorrect(self):
        self.assertFalse(self.user.verify_password('notpassword'))

    def test_random_password_salting(self):
        self.assertTrue(self.user.password_hash != self.otherUser.password_hash)

    def test_roles_and_permissions(self):
        self.assertTrue(self.user.can(Permission.WRITE_POSTS))
        self.assertFalse(self.user.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))
