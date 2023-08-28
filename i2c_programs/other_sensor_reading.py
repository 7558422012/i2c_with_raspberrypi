import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Define the values to be inserted
sensor_id = 11
update_frequency = 5
mean_value = 0.0
minimum_value = 0.0
maximum_value = 0.0

# Execute the INSERT query
cursor.execute("INSERT INTO other_sensor_reading1 (sensorId, updateFrequency, meanValue, minimumValue, maximumValue) VALUES (?, ?, ?, ?, ?)",
               (sensor_id, update_frequency, mean_value, minimum_value, maximum_value))

# Commit the changes and close the database connection
conn.commit()
conn.close()
