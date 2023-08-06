#!/usr/bin/env python3

import os
import sqlite3
from sqlite3 import Error

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(bcolors.FAIL,e,bcolors.ENDC)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(bcolors.FAIL,e,bcolors.ENDC)

def createdatabase():
    autodir = ".pyautocomplete"
    dir = os.path.join(os.environ["HOME"], autodir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = "autocomplete.db"
    database = os.path.join(dir, file)


    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS autocomplete (
                                    PYNAME  CHAR(128) NOT NULL,
                                    OPTIONS  CHAR(1000)
                                    ); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
    else:
        print(bcolors.FAIL,"Error! cannot create the database connection.",bcolors.ENDC)




if __name__ == '__main__':
    createdatabase()
