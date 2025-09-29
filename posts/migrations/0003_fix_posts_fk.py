from django.db import migrations


def forwards(apps, schema_editor):
    # This migration only targets SQLite databases where altering FK constraints
    # requires table recreation. It will be a no-op on other backends.
    conn = schema_editor.connection
    if conn.vendor != 'sqlite':
        return

    cur = conn.cursor()
    cur.execute("PRAGMA foreign_key_list('posts_post')")
    fks = cur.fetchall()
    # If FK already points to users_customuser, nothing to do
    for fk in fks:
        # FK tuple format: (id, seq, table, from, to, on_update, on_delete, match)
        if fk and fk[2] == 'users_customuser':
            return

    # Recreate posts_post with FK -> users_customuser
    cur.execute('PRAGMA foreign_keys=OFF;')
    try:
        cur.execute('BEGIN')
        cur.execute('''
            CREATE TABLE posts_post_new (
                id integer PRIMARY KEY,
                title varchar(200) NOT NULL,
                content TEXT NOT NULL,
                created_at datetime NOT NULL,
                updated_at datetime NOT NULL,
                image varchar(100),
                author_id integer NOT NULL,
                FOREIGN KEY(author_id) REFERENCES users_customuser(id) ON DELETE CASCADE
            );
        ''')
        cur.execute('''
            INSERT INTO posts_post_new (id, title, content, created_at, updated_at, image, author_id)
            SELECT id, title, content, created_at, updated_at, image, author_id FROM posts_post;
        ''')
        cur.execute('DROP TABLE posts_post;')
        cur.execute('ALTER TABLE posts_post_new RENAME TO posts_post;')
        cur.execute('COMMIT')
    finally:
        cur.execute('PRAGMA foreign_keys=ON;')


def reverse(apps, schema_editor):
    # No reliable reverse operation for this low-level schema change.
    return


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_author'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
