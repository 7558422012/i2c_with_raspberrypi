import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Create the table with the current time as the default value for captureTime
cursor.execute('''CREATE TABLE other_sensor_reading1(
                    Id INTEGER PRIMARY KEY,
                    sensorId REAL,
                    captureTime TEXT DEFAULT (datetime('now', 'localtime')),
                    updateFrequency INTEGER,
                    meanValue REAL,
                    minimumValue REAL,
                    maximumValue REAL
                )''')

# Commit the changes and close the database connection
conn.commit()
conn.close()
