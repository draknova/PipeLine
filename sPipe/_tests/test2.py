import sqlite3

import PCore as pc

conn = sqlite3.connect(pc.DATABASEPATH)
conn.row_factory = sqlite3.Row  # Needed to get database as a array
cur = conn.cursor()

print cur.execute('UPDATE farm_tasks SET status="end" WHERE rowid=1')

for item in cur.execute("SELECT priority,name,status FROM farm_tasks ORDER BY status"):
    task = item
    print task