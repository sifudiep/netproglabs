import sqlite3

def printTable(tableName : str):
    c.execute(f"SELECT * FROM {tableName}")
    table = c.fetchall()
    for row in table:
        print(row)

lines = ""
with open('score2.txt') as txtFile:
    lines = txtFile.readlines()

conn = sqlite3.connect("database.db")
c = conn.cursor()

# 1. Populate tables

for line in lines:
    line = line.strip('\n')
    words = line.split(" ")
    firstname = words[2]
    lastname = words[3]
    c.execute("INSERT OR IGNORE INTO persons (name1, name2) VALUES (?, ?)", (firstname, lastname))

    taskNumber = words[1]
    score = words[4]
    c.execute("SELECT id FROM persons WHERE name1 = (?) AND name2 = (?)", (firstname, lastname))
    c.execute("INSERT OR IGNORE INTO scores (personId, task, score) VALUES (?, ?, ?)", (c.fetchall()[0][0], taskNumber, score))

# printTable("persons")

# 2. SQL Queries
# Top 10 Highest Scorers
c.execute("SELECT name1, name2, sum(score) FROM persons JOIN scores on id=personId GROUP BY personId ORDER BY sum(score) DESC LIMIT 10")
# print(c.fetchall())

# Top 10 Hardest tasks
c.execute("SELECT task, sum(score) FROM scores GROUP BY task ORDER BY sum(score) LIMIT 10")
# print(c.fetchall())


conn.commit()

conn.close()




