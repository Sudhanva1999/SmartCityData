# user_routes.py
from flask import Flask, render_template,Blueprint, request, redirect, url_for, session, jsonify
from database import mysql

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user_menu')
def user_menu():
    return render_template('citizen/citizenMenu.html', first_name = session['first_name'])


@user_routes.route('/sensor_menu')
def sensor_menu():
    return render_template('citizen/sensorData/sensorMenu.html')

@user_routes.route('/sensor_data_menu')
def sensor_data_menu():
    return render_template('citizen/sensorData/sensorDataMenu.html')

@user_routes.route('/air_quality_sensors')
def show_air_quality_sensors():
    user_mail = session['user_mail']
    airQualityCursor = mysql.cursor()
    airQualityCursor.callproc('get_air_quality_sensor_data_for_citizen',  [user_mail['email']])
    result = airQualityCursor.fetchall()
    airQualityCursor.close()
    return render_template('citizen/sensorData/airQualitySensors.html', air_quality_sensors = result)

@user_routes.route('/temp_sensors')
def show_temp_sensors():
    user_mail = session['user_mail']
    tempCursor = mysql.cursor()
    tempCursor.callproc('get_temperature_sensor_data_for_citizen',  [user_mail['email']])
    result = tempCursor.fetchall()
    print(result)
    tempCursor.close()
    return render_template('citizen/sensorData/tempSensors.html', temp_sensors = result)

@user_routes.route('/humidity_sensors')
def show_humidity_sensors():
    user_mail = session['user_mail']
    humidityCursor = mysql.cursor()
    humidityCursor.callproc('get_humidity_sensor_data_for_citizen',  [user_mail['email']])
    result = humidityCursor.fetchall()
    humidityCursor.close()
    return render_template('citizen/sensorData/humiditySensors.html', humid_sensors = result)

@user_routes.route('/light_sensors')
def shoe_light_sensors():
    lightCursor = mysql.cursor()
    user_mail = session['user_mail']
    lightCursor.callproc('get_light_sensor_data_for_citizen', [user_mail['email']] )
    result = lightCursor.fetchall()
    lightCursor.close()
    return render_template('citizen/sensorData/lightSensors.html', light_sensors = result)

@user_routes.route('/speed_sensors')
def show_speed_sensors():
    speedCursor = mysql.cursor()
    user_mail = session['user_mail']
    speedCursor.callproc('get_speed_sensor_data_for_citizen', [user_mail['email']])
    result = speedCursor.fetchall()
    speedCursor.close()
    return render_template('citizen/sensorData/speedSensors.html', speed_sensors = result)

@user_routes.route('/sensor_alerts')
def load_sensor_alerts():
    user_mail = session['user_mail']
    alertsCursor = mysql.cursor()
    alertsCursor.callproc('get_sensor_alerts_for_citizen',  [user_mail['email']])
    result = alertsCursor.fetchall()
    return render_template('citizen/sensorData/sensorAlerts.html', sensor_alerts = result)

@user_routes.route('/wifi_zones')
def show_wifi_zones():
    wifiCursor = mysql.cursor()
    user_mail = session['user_mail']
    wifiCursor.callproc('get_wifi_zones_for_user',  [user_mail['email']])
    wifi_zones = wifiCursor.fetchall()
    wifiCursor.close()
    return render_template('citizen/wifiZones.html', wifi_zones = wifi_zones)

@user_routes.route('/signals')
def show_signals():
    signalCursor = mysql.cursor()
    user_mail = session['user_mail']
    signalCursor.callproc('get_smart_signals_for_citizen',  [user_mail['email']])
    signals = signalCursor.fetchall()
    signalCursor.close()
    return render_template('citizen/signals.html', smart_signals = signals)

@user_routes.route('/parking')
def show_parking():
    parkingCursor = mysql.cursor()
    user_mail = session['user_mail']
    parkingCursor.callproc('get_charging_stations_for_citizen',  [user_mail['email']])
    stations = parkingCursor.fetchall()
    return render_template('citizen/parking.html', charging_stations = stations)

@user_routes.route('/get_machines', methods=['POST'])
def get_machines():
    cursor = mysql.cursor()
    # Get the selected charging station from the dropdown
    selected_station = request.form.get('charging_station')

    # Fetch machines for the selected charging station
    cursor.execute(f"CALL get_charging_station_machines('{selected_station}')")
    machines = cursor.fetchall()

    return render_template('citizen/parkingMachines.html', machines=machines)