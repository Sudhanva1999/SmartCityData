# report_routes.py
from flask import Flask, render_template,Blueprint, request, redirect, url_for, make_response
from database import mysql
import matplotlib.pyplot as plt
import base64
import os
from io import BytesIO
import datetime


report_routes = Blueprint('report_routes', __name__)

from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Function to create a bubble chart and return its base64 encoding
def create_bubble_chart(data):
    plt.switch_backend('Agg') 
    cities = [entry['CityName'] for entry in data]
    signals_count = [entry['TrafficSignalsCount'] for entry in data]
    alerts_count = [entry['SpeedSensorAlertsCount'] for entry in data]
    fig, ax = plt.subplots()
    plt.scatter(signals_count, alerts_count)
    plt.title("Number of speed violations compared to Number of signals in city.")
    plt.xlabel("Number of signals in city.")
    plt.ylabel("Number of speed violations in city.")

    for i, city in enumerate(cities):
        ax.annotate(city, (signals_count[i], alerts_count[i]), fontsize=8, ha='right')

    # Create a buffer to save the plot
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image as base64
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')

    return encoded_image

def create_sensor_chart(sensor_type, sensor_data):
    plt.switch_backend('Agg') 
    # Extracting dates and values from sensor_data
    dates = [entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S') for entry in sensor_data]
    values = [float(entry[sensor_type]) for entry in sensor_data]  # Convert Decimal to float

    # Convert dates to datetime objects
    date_objects = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]
    print(date_objects)
    print(type(date_objects))
    in_order_date = sorted(date_objects)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(in_order_date, values, label=sensor_type, marker='o')  # Added marker for data points
    plt.xlabel('Timestamp')
    plt.ylabel(f'{sensor_type} Data')
    plt.title(f'{sensor_type} Data Over Time')
    plt.legend()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image


def fetch_sensor_data(sensor_type, selected_city):
    sensor_type = sensor_type.lower()
    query = ""
    cursor = mysql.cursor()
    # Fetch sensor data from MySQL using a cursor
    if sensor_type == "temperature":
        query = "CALL GetTemperatureSensorsInCity('" + selected_city + "');"
    elif sensor_type == "humidity":
        query = "CALL GetHumiditySensorsInCity('" + selected_city + "');"
    elif sensor_type == "light":
        query = "CALL GetLightSensorsInCity('" + selected_city + "');"
    elif sensor_type == "air_quality":
        query = "CALL AirQualitySensorsInCity('" + selected_city + "');"
    elif sensor_type == "speed":
        query = "CALL SpeedSensorsInCity('" + selected_city + "');"

    cursor.execute(query)
    sensor_data = cursor.fetchall()
    cursor.close()

    return sensor_data

def create_bar_chart(city_names, populations):
    plt.switch_backend('Agg') 
    plt.figure(figsize=(10, 6))
    plt.bar(city_names, populations, color='skyblue')
    plt.xlabel('City Name')
    plt.ylabel('Population')
    plt.title('Population Distribution Across Cities')
    plt.xticks(rotation=45, ha='right')
    
    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image

def create_elevation_chart(city_names, elevations):
    plt.switch_backend('Agg') 
    plt.figure(figsize=(10, 6))
    plt.bar(city_names, elevations, color='skyblue')
    plt.xlabel('City Name')
    plt.ylabel('Elevation in meters')
    plt.title('City wise Elevation Distribution')
    plt.xticks(rotation=45, ha='right')
    
    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    
    # Encode the image as base64
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image



@report_routes.route('/report_menu')
def report_menu():
    return render_template('admin/reports/reportMenu.html')

@report_routes.route('/report_population_city')
def report_population_city():
    cursor = mysql.cursor()
    try:
        cursor.execute('CALL GetPopulationDistribution()')
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    # Extracting data for the chart
    city_names = [row['city_name'] for row in data]
    populations = [row['population'] for row in data]
    chart_image = create_bar_chart(city_names, populations)

    rendered_template = render_template('admin/reports/populationDistribution.html', chart_image=chart_image, data=data)
    return rendered_template

@report_routes.route('/report_elevation_distribution')
def report_elevation_city():
    cursor = mysql.cursor()
    try:
        cursor.execute('CALL GetElevationDistribution()')
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    # Extracting data for the chart
    city_names = [row['city_name'] for row in data]
    elevations = [row['elevation'] for row in data]
    chart_image = create_elevation_chart(city_names, elevations)

    rendered_template = render_template('admin/reports/elevationDistribution.html', chart_image=chart_image, data=data)
    return rendered_template

@report_routes.route('/get_all_sensors', methods=['GET', 'POST'])
def get_all_sensors():
    selected_city = request.form.get('city_select')

    temperature_data = fetch_sensor_data('Temperature', selected_city)
    humidity_data = fetch_sensor_data('Humidity', selected_city)
    light_data = fetch_sensor_data('Light', selected_city)
    air_quality_data = fetch_sensor_data('Air_Quality', selected_city)
    speed_data = fetch_sensor_data('Speed', selected_city)

    temperature_chart = create_sensor_chart('temperature_data', temperature_data)
    humidity_chart = create_sensor_chart('humidity_data', humidity_data)
    light_chart = create_sensor_chart('light_intensity_data', light_data)
    air_quality_chart = create_sensor_chart('air_quality_data', air_quality_data)
    speed_chart = create_sensor_chart('speed_data', speed_data)

    return render_template(
        'admin/reports/sensorDataReports.html',
        temperature_chart=temperature_chart,
        humidity_chart=humidity_chart,
        light_chart=light_chart,
        air_quality_chart=air_quality_chart,
        speed_chart=speed_chart
    )
    
@report_routes.route('/sensor_data_vis')
def sensor_data_vis():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM city")
    cities = [city['city_name'] for city in cursor.fetchall()]
    return render_template('admin/reports/citySelect.html', cities=cities)

   

@report_routes.route('/report_speed_signal')
def report_speed_signal():
    cursor =mysql.cursor()
    cursor.callproc('GetTrafficSignalsAndSpeedSensorAlerts')
    data = cursor.fetchall()
    cursor.close()
    chart_image = create_bubble_chart(data)

    return render_template('admin/reports/speedSignalRelation.html', chart_image=chart_image)



    
