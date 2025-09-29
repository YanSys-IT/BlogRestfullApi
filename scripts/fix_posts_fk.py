import os
import sqlite3

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.join(PROJECT_ROOT, 'db.sqlite3')
print('DB:', DB)
con = sqlite3.connect(DB)
cur = con.cursor()

print('PRAGMA foreign_keys before:')
cur.execute("PRAGMA foreign_key_list('posts_post')")
print(cur.fetchall())

print('Beginning migration to recreate posts_post with FK -> users_customuser')
cur.execute('PRAGMA foreign_keys=OFF')
con.commit()
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
    print('Recreation done')
finally:
    cur.execute('PRAGMA foreign_keys=ON')
    con.commit()

print('PRAGMA foreign_keys after:')
cur.execute("PRAGMA foreign_key_list('posts_post')")
print(cur.fetchall())
con.close()
print('All done')
