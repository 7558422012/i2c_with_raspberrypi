import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Rename the table
cursor.execute('ALTER TABLE other_sensor_reading1 RENAME TO other_sensor_reading2')

# Commit the changes and close the database connection
conn.commit()
conn.close()
