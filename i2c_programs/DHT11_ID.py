import Adafruit_DHT
import sqlite3

# Set the sensor type and GPIO pin
sensor = Adafruit_DHT.DHT11
gpio_pin = 4  # Replace with the appropriate GPIO pin number

# Attempt to read the sensor data
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)

if humidity is not None and temperature is not None:
    sensor_id = 'DHT11'

    # Connect to the SQLite database
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    # Insert the sensor ID into the database
    cursor.execute("INSERT INTO other_sensor_reading(Id,sensorId,captureTime,updateFrequency,meanValue,minimumValue,maximumValue) VALUES (5,?,2,3,4,5,6)", (sensor_id,))
    conn.commit()

    # Close the database connection
    conn.close()
else:
    print('Failed to retrieve data from the sensor.')
