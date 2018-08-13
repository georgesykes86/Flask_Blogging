import unittest
from unittest.mock import Mock
from app.models import User, Role, Permission, AnonymousUser

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user_role = Role(name="User")
        self.user_role.permissions = Permission.FOLLOW | \
                                    Permission.COMMENT | \
                                    Permission.WRITE_POSTS
        self.admin_user_role = Role(name="Admin")
        self.admin_user_role.permissions = 0xff
        self.user = User(email='testuser@example.com', password='password', role=self.user_role)
        self.other_user = User(email='othertestuser@example.com', password='password', role=self.user_role)
        self.admin_user = User(email='admin@example.com', password='password', role=self.admin_user_role)

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
        self.assertTrue(self.user.password_hash != self.other_user.password_hash)

    def test_roles_and_permissions(self):
        self.assertTrue(self.user.can(Permission.WRITE_POSTS))
        self.assertFalse(self.user.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))

    def test_admin_user(self):
        self.assertTrue(self.admin_user.is_administrator())

    def test_update_gravatar_hash_no_email_change(self):
        current_hash = self.user.avatar_hash
        self.user.update_gravatar_hash()
        self.assertTrue(self.user.avatar_hash == current_hash)

    def test_update_gravatar_hash_email_change(self):
        current_hash = self.user.avatar_hash
        self.user.email = 'new_email@test.com'
        self.user.update_gravatar_hash()
        self.assertTrue(self.user.avatar_hash != current_hash)
