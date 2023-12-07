# admin_routes.py
from flask import Flask, render_template,Blueprint, request, redirect, url_for, make_response, session
from database import mysql
import json

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin_menu')
def admin_menu():
    return render_template('admin/adminMenu.html', first_name = session["first_name"])


@admin_routes.route('/data_management_menu')
def data_management_menu():
    return render_template('admin/dataManagement/dataManagementMenu.html')

@admin_routes.route('/manage_users')
def manage_user():
    userCursor = mysql.cursor()
    userCursor.execute('SELECT * FROM citizen')
    citizens = userCursor.fetchall()
    userCursor.close()
    return render_template('admin/dataManagement/manageUser/manageUsers.html', citizens=citizens)

# Edit Page - Prefilled form for editing
@admin_routes.route('/edit/<email>', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_user'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageUser/citizenEdit.html', citizen=citizen, cities=cities)

# Add Page 
@admin_routes.route('/addUser', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_user'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageUser/addUser.html', cities=cities)

# Delete Citizen
@admin_routes.route('/delete/<email>')
def delete(email):
    # Delete citizen from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM citizen WHERE email=%s', (email))
        mysql.commit()
    return redirect(url_for('admin_routes.manage_user'))



@admin_routes.route('/manage_cameras')
def manage_camera():
    cameraCursor = mysql.cursor()
    cameraCursor.execute('SELECT * FROM surveillance_cameras')
    cameras = cameraCursor.fetchall()
    cameraCursor.close()
    return render_template('admin/dataManagement/manageCameras/manageCameras.html', cameras=cameras)

# Edit Page - Prefilled form for editing
@admin_routes.route('/editCamera/<serial_number>', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_camera'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageCameras/editCamera.html', cameras = camera, cities=cities)

# Add Page 
@admin_routes.route('/addCamera', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_camera'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageCameras/addCamera.html', cities=cities)

# Delete Citizen
@admin_routes.route('/deleteCamera/<serial_number>')
def deleteCamera(serial_number):
    # Delete citizen from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM surveillance_cameras WHERE serial_number=%s', (serial_number))
        mysql.commit()
    return redirect(url_for('admin_routes.manage_camera'))

# Manage Signals Page
@admin_routes.route('/manage_signals')
def manage_signal():
    signalCursor = mysql.cursor()
    signalCursor.execute('SELECT * FROM smart_signal')
    signals = signalCursor.fetchall()
    signalCursor.close()
    return render_template('admin/dataManagement/manageSignals/manageSignals.html', signals=signals)

# Edit Page - Prefilled form for editing
@admin_routes.route('/editSignal/<serial_number>', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_signal'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageSignals/editSignal.html', signal=signal, cities=cities)

# Add Page
@admin_routes.route('/addSignal', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_signal'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageSignals/addSignal.html', cities=cities)

# Delete Signal
@admin_routes.route('/deleteSignal/<serial_number>')
def deleteSignal(serial_number):
    # Delete signal from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM smart_signal WHERE serial_number=%s', (serial_number,))
        mysql.commit()
    return redirect(url_for('admin_routes.manage_signal'))

# Manage WiFi Zones Page
@admin_routes.route('/manage_wifi_zones')
def manage_wifi_zones():
    zone_cursor = mysql.cursor()
    zone_cursor.execute('SELECT * FROM wifi_zones')
    wifi_zones = zone_cursor.fetchall()
    zone_cursor.close()
    return render_template('admin/dataManagement/manageWiFi/manageWiFi.html', wifi_zones=wifi_zones)

# Edit Page - Prefilled form for editing
@admin_routes.route('/editWifi/<zone_id>', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_wifi_zones'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageWiFi/editWiFi.html', zone=wifi_zone, cities=cities)

# Add Page
@admin_routes.route('/addZone', methods=['GET', 'POST'])
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
            return redirect(url_for('admin_routes.manage_wifi_zones'))

    # Fetch all cities for dropdown
    with mysql.cursor() as cursor:
        cursor.execute('SELECT city_name FROM city')
        cities = [city['city_name'] for city in cursor.fetchall()]

    return render_template('admin/dataManagement/manageWiFi/addWiFi.html', cities=cities)

# Delete WiFi Zone
@admin_routes.route('/deleteWiFiZone/<zone_id>')
def deleteWiFiZone(zone_id):
    # Delete WiFi zone from the database
    with mysql.cursor() as cursor:
        cursor.execute('DELETE FROM wifi_zones WHERE zone_id=%s', (zone_id,))
        mysql.commit()
    return redirect(url_for('admin_routes.manage_wifi_zones'))

