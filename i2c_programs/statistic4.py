import Adafruit_DHT
import datetime
import time
import sqlite3
import os

# Set up SQLite3 connection
db = sqlite3.connect('sqlite.db')
cursor = db.cursor()

# DHT11 sensor pin
sensor = Adafruit_DHT.DHT11
pin = 4

# Attempt to read the sensor data
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('DHT11 sensor ID: {}'.format(sensor))
else:
    print('Failed to retrieve data from the sensor.')


# Set up SQLite3 connection configuration
db_path = os.path.join(os.getcwd(), 'sqlite.db')
db_config = {
    'database': db_path
}


# Function to insert sensor data into the database
def insert_sensor_data():
    # Read sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Get the current date and time
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time().strftime('%H:%M:%S')

    # Insert sensor data and current date and time into SQLite3 database
    query = "INSERT INTO DHT11_2 (Date, Time, temperature, humidity) VALUES (?, ?, ?, ?)"
    values = (current_date, current_time, temperature, humidity)
    cursor.execute(query, values)

    # Commit the changes to the database
    db.commit()

    # Calculate statistics after each data insertion
    calculate_statistics()


# Function to calculate mean, minimum, and maximum values and update other_sensor_reading1 table
def calculate_statistics():
    # Fetch the sensorId from other_sensor_reading1 table
    cursor.execute("SELECT sensorId FROM other_sensor_reading1")
    row = cursor.fetchone()

    if row is not None:
        sensor_id = row[0]
        
        # Calculate mean, minimum, and maximum values
        cursor.execute("SELECT AVG(temperature), MIN(temperature), MAX(temperature) FROM DHT11_2")
        temperature_stats = cursor.fetchone()
        cursor.execute("SELECT AVG(humidity), MIN(humidity), MAX(humidity) FROM DHT11_2")
        humidity_stats = cursor.fetchone()

        # Check for None values in statistics calculation
        temperature_mean = temperature_stats[0] if temperature_stats[0] is not None else 0
        temperature_min = temperature_stats[1] if temperature_stats[1] is not None else 0
        temperature_max = temperature_stats[2] if temperature_stats[2] is not None else 0
        humidity_mean = humidity_stats[0] if humidity_stats[0] is not None else 0
        humidity_min = humidity_stats[1] if humidity_stats[1] is not None else 0
        humidity_max = humidity_stats[2] if humidity_stats[2] is not None else 0

        # Update the row with the new statistics
        query = "UPDATE other_sensor_reading1 SET meanValue = ?, minimumValue = ?, maximumValue = ? WHERE sensorId = ?"
        values = (temperature_mean, temperature_min, temperature_max, sensor_id)
        cursor.execute(query, values)
        db.commit()


if __name__ == '__main__':
    # Start the data insertion and statistics calculation every second
    while True:
        insert_sensor_data()
        time.sleep(1)  # Sleep for 1 second
