#Store data into mysql as well as upload into API
import Adafruit_DHT
import mysql.connector
import datetime
import mysql.connector
import time
from flask import Flask, jsonify, request
import mysql.connector
import os
import subprocess
# Set up MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tushar111",
    database="sphinx"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# DHT11 sensor pin
sensor = Adafruit_DHT.DHT11
pin = 4

# Read sensor data
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#Get the current date and time
current_datetime = datetime.datetime.now()
current_time = time.strftime('%H:%M:%S')

# Insert sensor data and current date and time into MySQL database
query = "INSERT INTO SENSOR3(Date,Time,temperature, humidity) VALUES (%s, %s, %s,%s)"
values = (current_datetime,current_time,temperature, humidity)
cursor.execute(query, values)


# Commit the changes to the database
db.commit()

# Close the database connection
db.close()

# Set up MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tushar111',
    'database': 'sphinx'
}


app = Flask(__name__)


# API route to fetch data from the database
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute("SELECT * FROM SENSOR3")

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        data = []
        for row in rows:
            data.append({
                'Date': row[1],
                'Time':str(row[2]),
                'temperature':row[3],
                'humidity':row[4]
            })

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        # Return the data as JSON response
        return jsonify(data)

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})


# API route to insert data into the database
@app.route('/api/data', methods=['POST'])
def insert_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Get the data from the request body
        data = request.json

        # Extract the values
        Date = data['Date']
        Time = time['Time']
        temperature= data['temperature']
        humidity=data['humidity']


        # Execute the SQL query
        cursor.execute("INSERT INTO SENSOR3(Date,Time,temperature,humidity) VALUES (%s,%s,%s,%s)", (Date,Time,temperature,humidity))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and database connection
        cursor.close()
        connection.close()

        return jsonify({'message': 'Data inserted successfully'})

    except mysql.connector.Error as error:
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
    app.run(debug=True)
