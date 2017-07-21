# -*- coding: utf-8 -*-
from flask import Flask, redirect,url_for, render_template, session
import flask
from flask import request
from shelljob import proc
import eventlet
eventlet.monkey_patch()
import logging
from logging.handlers import RotatingFileHandler
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
#session

head='''<html>
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
      <script type="text/javascript" src="http://netdna.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
      <link href="http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
      <link href="http://pingendo.github.io/pingendo-bootstrap/themes/default/bootstrap.css" rel="stylesheet" type="text/css">
   </head>
    <script>
        .dropdown-submenu {
    position: relative;
}

.dropdown-submenu .dropdown-menu {
    top: 20;
    left: 100%;
    margin-top: 30px;
}

.hide{
  display:none;
}
</script>
   <body>
      <div class="navbar navbar-default navbar-static-top">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-ex-collapse">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#"><span>DASHBOARD</span></a>
                </div>
                <div class="collapse navbar-collapse" id="navbar-ex-collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li class="active">
                            <a href="/dashboard">Home</a>
                        </li>
                        <li>
                            <a href="/addhost">Add Host</a>
                        </li>
                        <li>
                            <a href="/addgroup">Add Group</a>
                        </li>
                        <li class="dropdown-submenu hide">
                        <a class="test" tabindex="-1" href="addpermission.html">PERMISSION<span class="caret"></span></a>
                            <ul class="dropdown-menu">
                             <li><a tabindex="-1" href="#">UPLOAD</a></li>
                            <li><a tabindex="-1" href="{{ url_for('addpermission') }}">UNCOMMENT</a></li>
                                                        </ul>
                       </li>

                        <li class="dropdown-submenu hide">
                        <a class="test" tabindex="-1" href="#">PLAYBOOK<span class="caret"></span></a>
                            <ul class="dropdown-menu">
                             <li><a tabindex="-1" href="#">UPLOAD ROLE</a></li>
                            <li><a tabindex="-1" href="#">UPLOAD PLAYBOOK</a></li>
                                                        <li><a tabindex="-1" href="#">RUN SINGLE YML</a></li>
                          </ul>
                       </li>
                        <li>
                            <a href="/signout">Sign out</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

      <div class="section">
         <div class="container">
            <div class="row">
               <div class="col-md-12">
                  <div class="panel panel-primary">
                     <div class="panel-heading">
                        <h3 class="panel-title">Console Log</h3>
                     </div>
                     <div class="panel-body">'''

tail=''' </div>
                  </div>
               </div>
            </div>
         </div>
      </div>

           <script>
$(document).ready(function(){
  $('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});
</script>   </body></html>'''

app = Flask(__name__)
app.secret_key = "super secret key"
@app.before_request
def before_request():
   owd = os.getcwd()
   try: 
        root1, dirs1, files1 = os.walk("external/plugins/Ansible_Playbook").next() 
        if dirs1==[]:
           print("please add atleas on role")
           #if os.path.exists("external/plugins/Ansible_Playbook"):
           #    os.system("rm -rf external/plugins/Ansible_Playbook")
        root, dirs, files = os.walk("external/plugins/").next()
        print dirs
        if dirs==[]:
          os.chdir("external/plugins/")
          os.system("mkdir Ansible_Playbook")
         # git.Git().clone("https://github.com/pavantech/Ansible_Playbook.git")
        else:
           print "not empty"
   finally:
        #change dir back to original working directory (owd)
        os.chdir(owd)
   conn,cur=connect()
   Database_actions(conn,cur).create_tables()

@app.route('/')
def index():
   app.logger.warning('testing warning log')
   app.logger.error('testing error log')
   app.logger.info('testing info log')
   return render_template('sign-in.html')

@app.route('/signout')
def signout():
   global session
   if 'dir' in session:
       dir = session['dir']
       os.system('rm -rf '+dir)
   session.pop('dir', None)
   conn,cur=connect()
   conn.close()
   return render_template('sign-in.html')

@app.route('/dashboard')
def dashboard():
   global session
   if 'dir' in session:
       dir = session['dir']
       os.system('rm -rf '+dir)
   session.pop('dir', None)
   return render_template('dashboard.html')

@app.route('/error.html')
def errormsg():
   return render_template('error.html')

@app.route('/login/sign-in.html')
def error():
   return render_template('sign-in.html')

@app.route('/message.html')
def msg():
   global session
   if 'dir' in session:
       dir = session['dir']
       os.system('rm -rf '+dir)
   return render_template('message.html')

@app.route('/runplugins')
def runplugins():
    global session
    if 'dir' in session:
       dir = session['dir']
       os.system('rm -rf '+dir)
    session.pop('dir', None)
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
    global consolelist, session, head, tail
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
    session['dir']=dir
    owd = os.getcwd()
    g = proc.Group()
    p = g.run( [ "bash", "-c", "(cd "+ dir +" && ansible-playbook main.yml)" ])
    def read_process():
        yield head
        while g.is_pending():
          lines = g.readlines()
          for proc, line in lines:
             app.logger.info(line)
             yield "<h3>" + line + "<h3><br>"
        yield tail
    return flask.Response( read_process(), mimetype= 'text/html' )
    
@app.route('/runplaybookhostname/', methods=['POST'])
def runplaybookhostname():
    global consolelist, session, head, tail
    del consolelist[:]
    hostname= request.form.getlist('hostname')
    role = request.form.getlist('rolename')
    print(role)
    dir=runplaybooks().runplaybookhost(hostname,role)
    session['dir']=dir
    owd = os.getcwd()
    g = proc.Group()
    p = g.run( [ "bash", "-c", "(cd "+ dir +" && ansible-playbook main.yml)" ])
    def read_process():
        yield head
        while g.is_pending():
          lines = g.readlines()
          for proc, line in lines:
             app.logger.info(line)
             yield "<h3>" + line + "<h3><br>"
        yield tail
    return flask.Response( read_process(), mimetype= 'text/html' )

@app.route('/runplaybookNotRegister/', methods=['POST'])
def runplaybookNotRegister():
    global consolelist, head, tail, session
    del consolelist[:]
    hostname=request.form['hostname']
    username=request.form['username']
    password=request.form['password']
    role = request.form.getlist('rolename')
    print(role)
    dir=runplaybooks().runplaybookhostnoregister(hostname,username,password,role)
    session['dir']=dir
    owd = os.getcwd()
    g = proc.Group()
    p = g.run( [ "bash", "-c", "(cd "+ dir +" && ansible-playbook main.yml)" ])
    def read_process():
        yield head
        while g.is_pending():
          lines = g.readlines()
          for proc, line in lines:
             app.logger.info(line)
             yield "<h3>" + line + "<h3><br>"
        yield tail
    return flask.Response( read_process(), mimetype= 'text/html' )

@app.route('/addgroup')
def addgroup():
   global session
   if 'dir' in session:
       dir = session['dir']
       os.system('rm -rf '+dir)
   session.pop('dir', None)
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
   if os.path.exists('log/info.log'):
      now = datetime.datetime.now()
      log="info"+str(now.strftime("%Y-%m-%d%H:%M"))+".log"
      os.system("mv log/info.log log/"+log)
      logHandler = RotatingFileHandler('log/info.log', maxBytes=1000, backupCount=1)
   else:
     logHandler = RotatingFileHandler('log/info.log', maxBytes=1000, backupCount=1)
    
    # set the log handler level
   logHandler.setLevel(logging.INFO)

    # set the app logger level
   app.logger.setLevel(logging.INFO)

   app.logger.addHandler(logHandler) 
   app.debug = True
   app.run(host="0.0.0.0")
   app.run(debug = True)

