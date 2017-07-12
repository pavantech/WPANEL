# -*- coding: utf-8 -*-
from flask import Flask, redirect,url_for, render_template
from flask import request
import sys
sys.path.insert(0, r'src/')
from selectDatabase import select
from connect import connect 

app = Flask(__name__)
@app.before_request
def before_request():
    connect()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/sign-up.html')
def signup():
   return render_template('sign-up.html')
@app.route('/sign-in.html')
def signin():
   return render_template('sign-in.html')
@app.route('/addhost')
def addhost():
   return render_template('addhost.html')
@app.route('/login/addgroup.html')
def addgroup():
   return render_template('addgroup.html')
@app.route('/login/addpermission.html')
def addpermission():
   return render_template('addpermission.html')
@app.route('/login/uploadrole.html')
def uploadrole():
   return render_template('uploadrole.html')
@app.route('/login/uploadplaybook.html')
def uploadplaybook():
   return render_template('uploadplaybook.html')
@app.route('/login/runsingleyml.html')
def runsingleyml():
   return render_template('runsingleyml.html')

@app.route('/index.html')
def indexmain():
   return render_template('index.html')

@app.route('/hello/', methods=['GET', 'POST'])
def hello():
    email=request.form['email']
    password=request.form['password']
    mobile=request.form['mobile']
    return render_template('form_action.html', email=email, password=password, mobile=mobile)

@app.route('/login/', methods=['POST'])
def  login():
    email=request.form['email']
    password=request.form['password']
    if(email=="mvvpavan@gmail.com"  and password=="password") :
        return redirect(url_for('addhost'))
    else:
    	return redirect(url_for('/'))


@app.route('/inserthost/', methods=['POST'])
def inserthostip():
    hostip = request.form['hostip']
    username = request.form['username']
    password = request.form['password']
    groupname= request.form['groupname']
    ssl = request.form.getlist('ssl[]')
    print(hostip + username +password +groupname)
    return  redirect(url_for('addhost'))


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0")
   app.run(debug = True)
