import os
import sqlite3
import os
import sqlite3
import sys
import django

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post
# The diagnostic script needs to import after django.setup in some environments; silence E402
# noqa: E402

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django

django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post
# The diagnostic script needs to import after django.setup in some environments; silence E402
# noqa: E402


def main() -> None:
    import os
    import sqlite3
    import sys
    import django

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

    from django.contrib.auth import get_user_model
    from posts.models import Post
        traceback.print_exc()

    # Also check sqlite foreign key pragma and tables
    db_path = os.path.join(PROJECT_ROOT, 'db.sqlite3')
    print('\nSQLite file:', db_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('PRAGMA foreign_keys=ON;')
    # List tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print('tables:', cur.fetchall())
    # show sample users table rows
    try:
        cur.execute('SELECT rowid,* FROM "{}" LIMIT 5'.format(User._meta.db_table))
        print('user table sample rows:', cur.fetchall())
    except Exception as exc:  # pragma: no cover - diagnostic helper
        print('Could not query user table:', exc)
    # show posts table rows
    try:
        cur.execute('SELECT rowid,* FROM posts_post LIMIT 5')
        print('posts table sample rows:', cur.fetchall())
    except Exception as exc:  # pragma: no cover - diagnostic helper
        print('Could not query posts table:', exc)
    con.close()


if __name__ == '__main__':
    main()
