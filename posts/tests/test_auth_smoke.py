from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class AuthSmokeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass1234')
        self.client = Client()

    def test_login_flow(self):
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'pass1234'}, follow=True)
        self.assertIn(resp2.status_code, (200, 302))

    def test_password_reset_flow(self):
        resp = self.client.get('/accounts/password_reset/')
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.post('/accounts/password_reset/', {'email': 'test@example.com'}, follow=True)
        self.assertIn(resp2.status_code, (200, 302))
