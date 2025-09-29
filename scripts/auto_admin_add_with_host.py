"""This script has been removed as it was a legacy diagnostic script.

Kept for historical reference; it should not be executed in production.
"""

import os
import sys

from django.contrib.auth import get_user_model
from django.test import Client


def main() -> None:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django

    django.setup()

    User = get_user_model()

    USERNAME = 'diag_admin'
    PASSWORD = 'diagpass'
    EMAIL = 'diag@example.com'

    if not User.objects.filter(username=USERNAME).exists():
        print('Creating superuser', USERNAME)
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    else:
        u = User.objects.get(username=USERNAME)
        u.set_password(PASSWORD)
        u.save()
        print('Updated password for', USERNAME)

    c = Client()
    logged = c.login(username=USERNAME, password=PASSWORD)
    print('Logged in:', logged)

    headers = {'HTTP_HOST': '127.0.0.1:8000'}
    try:
        r = c.get('/admin/posts/post/add/', **headers)
        print('GET add page status:', r.status_code)
        post_data = {
            'title': 'diag automated post 2',
            'content': 'content from automated script',
            '_save': 'Save',
        }
        r2 = c.post('/admin/posts/post/add/', post_data, follow=True, **headers)
        print('POST status:', r2.status_code)
        print('Redirect chain:', r2.redirect_chain)
        print('Response body (truncated):')
        print(r2.content.decode('utf-8', errors='replace')[:4096])
    except Exception as e:
        import traceback

        print('Exception during admin POST:', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
