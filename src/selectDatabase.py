import re
import sys
import psycopg2
#sys.path.insert(0, r'../lib/')
from connect import *
from database_actions import Database_actions
from connectionclose import close
total=[]
def select():
      global total
      try :
           print("Creating Object")
           conn,cur=connect()
           #db = Database_actions(conn,cur)
           # execute a statement
           print('PostgreSQL database version:')
           #cur.execute('SELECT * from rolelist')
         # display the PostgreSQL database server version
           #cur.execute(Database_actions(conn,cur).create_tables())
           #cur.execute('CREATE TABLE  roleList(roleid serial PRIMARY KEY, rolename VARCHAR(50), location VARCHAR(50));')
           #db_version = cur.fetchall()
           #print(db_version)
           print("print list of tables exist")
           for table in  Database_actions(conn,cur).getTablesList():
              total.append(re.findall(r"\('(.*?)',\)", str(table)))
           sp=str(total).replace('[','').replace(']','')
           pattern = re.compile("\s*,\s*|\s+$")
           x=pattern.split(sp)
           for i in x:
             print(i.replace("'", ""))
         
           print(len(Database_actions(conn,cur).getTablesList()))
           if(len(Database_actions(conn,cur).getTablesList())!=5):
             print("condition pass")
             Database_actions(conn,cur).create_tables()
        
           close()
      except (Exception, psycopg2.DatabaseError) as error:
          print(error)

if __name__ == '__main__':
    select()

