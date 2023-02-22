import sqlite3
from contextlib import closing
from objects import Paint, Project

DBFILE = "data/paintDB.db"
conn = None

def connect():
    global conn
    conn = sqlite3.connect(DBFILE)
    conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def checkDatabasePaints():
    query = '''CREATE TABLE IF NOT EXISTS paints (
    paint_id TEXT NOT NULL UNIQUE PRIMARY KEY, 
    paint_name TEXT NOT NULL UNIQUE,
    paint_type TEXT, pot_amount INTEGER,
    pot_status TEXT, paint_colour TEXT, 
    hexcode TEXT, brand TEXT);'''

    with closing(conn.cursor()) as c:
        c.execute(query)

def checkDatabaseProject():
    query = '''CREATE TABLE IF NOT EXISTS projects (
    name TEXT NOT NULL,
    system TEXT,
     TEXT);'''

    with closing(conn.cursor()) as c:
        c.execute(query, ())

def makePaint(row):
    return Paint(row["paint_id"], row["paint_name"], row["paint_type"], row["pot_amount"],
                 row["pot_status"], row["paint_colour"], row["hexcode"], row["brand"])

def getCount():
    query = '''
    SELECT SUM(pot_amount) 
    FROM paints'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchone()

    return results[0]

def getLow():
    query = '''
    SELECT * 
    FROM paints 
    WHERE pot_status = "Low" AND pot_amount = 1'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    paints = []
    for row in results:
        paints.append(makePaint(row))

    return paints

def getDepleted():
    query = '''
    SELECT *
    FROM paints
    WHERE pot_amount = 0'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    paints = []
    for row in results:
        paints.append(makePaint(row))

    return paints

def getColours():
    query = '''
        SELECT COUNT(*) 
        FROM paints
        WHERE pot_amount > 0'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchone()

    return results[0]

def getPaints():
    query = '''
    SELECT * 
    FROM paints 
    ORDER BY paint_id'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    paints = []
    for row in results:
        paints.append(makePaint(row))

    return paints

def getPaint(paint_id):
    query = '''SELECT * FROM paints WHERE paint_id = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (paint_id,))
        result = c.fetchall()

    paint = []
    for row in result:
        paint.append(makePaint(row))

    return paint[0]

def addPaint(paint):
    print(f'Adding {paint.paint_id}')
    query = '''INSERT INTO paints (paint_id, paint_name, paint_type,
            pot_amount, pot_status, paint_colour, hexcode, brand)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    with closing(conn.cursor()) as c:
        c.execute(query, (paint.paint_id, paint.paint_name, paint.paint_type, paint.pot_amount,
                          paint.pot_status, paint.paint_colour, paint.hexcode, paint.brand))
        conn.commit()

def updatePaint(paint_id, paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode, brand):
    print(f'Updating {paint_id}')
    query = '''UPDATE paints
                SET paint_name = ?, paint_type = ?, pot_amount = ?,
                 pot_status = ?, paint_colour = ?, hexcode = ?,
                 brand = ?
                WHERE paint_id = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (paint_name, paint_type, pot_amount, pot_status, paint_colour, hexcode, brand, paint_id))
        conn.commit()

def deletePaint(paint_id):
    print(f'Deleting {paint_id}')
    query = '''DELETE FROM paints WHERE paint_id = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (paint_id,))
        conn.commit()

def makeProject(row):
    parts = getProjectParts(row["project_id"])
    return Project(row["project_id"], row["project_name"], row["system"], parts)

def getProjects():
    query = '''
    SELECT *
    FROM projects
    ORDER BY project_id'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    projects = []
    for row in results:
        projects.append(makeProject(row))

    return projects

def getProjectParts(project_id):

    query = '''SELECT * FROM projects_paints WHERE project_id = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (project_id,))
        results = c.fetchall()

    parts = []

    for result in results:
        part = [getPaint(result["paint_id"]), result["notes"]]

        parts.append(part)

    return parts
