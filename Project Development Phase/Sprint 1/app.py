from crypt import methods
from flask import Flask, render_template, request, redirect, session,url_for
import ibm_db
import sys

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tkt02689;PWD=iJblyvngVsuVA5ae;",'','')

app = Flask(__name__)
app.secret_key = 'fasdgfdgdfg'

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
     try:
         mail = request.form['mail']
         pwd = request.form['psw']
         sql = "SELECT * from employee where email = '{}'".format(mail)        
         stmt = ibm_db.exec_immediate(conn, sql)
         dict = ibm_db.fetch_assoc(stmt)         
         if (mail == dict['EMAIL'].strip() and pwd == dict['PASSWORD'].strip()):
            return redirect(url_for("home"))
         else:
            return render_template("signin.html",message = "Not a valid user")
    
             
     except:            
            print (sys.exc_info()[0])
    if request.method == 'GET':
        return render_template("signin.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
      try:
        dict = {}
        name = request.form['user_name']
        email = request.form['email']
        age = request.form['age']
        pw = request.form['psw']
        sql1 = "SELECT email from employee where email = '{}'".format(email)
        stmt = ibm_db.exec_immediate(conn, sql1) 
        dict = ibm_db.fetch_assoc(stmt)
        if(dict == False):
            sql = "INSERT into employee values ('{}', '{}','{}', '{}')".format(name, email, age, pw)
            stmt = ibm_db.exec_immediate(conn, sql) 
            return render_template('signin.html')
        else:
            return redirect(url_for('exists'))        
     
      except:
        print (sys.exc_info()[0])
      
    if request.method == 'GET':
        return render_template('signup.html')

@app.route('/exists')
def exists():
    return render_template('signup.html',exists = "User already exists")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addsalary')
def salary():
    return render_template('salary.html')

@app.route('/addexpenses')
def expenses():
    return render_template('expenses.html')

@app.route('/visualization')
def vis():
    return render_template('vis.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
