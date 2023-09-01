import sqlite3

conn = sqlite3.connect('D:\Skill\Test\submissions.db')

cursor = conn.cursor()

cursor.execute('DELETE FROM submissions')

conn.commit()

conn.close()

print("All entries have been cleared.")
