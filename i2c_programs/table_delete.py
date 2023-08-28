import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Drop the table
cursor.execute('DROP TABLE your_table_name')

# Commit the changes and close the database connection
conn.commit()
conn.close()
