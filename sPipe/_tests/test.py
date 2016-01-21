import sqlite3
conn = sqlite3.connect("/Users/draknova/Desktop/database.db")
conn.row_factory = sqlite3.Row  # Needed to get database as a array
cur = conn.cursor()

cur.execute("DROP TABLE tasks")
cur.execute("DELETE FROM jobs")
#cur.execute("DELETE FROM tasks")

# Check if table exists
if cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='jobs'").fetchone()[0] == 0:
    cur.execute("CREATE TABLE jobs(priority, name, user, status, spooled, elapsed, tasks)")
    
if cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='tasks'").fetchone()[0] == 0:
    cur.execute("CREATE TABLE tasks(priority, name, user, status, spooled, elapsed, dependance)")
    

cur.executescript("""
insert into tasks values (100,'Render frame 1','sebastien-m','waiting',0,0,'[]');
insert into tasks values (100,'Render frame 2','sebastien-m','waiting',0,0,'[0]');
insert into tasks values (100,'Render frame 3','sebastien-m','waiting',0,0,'[1]');
insert into tasks values (100,'Render frame 4','sebastien-m','waiting',0,0,'[2]');
insert into tasks values (100,'Render frame 5','sebastien-m','waiting',0,0,'[3]');
""")
cur.execute("insert into jobs values (100,'Render','sebastien-m','waiting',0,0,'[0,1,2,3,4]')")

cur.executescript("""
insert into tasks values (100,'Converting sequence in Nuke','sebastien-m','waiting',0,0,'[]');
""")
cur.execute("insert into jobs values (99,'Make Daily','sebastien-m','waiting',0,0,'[5]')")

cur.executescript("""
insert into tasks values (100,'Copying data to server','sebastien-m','waiting',0,0,'[]');
insert into tasks values (100,'Modifying database','sebastien-m','waiting',0,0,'[]');
""")
cur.execute("insert into jobs values (95,'Release','sebastien-m','waiting',0,0,'[6,7]')")

cur.executescript("""
insert into tasks values (100,'File Copy','sebastien-m','waiting',0,0,'[]');
""")
cur.execute("insert into jobs values (90,'File Copy','sebastien-m','waiting',0,0,'[8]')")


for item in cur.execute("select * from jobs"):
    print item


cur.close()

# Save and Close
conn.commit()
conn.close()