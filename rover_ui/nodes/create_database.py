#!/usr/bin/env python3
import sqlite3

conn=sqlite3.connect('/home/melikenur/proje2_ws/src/rover_ui/nodes/rocks.db')

# create a cursor
c=conn.cursor()

# create a table
c.execute("""CREATE TABLE rocks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class TEXT,
    description TEXT
)""")

# commit our command
conn.commit()

# close the connection
conn.close()

