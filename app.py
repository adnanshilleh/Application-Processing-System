import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = '193fhdu98p4djilc90f34'

mydb = mysql.connector.connect(
  host = 'ec2-52-71-28-24.compute-1.amazonaws.com',
  user = 'adnanshilleh',
  password = 'seas',
  database = 'appsDB'
)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        c = mydb.cursor(dictionary = True)
        c.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password, ))
        account = c.fetchone()

        if account:
            session['loggedin'] = True
            session['UID'] = account['UID']
            session['username'] = account['username']
            session['role'] = account['role']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

  
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('UID', None)
   session.pop('username', None)
   session.pop('role', None)
   return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'role' in request.form and 'fname' in request.form and 'lname' in request.form and 'birthday' in request.form and 'ssn' in request.form and 'addr' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form and 'zipcode' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        fname = request.form['fname']
        lname = request.form['lname']
        birthday = request.form['birthday']
        ssn = request.form['ssn']
        addr = request.form['addr']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']    
        zipcode = request.form['zipcode'] 

        c = mydb.cursor()
        c.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = c.fetchone()

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers!'
        elif not re.match(r'[\d{1}]', role):
            msg = 'Invalid role'
        elif not re.match(r'[A-Za-z]+', fname):
            msg = 'Invalid first name!'
        elif not re.match(r'[A-Za-z]+', lname):
            msg = 'Invalid last name!'
        elif not re.match(r'[\d{2}/\d{2}/\d{4}]', birthday):
            msg = "Enter DOB as XX/XX/XXXX"
        elif not re.match(r'[\d{9}]', ssn):
            msg = "Enter social security # as 9 digit number"
        elif not request.form['addr']:
            msg = "Invalid address"
        elif not re.match(r'[A-Za-z]+', city):
            msg = "Invalid city"
        elif not re.match(r'[A-Za-z]+', state):
            msg = "Invalid state"
        elif not re.match(r'[A-Za-z]+', country):
            msg = "Invalid country"
        elif not re.match(r'[\d{5}]', zipcode):
            msg = "Invalid zipcode"
        else:
            c.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, password, email, role, fname, lname, birthday, ssn, addr, city, state, country, zipcode, ))
            mydb.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg = msg)
  
  
@app.route("/index")
def index():
    if 'loggedin' in session: 
        return render_template("index.html")
    return redirect(url_for('login'))
  
  
@app.route("/display")
def display():
    if 'loggedin' in session:
        c = mydb.cursor()
        c.execute('SELECT * FROM accounts WHERE id = %s', (session['UID'], ))
        account = c.fetchone()    
        return render_template("display.html", account = account)
    return redirect(url_for('login'))
  
@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'fname' in request.form and 'lname' in request.form and 'birthday' in request.form and 'ssn' in request.form and 'addr' in request.form and 'city' in request.form and 'state' in request.form and 'country' in request.form and 'zipcode' in request.form:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            fname = request.form['fname']
            lname = request.form['lname']
            birthday = request.form['birthday']
            ssn = request.form['ssn']  
            addr = request.form['addr']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']    
            zipcode = request.form['zipcode'] 

            c = mydb.cursor()
            c.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
            account = c.fetchone()

            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email) or not request.form['email']:
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username) or not request.form['username']:
                msg = 'name must contain only characters and numbers!'
            elif not re.match(r'[A-Za-z]+', fname) or not request.form['fname']:
                msg = 'Invalid first name!'
            elif not re.match(r'[A-Za-z]+', lname) or not request.form['lname']:
                msg = 'Invalid last name!'
            elif not re.match(r'[\d{2}/\d{2}/\d{4}]', birthday) or not request.form['birthday']:
                msg = "Enter DOB as XX/XX/XXXX (month/day/year)"
            elif not re.match(r'[\d{9}]', ssn) or not request.form['ssn']:
                msg = "Enter social security # as 9 digit number"
            elif not request.form['addr']:
                msg = "Invalid address"
            elif not re.match(r'[A-Za-z]+', city) or not request.form['city']:
                msg = "Invalid city"
            elif not re.match(r'[A-Za-z]+', state) or not request.form['state']:
                msg = "Invalid state"
            elif not re.match(r'[A-Za-z]+', country) or not request.form['country']:
                msg = "Invalid country"
            elif not re.match(r'[\d{5}]', zipcode) or not request.form['zipcode']:
                msg = "Invalid zipcode"
            else:
                c.execute('UPDATE accounts SET  username = %s, password = %s, email = %s, fname = %s, lname = %s, birthday = %s, ssn = %s, addr = %s, city = %s, state = %s, country = %s, zipcode = %s WHERE UID = %s', (username, password, email, fname, lname, birthday, ssn, addr, city, state, country, zipcode, (session['UID'], ), ))
                mydb.commit()
                msg = 'You have successfully updated!'

        return render_template("update.html", msg = msg)
    return redirect(url_for('login'))

@app.route("/application", methods = ['GET', 'POST'])
def application():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'admin_date' in request.form and 'degree_app' in request.form and 'bachelor' in request.form and 'bach_school' in request.form and 'bach_gpa' in request.form and 'GRE_verbal' in request.form and 'GRE_quant' in request.form:
            admin_date = request.form['admin_date']
            degree_app = request.form['degree_app']
            bachelor = request.form['bachelor']
            bach_school = request.form['bach_school']
            bach_gpa = request.form['bach_gpa']
            GRE_verbal = request.form['GRE_verbal']  
            GRE_quant = request.form['GRE_quant']

            c = mydb.cursor()
            c.execute('SELECT UID FROM academic_info WHERE UID = %s', (session['UID'], ))
            ID = c.fetchone()

            if ID is not None:
                msg = 'You have already submitted an application!'
            elif not re.match(r'[A-Za-z0-9]+', admin_date):
                msg = 'Invalid date of admission! Ex. Fall 2021'
            elif not re.match(r'[A-Za-z]+', degree_app):
                msg = 'Invalid major!'
            elif not re.match(r'[A-Za-z]+', bachelor):
                msg = 'Invalid Bachelor Degree Entry!'
            elif not re.match(r'[A-Za-z]+', bach_school):
                msg = 'Invalid Undergraduate School!'
            elif not re.match(r'[\d*\.\d+|\d+]', bach_gpa):
                msg = "Invalid GPA!"
            elif not re.match(r'[\d{3}]', GRE_verbal):
                msg = "Invalid GRE Verbal score, enter in range 130-170"
            elif not re.match(r'[\d{3}]', GRE_quant):
                msg = "Invalid GRE Quantitative score, enter in range 130-170"
            else:
                c.execute('INSERT INTO academic_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (session['UID'], admin_date, degree_app, bachelor, bach_school, bach_gpa, GRE_verbal, GRE_quant, ))
                mydb.commit()
                msg = 'You have successfully Applied!'

        return render_template("application.html", msg = msg)


@app.route("/submitletters", methods = ['GET', 'POST'])
def submitletters():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            fullname1 = request.form['fullname1']
            rec_email1 = request.form['rec_email1']
            title1 = request.form['title1']
            affiliation1 = request.form['affiliation1']
            fullname2 = request.form['fullname2']
            rec_email2 = request.form['rec_email2']
            title2 = request.form['title2']
            affiliation2 = request.form['affiliation2']
            fullname3 = request.form['fullname3']
            rec_email3 = request.form['rec_email3']
            title3 = request.form['title3']
            affiliation3 = request.form['affiliation3']
            
            c = mydb.cursor()
            c.execute('SELECT UID FROM letters WHERE UID = %s', (session['UID'], ))
            ID = c.fetchone()
            
            if ID is not None:
                msg = 'You have already submitted this form!'
            elif not re.match(r'[A-Za-z]+', fullname1) or not request.form['fullname1']:
                msg = 'Invalid name'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', rec_email1) or not request.form['rec_email1']:
                msg = 'Invalid email format'
            elif not re.match(r'[A-Za-z]+', title1) or not request.form['title1']:
                msg = 'Invalid title'
            elif not re.match(r'[A-Za-z]+', affiliation1) or not request.form['affiliation1']:
                msg = 'Invalid affiliation'
            elif not re.match(r'[A-Za-z]+', fullname2) or not request.form['fullname2']:
                msg = 'Invalid name'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', rec_email2) or not request.form['rec_email2']:
                msg = 'Invalid email format'
            elif not re.match(r'[A-Za-z]+', title2) or not request.form['title2']:
                msg = 'Invalid title'
            elif not re.match(r'[A-Za-z]+', affiliation2) or not request.form['affiliation2']:
                msg = 'Invalid affiliation'
            elif not re.match(r'[A-Za-z]+', fullname3) or not request.form['fullname3']:
                msg = 'Invalid name'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', rec_email3) or not request.form['rec_email3']:
                msg = 'Invalid email format'
            elif not re.match(r'[A-Za-z]+', title3) or not request.form['title3']:
                msg = 'Invalid title'
            elif not re.match(r'[A-Za-z]+', affiliation3) or not request.form['affiliation3']:
                msg = 'Invalid affiliation'
            
            else:
                c.execute('INSERT INTO letters VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (session['UID'], fullname1, rec_email1, title1, affiliation1, fullname2, rec_email2, title2, affiliation2, fullname3, rec_email3, title3, affiliation3, ))
                mydb.commit()
                msg = 'Request for letters submitted successfully!'

        return render_template('submitletters.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)



app.run(host='0.0.0.0', port=8080)