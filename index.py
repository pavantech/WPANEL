# -*- coding: utf-8 -*-
from flask import Flask, redirect,url_for, render_template
from flask import request
import os
import git
import sys
import re
from distutils.dir_util import copy_tree
import shutil
import subprocess
import datetime
sys.path.insert(0, r'src/')
from selectDatabase import select
from connect import connect 
from database_actions import Database_actions
from runplaybooks import runplaybooks
newlist=[]
removedquoteslist=[]
iplist=[]
ipremovedquoteslist=[]
consolelist=[]
app = Flask(__name__)
@app.before_request
def before_request():
   owd = os.getcwd()
   try:
        root, dirs, files = os.walk("external/plugins/").next()
        print dirs
        if dirs==[]:
          os.chdir("external/plugins/")
          git.Git().clone("https://github.com/pavantech/Ansible_Playbook.git")
        else:
           print "not empty"
   finally:
        #change dir back to original working directory (owd)
        os.chdir(owd)
   conn,cur=connect()
   Database_actions(conn,cur).create_tables()

@app.route('/')
def index():
   return render_template('sign-in.html')

@app.route('/signout')
def signout():
   conn,cur=connect()
   conn.close()
   return render_template('sign-in.html')

@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@app.route('/error.html')
def errormsg():
   return render_template('error.html')

@app.route('/login/sign-in.html')
def error():
   return render_template('sign-in.html')

@app.route('/message.html')
def msg():
   return render_template('message.html')

@app.route('/runplugins')
def runplugins():
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
           iplist.append(re.findall(r"\('(.*?)',\)", str(ipname)))
    removesquarebrackets1=str(iplist).replace('[','').replace(']','')
    afterlist1=pattern.split(removesquarebrackets1)
    for i in afterlist1:
      ipremovedquoteslist.append(i.replace("'", ""))   
    root, dirs, files = os.walk("external/plugins/Ansible_Playbook/").next()
    return render_template('runplugins.html',  groupnames=removedquoteslist, ipnames=ipremovedquoteslist, rolenames=dirs[1:])

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

@app.route('/runplaybookplugin/', methods=['POST'])
def runplaybookplugin():
    global consolelist
    del consolelist[:]
    groupname= request.form.getlist('groupname')
    role = request.form.getlist('rolename')
    conn,cur=connect()
    cur.execute("SELECT * FROM hostlist where groupname='%s'"%groupname[0])
    data = cur.fetchall()
    print len(data)
    if len(data)==0:
        messages = "Please added atleast one host from addhost menu"
        return  render_template('message.html', messages = messages)
    if len(role)==0:
        messages = "Please add roles at external/plugins folder"
        return  render_template('message.html', messages = messages)
    dir=runplaybooks().runplaybookgroup(groupname,role)
    owd = os.getcwd()
    now = datetime.datetime.now()
    f = open('log/log'+now.isoformat()+'.log', 'a')
    os.chdir(dir)
    print(os.getcwd())
    p = subprocess.Popen('ansible-playbook main.yml', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
         print line,
         consolelist.append(line)
         f.write(line)
    retval = p.wait()
    print(retval)
    f.close()
    os.chdir(owd)
    os.system('rm -rf '+dir)
    files = os.listdir('log/')  
    return render_template('consoletab.html', consolelog=consolelist, logfiles=files)
@app.route('/runplaybookhostname/', methods=['POST'])
def runplaybookhostname():
    global consolelist
    del consolelist[:]
    hostname= request.form.getlist('hostname')
    role = request.form.getlist('rolename')
    print(role)
    dir=runplaybooks().runplaybookhost(hostname,role)
    owd = os.getcwd()
    now = datetime.datetime.now()
    f = open('log/log'+now.isoformat()+'.log', 'a')
    os.chdir(dir)
    print(os.getcwd())
    p = subprocess.Popen('ansible-playbook main.yml', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
         print line,
         consolelist.append(line)
         f.write(line)
    retval = p.wait()
    print(retval)
    f.close()
    os.chdir(owd)
    os.system('rm -rf '+dir)
    files = os.listdir('log/')
    return render_template('consoletab.html', consolelog=consolelist, logfiles=files)

@app.route('/runplaybookNotRegister/', methods=['POST'])
def runplaybookNotRegister():
    global consolelist
    del consolelist[:]
    hostname=request.form['hostname']
    username=request.form['username']
    password=request.form['password']
    role = request.form.getlist('rolename')
    print(role)
    dir=runplaybooks().runplaybookhostnoregister(hostname,username,password,role)
    owd = os.getcwd()
    now = datetime.datetime.now()
    f = open('log/log'+now.isoformat()+'.log', 'a')
    os.chdir(dir)
    print(os.getcwd())
    p = subprocess.Popen('ansible-playbook main.yml', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
         print line,
         consolelist.append(line)
         f.write(line)
    retval = p.wait()
    print(retval)
    f.close()
    os.chdir(owd)
    os.system('rm -rf '+dir)
    files = os.listdir('log/')
    return render_template('consoletab.html', consolelog=consolelist, logfiles=files)

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
    if(email=="admin"  and password=="admin") :
        return redirect(url_for('dashboard'))
    else:
        messages = "Please use username admin and password admin"
    	return  render_template('error.html', messages = messages)


@app.route('/inserthost/', methods=['POST'])
def inserthostip():
    hostip = request.form['hostip']
    username = request.form['username']
    password = request.form['password']
    groupname= request.form['groupname']
    #ssl = request.form.getlist('ssl')
    #if ssl[0]=="yes":
    #   check="checked"
    #else:
    check="not checked" 
    conn,cur= connect()
    sql,data=Database_actions(conn,cur).inserthostlist_data(hostip, username, password, groupname, check)
    cur.execute(sql,data)
    conn.commit()
    messages = "Succcessfully added the host"
    return  render_template('message.html', messages = messages)
   

@app.route('/insertgroup/', methods=['POST'])
def insertgroup():
    groupname= request.form['groupname']
    conn,cur= connect()
    result=Database_actions(conn,cur).insertgroupname_data(groupname)
    return  render_template('message.html', messages = result)


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0")
   app.run(debug = True)
