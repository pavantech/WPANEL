#!/usr/bin/python -W ignore::DeprecationWarning

class Database_actions:
   def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        
   def create_tables(self):
        """ create tables in the PostgreSQL database"""
       # commands = (
      #  """
      #   CREATE TABLE IF NOT EXISTS hostlist( id serial PRIMARY KEY, hostip VARCHAR (50) UNIQUE NOT NULL, 
      #				username VARCHAR (50), password VARCHAR (50), 
      #				groupname VARCHAR (50), ssl VARCHAR(20)
      #		  )
      #  """,
      #  """
      #    CREATE TABLE IF NOT EXISTS groupList(
      #  		id serial PRIMARY KEY, groupname VARCHAR (50) UNIQUE NOT NULL
      #		)
      #  """,
      # """
      #  self.cursor.execute('CREATE TABLE IF NOT EXISTS roleList(id serial PRIMARY KEY, rolename VARCHAR (50) UNIQUE NOT NULL, location VARCHAR (50));')
        self.cursor.execute('CREATE TABLE  Singleymlfile(id serial PRIMARY KEY, singlefilename VARCHAR (50) UNIQUE NOT NULL,location VARCHAR (50));')
        self.cursor.execute("CREATE TABLE  playbookList(id serial PRIMARY KEY, playbookname VARCHAR (50) UNIQUE NOT NULL, location VARCHAR (50));")
        self.cursor.execute("INSERT INTO roleList(rolename, location) VALUES('java','/opt')")
       
   def inserthostlist_data(self, hostip, username, password, groupname, ssl):
             """ insert multiple record into the hostlist table  """
             sql = "INSERT INTO hostlist(hostip, username, password, groupname, ssl) VALUES(%s)"
	     data = (hostip, username, password, groupname, ssl)
	     return sql, data
		  
   def insertroleList_data(self, rolename, location):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO roleList(rolename, location) VALUES(%s,%s)"
	  data = (rolename, location)
	  return sql, data
		  
   def insertgroupname_data(self,  groupname):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO hostlist(groupname) VALUES(%s)"
	  data = (groupname)
	  return sql, data
		  
   def insertplaybooklist_data(self, playbookname, location):
          """ insert multiple record into the hostlist table  """
          sql = "INSERT INTO playbookList(playbookname, location) VALUES(%s,%s)"
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

