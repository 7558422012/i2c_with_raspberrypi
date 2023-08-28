import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Execute the DELETE statement
cursor.execute('DELETE FROM other_sensor_reading1')

# Commit the changes
conn.commit()

# Close the database connection
conn.close()
