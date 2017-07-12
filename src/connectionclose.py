import sys
import psycopg2
from connect import connect
def close():
      try :
           conn,cur=connect()
     # close the communication with the PostgreSQL
           cur.close()
      except (Exception, psycopg2.DatabaseError) as error:
          print(error)
      finally:
         if conn is not None:
            conn.close()
            print('Database connection closed.')
      return


