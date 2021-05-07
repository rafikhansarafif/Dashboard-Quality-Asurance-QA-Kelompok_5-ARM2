# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import random
import datetime
import time
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
#import pandas as pd

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'postgre123'
app.config['MYSQL_DB'] = 'db_bengkel_website'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# start html 1
@app.route('/')
def home2():
    return render_template("home2.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        if request.form['email'] == '':
            flash('Insert All Data First')
            return render_template("register.html")
        else:
            if request.form['name'] == '':
                flash('Insert All Data First')
                return render_template("register.html")
            else:
                if request.form['password'] == '':
                    flash('Insert All Data First')
                    return render_template("register.html")
                else:
                    name = request.form['name']
                    email = request.form['email']
                    password = request.form['password'].encode('utf-8')
                    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                                (name, email, hash_password))
                    mysql.connection.commit()
                    session['name'] = request.form['name']
                    session['email'] = request.form['email']
                    return redirect(url_for('home_user'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()
        if request.form['submit_button'] == 'Log In as Admin':
            return render_template("login_admin.html")
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home_user.html")
            else:
                flash('Email and Password Incorrect')
                return render_template("login.html")
        else:
            flash('Input Email and Password First')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/login_admin', methods=["GET", "POST"])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user_admin WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()
        if request.form['submit_button'] == 'Log In as User':
            return render_template("login.html")
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                flash('Email and Password Incorrect')
                return render_template("login_admin.html")
        else:
            flash('Input Email and Password First')
            return render_template("login_admin.html")
    else:
        return render_template("login_admin.html")
# end html 1

# start html 2
@app.route('/home_user')
def home_user():
    return render_template("home_user.html")

@app.route('/dashboard_user')
def dashboard_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM data GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('dashboard_user.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

@app.route('/barchart_user')
def barchart_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM data GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('barchart_user.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

@app.route('/about_user')
def about_user():
    return render_template("about_user.html")

@app.route('/users_user', methods=["GET", "POST"])
def users_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user_admin WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("users_user.html")

@app.route('/logout_user', methods=["GET", "POST"])
def logout_user():
    session.clear()
    return render_template("home2.html")
# end html 2

# start html 3
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM data GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('dashboard.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

@app.route('/barchart')
def barchart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data")
    list_part = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM data GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)

    return render_template('barchart.html', list_part = list_part, chart_data = chart_data, chart_labels = chart_labels)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_admin")
    list_data = cur.fetchall()
    cur.execute("SELECT * FROM users")
    list_users = cur.fetchall()
    return render_template("users.html", list_data = list_data, list_users = list_users)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home2.html")

#dashboard
@app.route('/add_data', methods=["POST"])
def add_data():
    n = request.form['btnradio']
    converted_num = int(n)
    for i in range(converted_num):
        letters = ['OK', 'REJECT']
        random_index1 = random.choices(letters)
        letter = ['FC', 'ESC', 'VTX', 'MOTOR']
        random_index = random.choices(letter)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data (nama_part, status) VALUES (%s, %s)", (random_index, random_index1))
        mysql.connection.commit()
        time.sleep(9)
    return redirect(url_for('dashboard'))

@app.route('/edit_data/<id>', methods = ['POST', 'GET'])
def edit_data(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM data WHERE Id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('fly_dashboard.html', data = data[0])

@app.route('/update_data/<Id>', methods=['POST'])
def update_data(Id):
    if request.form['btnradio'] == 'OK':
        cur = mysql.connection.cursor()
        letterz = ['OK']
        cur.execute("""
            UPDATE data
            SET status = %s
            WHERE Id = %s 
        """, (letterz, Id))
        mysql.connection.commit()
        flash('Status Changed to "OK"')
        return redirect(url_for('dashboard'))
    elif request.form['btnradio'] == 'REJECT':
        cur = mysql.connection.cursor()
        letterz = ['REJECT']
        cur.execute("""
            UPDATE data
            SET status = %s
            WHERE Id = %s
        """, (letterz, Id))
        mysql.connection.commit()
        flash('Status Changed to "REJECT"')
        return redirect(url_for('dashboard'))
    

@app.route('/delete_data/<string:id_data>', methods=["GET"])
def delete_data(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data WHERE Id=%s", (id_data,))
    flash('Data Deleted Successfully')
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_admin', methods=["POST"])
def add_admin():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user_admin (name, email, password) VALUES (%s,%s,%s)",
                (name, email, hash_password))
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/delete_admin/<string:id_data>', methods=["GET"])
def delete_admin(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user_admin WHERE Id=%s", (id_data,))
    flash('Admin Account Deleted')
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/delete_user/<string:id_data>', methods=["GET"])
def delete_user(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE Id=%s", (id_data,))
    flash('User Account Deleted')
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route("/chart")
def chart():
    cur = mysql.connection.cursor()
    data_1 = cur.execute('SELECT * FROM data WHERE Id = OK', (id))
    ok_data = data['data_1'].count()
    data_2 = cur.execute('SELECT * FROM data WHERE Id = REJECT', (id))
    reject_data = data['data_2'].count()
    labels = ["OK","REJECT"]
    values = int([ok_data, reject_data])
    return render_template('chart.html', values=values, labels=labels)
# end dashboard
# end html 3

# start kodular
@app.route('/dashboard_mobile')
def dashboard_mobile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data ")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    for result in rv:
     return render_template('dashboard_mobile.html', data=rv)
#end kodular

if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host = '0.0.0.0', debug=True)
