#!/usr/local/bin/python2.7
"""Usage:fg_to_sqlite
    fg_to_sqlite.py (-l <logfile>)
                    (-d <dbfile>)
"""
__author__ = 'olivier'

import os.path

from docopt import docopt
import sqlite3
import shlex


def check_if_file_exists(filename):
    """
    checks if file exists
    """
    return os.path.isfile(filename)


def create_table(dbfile):
    """
    creates an empty fortiguard log database
    """
    if check_if_file_exists(dbfile):
        print "error: file exists already"
        exit(1)

    statement = '''
    CREATE TABLE log(
    id INT PRIMARY KEY NOT NULL,
    dstcountry  TEXT,
    dstintf TEXT,
    date    DATE,
    time    TIME,
    logid   TEXT,
    type    TEXT,
    subtype TEXT,
    level   TEXT,
    vd      TEXT,
    srcip   TEXT,
    srcport TEXT,
    srcintf TEXT,
    dstip   TEXT,
    dstport TEXT,
    sessionid   TEXT,
    status  TEXT,
    policyid    TEXT,
    srccountry  TEXT,
    trandisp    TEXT,
    serivce TEXT,
    proto   TEXT,
    duration    TEXT,
    sendbyte    TEXT,
    rcvdbyte    TEXT)
    '''
    execute_sqlite_query(dbfile, statement)
    return True


def execute_sqlite_query(dbfile, query):
    check_if_file_exists(dbfile)
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return True



def read_fg_firewall_log(logfile):
    """
    Reads fortigate firewall logfile. Returns a list with
    a dictionary for each line.
    """
    KVDELIM = '='  # key and value deliminator
    try:
        fh = open(logfile, "r")
    except Exception, e:
        print "Error: file %s not readable" % (logfile)
        print e.message
        sys.exit(2)

    loglist = []

    for line in fh:
        # lines are splited with shlex to recognise embeded substrings
        # such as key="valword1 valword2"
        keyvalues = {}
        for field in shlex.split(line):
            key, value = field.split(KVDELIM)
            keyvalues[key] = value
        loglist.append(keyvalues)
        keyvalues = {}
    fh.close()
    return loglist


def write_loglist_to_db(dbfile, loglist):
    """
    writes a fortigate loglist to an sqllite db
    """
    print loglist[0]
    for counter, line in enumerate(loglist):
        query = """
        INSERT INTO log
        VALUES (
        %s
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        ,"%s"
        );
        """ % (counter
               , loglist[counter]['dstcountry']
               , loglist[counter]['dstintf']
               , loglist[counter]['date']
               , loglist[counter]['time']
               , loglist[counter]['logid']
               , loglist[counter]['type']
               , loglist[counter]['subtype']
               , loglist[counter]['level']
               , loglist[counter]['vd']
               , loglist[counter]['srcip']
               , loglist[counter]['srcport']
               , loglist[counter]['srcintf']
               , loglist[counter]['dstip']
               , loglist[counter]['dstport']
               , loglist[counter]['sessionid']
               , loglist[counter]['status']
               , loglist[counter]['policyid']
               , loglist[counter]['srccountry']
               , loglist[counter]['trandisp']
               , loglist[counter]['service']
               , loglist[counter]['proto']
               , loglist[counter]['duration']
               , loglist[counter]['sentbyte']
               , loglist[counter]['rcvdbyte']
               )
        print query
        execute_sqlite_query(dbfile, query)
    None


def main():
    """
    main function
    """
    # gets arguments from docopt
    arguments = docopt(__doc__)
    dbfile = arguments['<dbfile>']
    logfile = arguments['<logfile>']
    # create database
    create_table(dbfile)
    f = open(logfile)
    loglist = read_fg_firewall_log(logfile)
    f.close()

    write_loglist_to_db(dbfile, loglist)

if __name__ == "__main__":
    main()
