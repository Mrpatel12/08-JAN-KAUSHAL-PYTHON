import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')

def main():
    if not os.path.exists(DB_PATH):
        print('db.sqlite3 not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ensure django_migrations table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations';")
    if not cur.fetchone():
        print('django_migrations table not found')
        conn.close()
        return

    app = 'accounts'
    name = '0001_initial'
    cur.execute('SELECT 1 FROM django_migrations WHERE app=? AND name=?', (app, name))
    if cur.fetchone():
        print('accounts.0001_initial already recorded')
        conn.close()
        return

    applied = datetime.utcnow().isoformat(sep=' ', timespec='seconds')
    cur.execute('INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)', (app, name, applied))
    conn.commit()
    conn.close()
    print(f'Inserted migration record for {app}.{name} (applied={applied})')

if __name__ == '__main__':
    main()
