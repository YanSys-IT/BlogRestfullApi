import sqlite3
DB = r'd:\PROJECTS\blog\db.sqlite3'
con = sqlite3.connect(DB)
cur = con.cursor()

print('== foreign_key_check ==')
try:
    cur.execute('PRAGMA foreign_key_check;')
    rows = cur.fetchall()
    if not rows:
        print('No FK violations (empty list)')
    else:
        for r in rows:
            print(r)
except Exception as e:
    print('Error running foreign_key_check:', e)

print('\n== foreign key lists for tables ==')
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
for (t,) in cur.fetchall():
    try:
        cur.execute(f"PRAGMA foreign_key_list('{t}')")
        fks = cur.fetchall()
        if fks:
            print(t, '->', fks)
    except Exception as e:
        print('Could not get fk for', t, e)

con.close()
