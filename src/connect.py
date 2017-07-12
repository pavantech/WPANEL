#!/usr/bin/python
import sys
import psycopg2
import os.path
from config import config
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        return conn, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


