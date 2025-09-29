from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from posts.models import Post


User = get_user_model()


class PostsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.other = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(title='Hello', content='World', author=self.user)

    def test_list_posts(self):
        url = '/api/posts/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # response may be a list or paginated dict
        data = resp.json()
        if isinstance(data, dict) and 'results' in data:
            items = data['results']
        else:
            items = data
        self.assertTrue(any(p.get('title') == 'Hello' for p in items))

    def test_create_requires_auth(self):
        url = '/api/posts/'
        resp = self.client.post(url, {'title': 'New', 'content': 'B'}, format='json')
        # Unauthenticated should be denied
        self.assertIn(resp.status_code, (401, 403))

    def obtain_jwt(self, username, password):
        url = '/api/auth/login/'
        resp = self.client.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(resp.status_code, 200)
        return resp.json().get('access')

    def test_create_post(self):
        access = self.obtain_jwt('alice', 'pass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        url = '/api/posts/'
        resp = self.client.post(url, {'title': 'AuthPost', 'content': 'ok'}, format='json')
        self.assertIn(resp.status_code, (200, 201))
        data = resp.json()
        self.assertEqual(data.get('title'), 'AuthPost')

    def test_update_and_delete_owner(self):
        url = f'/api/posts/{self.post.pk}/'
        # bob cannot edit alice's post
        bob_token = self.obtain_jwt('bob', 'pass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {bob_token}')
        resp = self.client.patch(url, {'title': 'Hacked'}, format='json')
        self.assertIn(resp.status_code, (401, 403, 404))

        # alice can update
        alice_token = self.obtain_jwt('alice', 'pass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {alice_token}')
        resp = self.client.patch(url, {'title': 'Updated'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Post.objects.get(pk=self.post.pk).title, 'Updated')

        # alice can delete
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (204, 200))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
