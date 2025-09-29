from django.db import migrations


def forwards(apps, schema_editor):
    conn = schema_editor.connection
    if conn.vendor != 'sqlite':
        return
    cur = conn.cursor()
    # Check current FK target
    cur.execute("PRAGMA foreign_key_list('django_admin_log')")
    fks = cur.fetchall()
    for fk in fks:
        if fk and fk[2] == 'users_customuser':
            return

    cur.execute('PRAGMA foreign_keys=OFF;')
    try:
        # Execute table recreation statements within the migration's transaction
        cur.execute('''
            CREATE TABLE django_admin_log_new (
                id integer PRIMARY KEY,
                action_time datetime NOT NULL,
                object_id text,
                object_repr varchar(200) NOT NULL,
                action_flag smallint NOT NULL,
                change_message text NOT NULL,
                content_type_id integer,
                user_id integer NOT NULL,
                FOREIGN KEY(content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
                FOREIGN KEY(user_id) REFERENCES users_customuser(id) ON DELETE CASCADE
            );
        ''')
        cur.execute('''
            INSERT INTO django_admin_log_new (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id)
            SELECT id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id FROM django_admin_log;
        ''')
        cur.execute('DROP TABLE django_admin_log;')
        cur.execute('ALTER TABLE django_admin_log_new RENAME TO django_admin_log;')
    finally:
        cur.execute('PRAGMA foreign_keys=ON;')


def reverse(apps, schema_editor):
    # No reverse
    return


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_fix_posts_fk'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
