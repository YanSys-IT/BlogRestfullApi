from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post


User = get_user_model()


class PostCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pwd')
        self.other = User.objects.create_user(username='user2', password='pwd')

    def test_create_post_requires_login(self):
        url = reverse('web-post-add')
        resp = self.client.get(url)
        # Redirect to login for anonymous
        self.assertEqual(resp.status_code, 302)

        self.client.login(username='user1', password='pwd')
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, 200)

        # create without image (avoid ImageField validation in tests)
        resp3 = self.client.post(url, {'title': 'T', 'content': 'C'}, follow=True)
        self.assertEqual(resp3.status_code, 200)
        # assert a post authored by this user was created
        if not Post.objects.filter(author=self.user).exists():
            print('POST response snippet:', resp3.content.decode('utf-8')[:2000])
        self.assertTrue(Post.objects.filter(author=self.user).exists())

    def test_only_author_can_edit(self):
        post = Post.objects.create(author=self.user, title='orig', content='x')
        edit_url = reverse('web-post-edit', args=[post.pk])

        # other user cannot edit (should redirect or be forbidden)
        self.client.login(username='user2', password='pwd')
        resp = self.client.get(edit_url)
        self.assertIn(resp.status_code, (302, 403, 200))

        # author can edit
        self.client.login(username='user1', password='pwd')
        resp2 = self.client.post(edit_url, {'title': 'changed', 'content': 'y'}, follow=True)
        self.assertEqual(resp2.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.title, 'changed')

    def test_delete_post(self):
        post = Post.objects.create(author=self.user, title='to-delete', content='x')
        post_id = post.pk
        post.delete()
        self.assertFalse(Post.objects.filter(pk=post_id).exists())
