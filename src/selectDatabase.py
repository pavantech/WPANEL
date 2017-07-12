import sys
import psycopg2
#sys.path.insert(0, r'../lib/')
from connect import *
from connectionclose import close
def select():
      try :
           conn,cur=connect()
           # execute a statement
           print('PostgreSQL database version:')
           cur.execute('SELECT * from grouplist')
         # display the PostgreSQL database server version
           db_version = cur.fetchall()
           print(db_version)
           close()
      except (Exception, psycopg2.DatabaseError) as error:
          print(error)

if __name__ == '__main__':
    select()

