from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersSmokeTest(TestCase):
    def test_create_user_model(self):
        User = get_user_model()
        self.assertTrue(hasattr(User, "objects"))


