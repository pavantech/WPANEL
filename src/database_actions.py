#!/usr/bin/python -W ignore::DeprecationWarning

class Database_actions:
   var="false"
   def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        
   def create_tables(self):
        #""" create tables in the PostgreSQL database"""
         self.cursor.execute('CREATE TABLE IF NOT EXISTS hostlist(id serial PRIMARY KEY, hostip VARCHAR (50) UNIQUE NOT NULL, username VARCHAR (50), password VARCHAR (50), groupname VARCHAR (50), ssl VARCHAR(20))')
         self.cursor.execute('CREATE TABLE IF NOT EXISTS groupList(id serial PRIMARY KEY, groupname VARCHAR (50) UNIQUE NOT NULL)')
         self.cursor.execute('CREATE TABLE IF NOT EXISTS roleList(id serial PRIMARY KEY, rolename VARCHAR (50) UNIQUE NOT NULL, location VARCHAR (50))')
         self.cursor.execute('CREATE TABLE IF NOT EXISTS Singleymlfile(id serial PRIMARY KEY, singlefilename VARCHAR (50) UNIQUE NOT NULL,location VARCHAR (50))')
         self.cursor.execute('CREATE TABLE IF NOT EXISTS playbookList(id serial PRIMARY KEY, playbookname VARCHAR (50) UNIQUE NOT NULL, location VARCHAR (50))')
         self.conn.commit()
        
       
   def inserthostlist_data(self, hostip, username, password, groupname, ssl):
             """ insert multiple record into the hostlist table  """
             sql = "INSERT INTO hostlist(hostip, username, password, groupname, ssl) VALUES(%s,%s,%s,%s,%s)"
	     data = (hostip, username, password, groupname, ssl)
	     return sql, data
		  
   def insertroleList_data(self, rolename, location):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO rolelist(rolename, location) VALUES(%s,%s)"
	  data = (rolename, location)
	  return sql, data
		  
   def insertgroupname_data(self, groupname):
          """ insert multiple record into the hostlist table  """
          print("gname:"+groupname)
          sql = "INSERT INTO grouplist(groupname) VALUES(%s)"
	  data = (groupname,)
          self.cursor.execute("""SELECT groupname FROM grouplist""")
          #if groupname in self.cursor.fetchall(): 
          #  print 'success'
          global var
          for table in self.cursor.fetchall():
               if  groupname in table:
                  var="true"
          if var!="true":
            self.cursor.execute(sql,data)
            self.conn.commit()
            return "success"
          else:
            return "Group Name aleady Existed"
	  
		  
   def insertplaybooklist_data(self, playbookname, location):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO playbooklist(playbookname, location) VALUES(%s,%s)"
	  data = (playbookname, location)
	  return sql, data
		  
   def insertsinglefile_data(self, singlefilename, location):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO Singleymlfile(singlefilename, location) VALUES(%s,%s)"
	  data = (singlefilename, location)
	  return sql, data
		  
   def getTablesList(self):
	self.cursor.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        #for table in self.cursor.fetchall():
        #   print(table)
	return self.cursor.fetchall()

   def getgroupNames(self):
        self.cursor.execute("""SELECT groupname FROM grouplist""")
        #for table in self.cursor.fetchall():
        #   print(table)
        return self.cursor.fetchall()


