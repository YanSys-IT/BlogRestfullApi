import sqlite3
DB = r'd:\PROJECTS\blog\db.sqlite3'
con = sqlite3.connect(DB)
cur = con.cursor()
print('== tables ==')
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
for r in cur.fetchall():
    print(r)

print('\n== auth_user rows ==')
try:
    cur.execute('SELECT rowid,* FROM auth_user')
    for r in cur.fetchall():
        print(r)
except Exception as e:
    print('auth_user query failed:', e)

print('\n== users_customuser rows ==')
try:
    cur.execute('SELECT rowid,* FROM users_customuser')
    for r in cur.fetchall():
        print(r)
except Exception as e:
    print('users_customuser query failed:', e)

print('\n== posts_post schema ==')
cur.execute("PRAGMA table_info('posts_post')")
for r in cur.fetchall():
    print(r)

print('\n== posts_post foreign keys ==')
cur.execute("PRAGMA foreign_key_list('posts_post')")
for r in cur.fetchall():
    print(r)

con.close()
