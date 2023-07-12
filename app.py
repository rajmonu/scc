from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    '''This is the Homepage'''
    return render_template("index.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template("courses.html")


# Student Registration and Login Page code

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scc'
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\rv201\\PycharmProjects\\SCC\\static\\profilePic'
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
app.config['SECRET_KEY'] = 'secret_key'

mysql = MySQL(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'Name' in request.form and 'Email' in request.form:
        Rollno = 'NULL'
        Name = request.form['Name']
        Age = request.form['Age']
        Gender = request.form['Gender']
        Email = request.form['Email']
        Mobile = request.form['Mobile']
        Address = request.form['Address']
        Password = request.form['Password']
        file = request.files['Photo']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        Photo = request.files['Photo'].filename

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM studentreg WHERE Email = % s', (Email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO studentreg VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s)', (Rollno, Name, Age, Gender, Email, Mobile, Address, Photo, Password,))
            mysql.connection.commit()
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("register.html", msg=msg)


# Student Login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        Email = request.form['Email']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM studentreg WHERE Email = % s AND Password = % s', (Email, Password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['Name']
            session['email'] = user['Email']
            return render_template('sDashboard.html', msg=msg)
        else:
            msg = 'Please enter correct email / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
