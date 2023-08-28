import Adafruit_DHT
import datetime
import time
from flask import Flask, jsonify, request
import sqlite3
import os
import subprocess

app = Flask(__name__)

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


# Function to calculate mean, minimum, and maximum values and update them in another table
def calculate_statistics():
    # Calculate mean, minimum, and maximum values
    cursor.execute("SELECT AVG(temperature), MIN(temperature), MAX(temperature) FROM DHT11_2")
    temperature_stats = cursor.fetchone()
    cursor.execute("SELECT AVG(humidity), MIN(humidity), MAX(humidity) FROM DHT11_2")
    humidity_stats = cursor.fetchone()

    # Get the current date and time
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time().strftime('%H:%M:%S')

    # Update statistics data in another table
    query = "UPDATE other_sensor_reading1 SET meanValue = ?, minimumValue = ?, maximumValue = ?"
    values = (temperature_stats[0], temperature_stats[1], temperature_stats[2])
    cursor.execute(query, values)

    # Commit the changes to the database
    db.commit()


# API route to fetch data from the database
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        connection = sqlite3.connect(**db_config)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute("SELECT * FROM DHT11_2")

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        data = []
        for row in rows:
            data.append({
                'Date': row[1],
                'Time': str(row[2]),
                'temperature': row[3],
                'humidity': row[4]
            })

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        # Return the data as JSON response
        return jsonify(data)

    except sqlite3.Error as error:
        return jsonify({'error': str(error)})


# API route to insert data into the database
@app.route('/api/data', methods=['POST'])
def insert_data():
    try:
        connection = sqlite3.connect(**db_config)
        cursor = connection.cursor()

        # Get the data from the request body
        data = request.json

        # Extract the values
        Date = data['Date']
        Time = data['Time']
        temperature = data['temperature']
        humidity = data['humidity']

        # Execute the SQL query
        cursor.execute("INSERT INTO DHT11_2(Date, Time, temperature, humidity) VALUES (?, ?, ?, ?)",
                       (Date, Time, temperature, humidity))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        return jsonify({'message': 'Data inserted successfully'})

    except sqlite3.Error as error:
        return jsonify({'error': str(error)})


# API route to reboot the system
@app.route('/api/reboot', methods=['GET'])
def reboot_system():
    try:
        # Run the system reboot command
        subprocess.run(['sudo', 'reboot'])

        # Return a success message
        return jsonify({'message': 'System reboot initiated'})

    except Exception as e:
        # Return an error message if the reboot fails
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    # Start the data insertion and statistics calculation every second
    while True:
        insert_sensor_data()
        calculate_statistics()
        time.sleep(1)  # Sleep for 1 second
    app.run(debug=True)
