# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/sign-up.html')
def signup():
   return render_template('sign-up.html')
@app.route('/sign-in.html')
def signin():
   return render_template('sign-in.html')
@app.route('/login/addhost.html')
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

@app.route('/hello/', methods=['POST'])
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
        return render_template('addhost.html')
    else:
    	return render_template('index.html')

if __name__ == '__main__':
   app.debug = True
   app.run()
   app.run(debug = True)