from django.db import migrations


def forwards(apps, schema_editor):
    conn = schema_editor.connection
    if conn.vendor != 'sqlite':
        return

    cur = conn.cursor()
    # Check if FK already points to users_customuser
    cur.execute("PRAGMA foreign_key_list('posts_comment')")
    fks = cur.fetchall()
    for fk in fks:
        # tuple: (id, seq, table, from, to, on_update, on_delete, match)
        if fk and fk[2] == 'users_customuser':
            return

    cur.execute('PRAGMA foreign_keys=OFF;')
    try:
        # Do not start an explicit transaction here: Django runs migrations inside a transaction
        # Recreate the table with the correct FK target
        cur.execute('''
            CREATE TABLE posts_comment_new (
                id integer PRIMARY KEY,
                post_id integer NOT NULL,
                author_id integer NOT NULL,
                content TEXT NOT NULL,
                created_at datetime NOT NULL,
                FOREIGN KEY(post_id) REFERENCES posts_post(id) ON DELETE CASCADE,
                FOREIGN KEY(author_id) REFERENCES users_customuser(id) ON DELETE CASCADE
            );
        ''')
        cur.execute('''
            INSERT INTO posts_comment_new (id, post_id, author_id, content, created_at)
            SELECT id, post_id, author_id, content, created_at FROM posts_comment;
        ''')
        cur.execute('DROP TABLE posts_comment;')
        cur.execute('ALTER TABLE posts_comment_new RENAME TO posts_comment;')
        # Changes are committed by Django's migration transaction
    finally:
        cur.execute('PRAGMA foreign_keys=ON;')


def reverse(apps, schema_editor):
    # No reliable reverse for this operation
    return


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_fix_admin_log_fk'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
