# -*- coding: utf-8 -*-
from flask import Flask, redirect,url_for, render_template
from flask import request


import sys
import re
sys.path.insert(0, r'src/')
from selectDatabase import select
from connect import connect 
from database_actions import Database_actions
newlist=[]
removedquoteslist=[]
iplist=[]
ipremovedquoteslist=[]

app = Flask(__name__)
@app.before_request
def before_request():
   conn,cur=connect()
   Database_actions(conn,cur).create_tables()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@app.route('/runplugins')
def runplugins():
   return render_template('runplugins.html')


@app.route('/sign-up.html')
def signup():
   return render_template('sign-up.html')
@app.route('/sign-in.html')
def signin():
   return render_template('sign-in.html')
@app.route('/addhost')
def addhost():
    global newlist, removedquoteslist
    del newlist[:]
    del removedquoteslist[:]
    conn,cur= connect()
    for groupname in  Database_actions(conn,cur).getgroupNames():
           newlist.append(re.findall(r"\('(.*?)',\)", str(groupname)))
    removesquarebrackets=str(newlist).replace('[','').replace(']','')
    pattern = re.compile("\s*,\s*|\s+$")
    afterlist=pattern.split(removesquarebrackets)
    for i in afterlist:
      removedquoteslist.append(i.replace("'", ""))
    return render_template('addhost.html',  groupnames=removedquoteslist)

@app.route('/runplaybookplugin')
def runplaybookplugin():
    global newlist, removedquoteslist
    del newlist[:]
    del removedquoteslist[:]
    del iplist[:]
    del ipremovedquoteslist[:]
    conn,cur= connect()
    for groupname in  Database_actions(conn,cur).getgroupNames():
           newlist.append(re.findall(r"\('(.*?)',\)", str(groupname)))
    removesquarebrackets=str(newlist).replace('[','').replace(']','')
    pattern = re.compile("\s*,\s*|\s+$")
    afterlist=pattern.split(removesquarebrackets)
    for i in afterlist:
      removedquoteslist.append(i.replace("'", ""))
    for ipname in  Database_actions(conn,cur).getipNames():
           iplist.append(re.findall(r"\('(.*?)',\)", str(groupipname)))
    removesquarebrackets1=str(newlist).replace('[','').replace(']','')
    afterlist1=pattern.split(removesquarebrackets1)
    for i in afterlist1:
      ipremovedquoteslist.append(i.replace("'", ""))    
    
    return render_template('addhost.html',  groupnames=removedquoteslist, ipnames=ipremovedquoteslist)


@app.route('/addgroup')
def addgroup():
   return render_template('addgroup.html')
@app.route('/addpermission.html')
def addpermission():
   return render_template('addpermission.html')
@app.route('/uploadrole.html')
def uploadrole():
   return render_template('uploadrole.html')
@app.route('/uploadplaybook.html')
def uploadplaybook():
   return render_template('uploadplaybook.html')
@app.route('/runsingleyml.html')
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
        return redirect(url_for('dashboard'))
    else:
    	return redirect(url_for('/'))


@app.route('/inserthost/', methods=['POST'])
def inserthostip():
    hostip = request.form['hostip']
    username = request.form['username']
    password = request.form['password']
    groupname= request.form['groupname']
    ssl = request.form.getlist('ssl')
    if ssl[0]=="yes":
       check="checked"
    else:
       check="not checked" 
    conn,cur= connect()
    sql,data=Database_actions(conn,cur).inserthostlist_data(hostip, username, password, groupname, check)
    cur.execute(sql,data)
    conn.commit()
    return  redirect(url_for('addhost'))

@app.route('/insertgroup/', methods=['POST'])
def insertgroup():
    groupname= request.form['groupname']
    conn,cur= connect()
    result=Database_actions(conn,cur).insertgroupname_data(groupname)
    return  redirect(url_for('addgroup'), results=result)

if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0")
   app.run(debug = True)
