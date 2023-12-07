from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql.cursors
import json
from datetime import date
from admin_routes import admin_routes
from user_routes import user_routes
from report_routes import report_routes
from database import mysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(admin_routes)
app.register_blueprint(user_routes)
app.register_blueprint(report_routes)

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
            return redirect(url_for('user_routes.user_menu'))
        elif role == 'admin':
            return redirect(url_for('admin_routes.admin_menu'))
    
    return render_template('/loggedOut.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        validateCursor = mysql.cursor()
        function_call = "SELECT validate_login('"+ username +"','"+ password_candidate + "')"
        get_user_name = "SELECT first_name FROM citizen WHERE username = '" + username + "';"
        validateCursor.execute(function_call)
        result = validateCursor.fetchone()
        validateCursor.execute(get_user_name)
        first_name = validateCursor.fetchone()
        validateCursor.execute("CALL get_user_mail('"+ username +"')")
        get_user_email = validateCursor.fetchone()
        if list(result.values() )[0]  == 1:
            # Password is correct, log in the user
            session['username'] = username
            session['first_name'] = first_name["first_name"]
            session['user_mail'] = get_user_email
            return redirect(url_for('index'))
        else:
            # Invalid login
             return render_template('/invalidLogin.html')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('/loggedOut.html')

def get_user_role(username):
    with mysql.cursor() as cursor:
        cursor.execute("SELECT user_type FROM citizen WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result['user_type']
    return None


if __name__ == '__main__':
   app.run(port=8000, debug=True)


