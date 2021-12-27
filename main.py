from types import MethodType
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.wrappers import ETagRequestMixin
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssword'
app.config['MYSQL_DB'] = 'sahyog'

mysql = MySQL(app)

registermsg = ""


@app.route('/')
@app.route('/home')
def home():
    return render_template ('./bootstrap/index.html',pagetitle='Home',loginstr=registermsg)

@app.route('/contact')
def contact():
    pagetitle="Contact"
    return render_template ('contact.html',pagetitle='Contact',loginstr=registermsg)

@app.route('/info')
def info():
    return render_template ('info.html',pagetitle='Info',loginstr=registermsg)

@app.route('/about')
def about():
    return render_template ('about.html',pagetitle='About',loginstr=registermsg)

@app.route('/events')
def events():
    return render_template ('events.html',pagetitle='Events',loginstr=registermsg)

@app.route('/login')
def login():
    return render_template ('./bootstrap/sign_in.html',pagetitle='Login',loginstr=registermsg)

@app.route('/register')
def register():
    return render_template ('./bootstrap/register.html',loginstr=registermsg)

@app.route('/saveuser', methods = ['POST'])
def saveuser():
    if request.method=='POST':
        return("Skip Save")
        firstname = request.form.get("first_name",False)
        lastname = request.form.get("last_name",False)
        email = request.form.get("email",False)
        password = request.form.get("psw", False)

        try:
            cur =mysql.connection.cursor()
            cur.execute("INSERT INTO user (first_name, last_name, password, email, address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, password, email,'','','',''))
            mysql.connection.commit()
            #welcome = "Thank you for registering {} {}.".format (firstname, lastname)
            welcome="Thank You"
            return(welcome)
        except Exception as e: 
            Error= "Sorry your email is not unique, please try using another one."
            print(e)
            return(Error)

@app.route('/loginuser', methods = ['POST'])
def loginuser():
    if request.method=='POST':
        try:
            cur = mysql.connection.cursor()
            name = ""
            id = 0
            email = request.form.get("email",False)
            password = request.form.get("psw", False)
            sql="SELECT first_name, last_name FROM user WHERE email='{}' and password='{}'".format(email,password)
            result=cur.execute(sql)
            userdetail = cur.fetchall()
            for (first_name, last_name) in userdetail:
                name = "Welcome " + first_name + " " + last_name
                
            print(name)

            if result>0:
                return render_template ('./bootstrap/index.html',pagetitle='Home',loginstr=name)
            else:
                return("Login failed")
        except Exception as e:
            error= str(e) + " " + sql
            return(error)
        
        #if cur.rowcount == 1:
        #    succesful = "Login succesful"
        #    return(succesful)
        #else:
        #    Error="Email or password is incorrect"
        #    return(Error)
        
        #email = request.form.get("email",False)
        #password = request.form.get("psw", False)
        #try:
#            cur =mysql.connection.cursor()
#            cur.execute("INSERT INTO user (first_name, last_name, password, email, address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, password, email))
#            mysql.connection.commit()
#            welcome = "Thank you for registering {} {}.".format (firstname, lastname)
            #return('HOLA')
        #except: 
         #   Error= "Sorry your email is not unique, please try using another one."
          #  return(Error)

 # cur.execute("INSERT INTO user (first_name, last_name, password, email, address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (firstname, ......))