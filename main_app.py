from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql.cursors
import json
from datetime import date

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Sudhanva1999'
app.config['MYSQL_DB'] = 'smartCityData'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Use dictionary cursor

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

def default_encoder(obj):
    # Custom encoder for non-serializable objects
    if isinstance(obj, date):
        return obj.isoformat()  # Convert date to string
    raise TypeError("Type not serializable")

@app.route('/')
def index():
    if 'username' in session:
        role = get_user_role(session['username'])
        if role == 'citizen':
            return redirect(url_for('user_menu'))
        elif role == 'admin':
            return redirect(url_for('admin_menu'))
    
    return render_template('/loggedOut.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        validateCursor = mysql.cursor()
        function_call = "SELECT validate_login('"+ username +"','"+ password_candidate + "')"
        validateCursor.execute(function_call)
        result = validateCursor.fetchone()
        
        
        if list(result.values() )[0]  == 1:
            # Password is correct, log in the user
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Invalid login
             return render_template('/invalidLogin.html')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('/loggedOut.html')



@app.route('/admin_menu')
def admin_menu():
    return render_template('admin/adminMenu.html')

@app.route('/data_management_menu')
def data_management_menu():
    return render_template('admin/dataManagement/dataManagementMenu.html')

@app.route('/manage_users')
def manage_user():
    userCursor = mysql.cursor()
    userCursor.execute('SELECT * FROM citizen')
    citizens = userCursor.fetchall()
    userCursor.close()
    return render_template('admin/dataManagement/manageUser/manageUsers.html', citizens=citizens)

# Edit Page - Prefilled form for editing
@app.route('/edit/<email>', methods=['GET', 'POST'])
def edit(email):
    # Fetch citizen details by email
    userCursor = mysql.cursor()
    userCursor.execute('SELECT * FROM citizen WHERE email=%s', (email,))
    citizen = userCursor.fetchone()

    if request.method == 'POST':
        # Update citizen data in the database
        with mysql.cursor() as cursor:
            update_query = """
                UPDATE citizen
                SET username=%s, password=%s, first_name=%s, last_name=%s,
                    phone_no=%s, user_type=%s, user_status=%s, age=%s, city_name=%s
                WHERE email=%s
            """
            cursor.execute(update_query, (
                request.form['username'],
                request.form['password'],
                request.form['first_name'],
                request.form['last_name'],
                request.form['phone_no'],
                request.form['user_type'],
                request.form['user_status'],
                request.form['age'],
                request.form['city_name'],
                email
            ))
            mysql.commit()
            return redirect(url_for('manage_user'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageUser/citizenEdit.html', citizen=citizen, cities=cities)

# Add Page 
@app.route('/addUser', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Update citizen data in the database
        with mysql.cursor() as cursor:
            insert_query = """
                INSERT INTO citizen VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s);
            """
            cursor.execute(insert_query, (
                request.form['email'],
                request.form['username'],
                request.form['password'],
                request.form['first_name'],
                request.form['last_name'],
                request.form['phone_no'],
                request.form['user_type'],
                request.form['user_status'],
                request.form['age'],
                request.form['city_name'],
            ))
            mysql.commit()
            return redirect(url_for('manage_user'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageUser/addUser.html', cities=cities)

# Delete Citizen
@app.route('/delete/<email>')
def delete(email):
    # Delete citizen from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM citizen WHERE email=%s', (email))
        mysql.commit()
    return redirect(url_for('manage_user'))



@app.route('/manage_cameras')
def manage_camera():
    cameraCursor = mysql.cursor()
    cameraCursor.execute('SELECT * FROM surveillance_cameras')
    cameras = cameraCursor.fetchall()
    cameraCursor.close()
    return render_template('admin/dataManagement/manageCameras/manageCameras.html', cameras=cameras)

# Edit Page - Prefilled form for editing
@app.route('/editCamera/<serial_number>', methods=['GET', 'POST'])
def editCamera(serial_number):
    # Fetch citizen details by email
    camCursor = mysql.cursor()
    camCursor.execute('SELECT * FROM surveillance_cameras WHERE serial_number=%s', (serial_number))
    camera = camCursor.fetchone()

    if request.method == 'POST':
        # Update citizen data in the database
        with mysql.cursor() as cursor:
            update_query = """
                UPDATE surveillance_cameras
                SET camera_type=%s, installation_date=%s, camera_status=%s,
                    camera_resolution=%s, field_of_view_angle=%s, connectivity_type=%s, power_source=%s, city_name=%s
                WHERE serial_number=%s
            """
            cursor.execute(update_query, (
                request.form['camera_type'],
                request.form['installation_date'],
                request.form['camera_status'],
                request.form['camera_resolution'],
                request.form['field_of_view_angle'],
                request.form['connectivity_type'],
                request.form['power_source'],
                request.form['city_name'],
                serial_number
            ))
            mysql.commit()
            return redirect(url_for('manage_camera'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageCameras/editCamera.html', cameras = camera, cities=cities)

# Add Page 
@app.route('/addCamera', methods=['GET', 'POST'])
def addCamera():
    if request.method == 'POST':
        # Update citizen data in the database
        with mysql.cursor() as cursor:
            insert_query = """
                INSERT INTO surveillance_cameras VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s);
            """
            cursor.execute(insert_query, (
                request.form['serial_number'],
                request.form['camera_type'],
                request.form['installation_date'],
                request.form['camera_status'],
                request.form['camera_resolution'],
                request.form['field_of_view_angle'],
                request.form['connectivity_type'],
                request.form['power_source'],
                request.form['city_name'],
            ))
            mysql.commit()
            return redirect(url_for('manage_camera'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageCameras/addCamera.html', cities=cities)

# Delete Citizen
@app.route('/deleteCamera/<serial_number>')
def deleteCamera(serial_number):
    # Delete citizen from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM surveillance_cameras WHERE serial_number=%s', (serial_number))
        mysql.commit()
    return redirect(url_for('manage_camera'))

# Manage Signals Page
@app.route('/manage_signals')
def manage_signal():
    signalCursor = mysql.cursor()
    signalCursor.execute('SELECT * FROM smart_signal')
    signals = signalCursor.fetchall()
    signalCursor.close()
    return render_template('admin/dataManagement/manageSignals/manageSignals.html', signals=signals)

# Edit Page - Prefilled form for editing
@app.route('/editSignal/<serial_number>', methods=['GET', 'POST'])
def editSignal(serial_number):
    # Fetch signal details by serial number
    signalCursor = mysql.cursor()
    signalCursor.execute('SELECT * FROM smart_signal WHERE serial_number=%s', (serial_number,))
    signal = signalCursor.fetchone()

    if request.method == 'POST':
        # Update signal data in the database
        with mysql.cursor() as cursor:
            update_query = """
                UPDATE smart_signal
                SET installation_date=%s, connectivity_type=%s,
                    schedule_start_time=%s, schedule_end_time=%s, city_name=%s
                WHERE serial_number=%s
            """
            cursor.execute(update_query, (
                request.form['installation_date'],
                request.form['connectivity_type'],
                request.form['schedule_start_time'],
                request.form['schedule_end_time'],
                request.form['city_name'],
                serial_number
            ))
            mysql.commit()
            return redirect(url_for('manage_signal'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageSignals/editSignal.html', signal=signal, cities=cities)

# Add Page
@app.route('/addSignal', methods=['GET', 'POST'])
def addSignal():
    if request.method == 'POST':
        # Insert signal data into the database
        with mysql.cursor() as cursor:
            insert_query = """
                INSERT INTO smart_signal VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                request.form['serial_number'],
                request.form['installation_date'],
                request.form['connectivity_type'],
                request.form['schedule_start_time'],
                request.form['schedule_end_time'],
                request.form['city_name'],
            ))
            mysql.commit()
            return redirect(url_for('manage_signal'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageSignals/addSignal.html', cities=cities)

# Delete Signal
@app.route('/deleteSignal/<serial_number>')
def deleteSignal(serial_number):
    # Delete signal from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM smart_signal WHERE serial_number=%s', (serial_number,))
        mysql.commit()
    return redirect(url_for('manage_signal'))

# Manage WiFi Zones Page
@app.route('/manage_wifi_zones')
def manage_wifi_zones():
    zone_cursor = mysql.cursor()
    zone_cursor.execute('SELECT * FROM wifi_zones')
    wifi_zones = zone_cursor.fetchall()
    zone_cursor.close()
    return render_template('admin/dataManagement/manageWiFi/manageWiFi.html', wifi_zones=wifi_zones)

# Edit Page - Prefilled form for editing
@app.route('/editWifi/<zone_id>', methods=['GET', 'POST'])
def editWifi(zone_id):
    # Fetch WiFi zone details by zone_id
    zone_cursor = mysql.cursor()
    zone_cursor.execute('SELECT * FROM wifi_zones WHERE zone_id=%s', (zone_id,))
    wifi_zone = zone_cursor.fetchone()

    if request.method == 'POST':
        # Update WiFi zone data in the database
        with mysql.cursor() as cursor:
            update_query = """
                UPDATE wifi_zones
                SET zone_name=%s, coverage_area=%s,
                    wifi_status=%s, zone_security=%s, city_name=%s
                WHERE zone_id=%s
            """
            cursor.execute(update_query, (
                request.form['zone_name'],
                request.form['coverage_area'],
                request.form['wifi_status'],
                request.form['zone_security'],
                request.form['city_name'],
                zone_id
            ))
            mysql.commit()
            return redirect(url_for('manage_wifi_zones'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageWiFi/editWiFi.html', zone=wifi_zone, cities=cities)

# Add Page
@app.route('/addZone', methods=['GET', 'POST'])
def add_wifi_zone():
    if request.method == 'POST':
        # Insert WiFi zone data into the database
        with mysql.cursor() as cursor:
            insert_query = """
                INSERT INTO wifi_zones (zone_name, coverage_area, wifi_status, zone_security, city_name)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                request.form['zone_name'],
                request.form['coverage_area'],
                request.form['wifi_status'],
                request.form['zone_security'],
                request.form['city_name'],
            ))
            mysql.commit()
            return redirect(url_for('manage_wifi_zones'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageWiFi/addWiFi.html', cities=cities)

# Delete WiFi Zone
@app.route('/deleteWiFiZone/<zone_id>')
def deleteWiFiZone(zone_id):
    # Delete WiFi zone from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM wifi_zones WHERE zone_id=%s', (zone_id,))
        mysql.commit()
    return redirect(url_for('manage_wifi_zones'))


@app.route('/user_menu')
def user_menu():
    return render_template('citizen/citizenMenu.html')


@app.route('/sensor_menu')
def sensor_menu():
    return render_template('citizen/sensorData/sensorMenu.html')

@app.route('/sensor_data_menu')
def sensor_data_menu():
    return render_template('citizen/sensorData/sensorDataMenu.html')

@app.route('/air_quality_sensors')
def show_air_quality_sensors():
    airQualityCursor = mysql.cursor()
    airQualityCursor.callproc('get_air_quality_sensor_data_for_citizen', [session['username']])
    result = airQualityCursor.fetchall()
    airQualityCursor.close()
    return render_template('citizen/sensorData/airQualitySensors.html', air_quality_sensors = result)

@app.route('/temp_sensors')
def show_temp_sensors():
    tempCursor = mysql.cursor()
    tempCursor.callproc('get_temperature_sensor_data_for_citizen', [session['username']])
    result = tempCursor.fetchall()
    tempCursor.close()
    return render_template('citizen/sensorData/tempSensors.html', temp_sensors = result)

@app.route('/humidity_sensors')
def show_humidity_sensors():
    humidityCursor = mysql.cursor()
    humidityCursor.callproc('get_humidity_sensor_data_for_citizen', [session['username']])
    result = humidityCursor.fetchall()
    humidityCursor.close()
    return render_template('citizen/sensorData/humiditySensors.html', humid_sensors = result)

@app.route('/light_sensors')
def shoe_light_sensors():
    lightCursor = mysql.cursor()
    lightCursor.callproc('get_light_sensor_data_for_citizen', [session['username']])
    result = lightCursor.fetchall()
    lightCursor.close()
    return render_template('citizen/sensorData/lightSensors.html', light_sensors = result)

@app.route('/speed_sensors')
def show_speed_sensors():
    speedCursor = mysql.cursor()
    speedCursor.callproc('get_speed_sensor_data_for_citizen', [session['username']])
    result = speedCursor.fetchall()
    speedCursor.close()
    return render_template('citizen/sensorData/speedSensors.html', speed_sensors = result)

@app.route('/sensor_alerts')
def load_sensor_alerts():
    alertsCursor = mysql.cursor()
    alertsCursor.callproc('get_sensor_alerts_for_citizen', [session['username']])
    result = alertsCursor.fetchall()
    return render_template('citizen/sensorData/sensorAlerts.html', sensor_alerts = result)

@app.route('/wifi_zones')
def show_wifi_zones():
    wifiCursor = mysql.cursor()
    wifiCursor.callproc('get_wifi_zones_for_user', [session['username']])
    wifi_zones = wifiCursor.fetchall()
    wifiCursor.close()
    return render_template('citizen/wifiZones.html', wifi_zones = wifi_zones)

@app.route('/signals')
def show_signals():
    signalCursor = mysql.cursor()
    signalCursor.callproc('get_smart_signals_for_citizen', [session['username']])
    signals = signalCursor.fetchall()
    signalCursor.close()
    return render_template('citizen/signals.html', smart_signals = signals)

@app.route('/parking')
def show_parking():
    parkingCursor = mysql.cursor()
    parkingCursor.callproc('get_charging_stations_for_citizen', [session['username']])
    stations = parkingCursor.fetchall()
    return render_template('citizen/parking.html', charging_stations = stations)

@app.route('/get_machines', methods=['POST'])
def get_machines():
    cursor = mysql.cursor()
    # Get the selected charging station from the dropdown
    selected_station = request.form.get('charging_station')

    # Fetch machines for the selected charging station
    cursor.execute(f"CALL get_charging_station_machines('{selected_station}')")
    machines = cursor.fetchall()

    return render_template('citizen/parkingMachines.html', machines=machines)

def get_user_role(username):
    with mysql.cursor() as cursor:
        cursor.execute("SELECT user_type FROM citizen WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result['user_type']
    return None

if __name__ == '__main__':
    app.run(debug=True)


