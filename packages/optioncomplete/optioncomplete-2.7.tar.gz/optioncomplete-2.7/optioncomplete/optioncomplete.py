#!/usr/bin/env python3
import os
import sqlite3
from sqlite3 import Error
import collections
from optparse import OptionParser

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
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print(bcolors.FAIL, "Error! cannot create the database connection.", bcolors.ENDC)

    return None

def row_write_sql(conn,name,stropt):
    row = "INSERT INTO autocomplete VALUES ('%s','%s') " % (name, stropt)

    try:
        cur = conn.cursor()
        cur.execute(row)
    except:
        print(bcolors.WARNING,"Row did not added!",bcolors.ENDC)
    conn.commit()

def row_update_sql(conn,name,stropt):
    sqlupdate = "UPDATE autocomplete SET OPTIONS='%s' WHERE PYNAME='%s'" % (stropt, name)
    try:
        cur = conn.cursor()
        cur.execute(sqlupdate)
    except:
        print(bcolors.WARNING,"Row did not updated yet!",bcolors.ENDC)
    conn.commit()

def create_script(name, options):
    script = '''_complete()
    {
       local cur prev opts
       COMPREPLY=()
       cur="${COMP_WORDS[COMP_CWORD]}"
       prev="${COMP_WORDS[COMP_CWORD-1]}"
       opts="''' + " ".join(options) + '''"

       if [[ ${cur} == -* ]]; then
          COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
          return 0
        else
          COMPREPLY=( $(compgen -W "$(ls ./)" -- $cur) )
       fi
    }

    complete -F _complete ''' + name
    home=os.environ["HOME"]
    path=os.path.join(home,".pyautocomplete")
    if not os.path.exists(path):
        os.makedirs(path)
    file=os.path.join(path,os.path.splitext(name)[0]+".sh")

    with open(file, "w") as fw:
        fw.write(script)
    fw.close()

    print(bcolors.WARNING,"\nThe options changed!\nPlease run new terminal or run the below command to use new option(s) auto complete.",bcolors.ENDC)
    print(bcolors.WARNING+"source " + file+"\n",bcolors.ENDC)


def autocomplete(parser: OptionParser,name: str):
    """
    Implements autocomplete options fo python scripts in command line\n
    :param parser: User defined OptionParser with option
    :type parser: OptionParser
    :param name: Name of the python script
    :type name: str

    """
    if not isinstance(parser,OptionParser):
        raise TypeError('Wrong aparameter type in autocomplete.')
        return False
    name=os.path.split(name)[1]
    options=[]
    for i in range(len(parser.option_list)):
        # print(str(parser.option_list.__getitem__(i)))
        for opt in str(parser.option_list.__getitem__(i)).split("/"):
            if opt not in options:
                options.append(opt)
    for i in parser._long_opt.keys():
        for opt in str(parser._long_opt[i]).split("/"):
            if opt not in options:
                options.append(opt)
    stropt=" ".join(options)

    autodir = ".pyautocomplete"
    home=os.environ["HOME"]
    dir = os.path.join(home, autodir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = "autocomplete.db"
    database = os.path.join(dir, file)
    if os.path.exists(database):
        sql = "SELECT OPTIONS  FROM autocomplete WHERE PYNAME='%s'" % (name)
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchall()
        if row == []:
            row_write_sql(conn,name,stropt)
            create_script(name, options)
        else:
            rowlist=str(row[0][0]).split()
            stroptlist=stropt.split()
            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
            if not compare(rowlist,stroptlist):
                row_update_sql(conn, name, stropt)
                create_script(name, options)
    else:
        print(bcolors.WARNING,database," not exists!\n",bcolors.ENDC)
