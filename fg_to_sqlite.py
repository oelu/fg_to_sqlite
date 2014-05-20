#!/usr/local/bin/python2.7
"""Usage:fg_to_sqlite
    fg_to_sqlite.py (-l <logfile>)
                    (-d <dbfile>)

    Options:
        -h --help  show help message
"""
__author__ = 'olivier'

import os.path
import sys

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

    statement = '''
    CREATE TABLE log(
    id INTEGER PRIMARY KEY,
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
    """
    executes an sqlite query
    """
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
    kvdelim = '='  # key and value deliminator
    try:
        filehandle = open(logfile, "r")
    except Exception, ex:
        print "Error: file %s not readable" % (logfile)
        print ex.message
        sys.exit(2)
    loglist = []
    for line in filehandle:
        # lines are splited with shlex to recognise embeded substrings
        # such as key="valword1 valword2"
        keyvalues = {}
        for field in shlex.split(line):
            key, value = field.split(kvdelim)
            keyvalues[key] = value
        loglist.append(keyvalues)
        keyvalues = {}
    filehandle.close()
    return loglist


def write_loglist_to_db(dbfile, loglist):
    """
    writes a fortigate loglist to an sqllite db
    """
    # If NULL is provided as primary key,
    # the primary key will be autoincremented by
    # sqlite
    for counter, line in enumerate(loglist):
        query = """
        INSERT INTO log
        VALUES (
        NULL
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        , "%s"
        );
        """ % (
               loglist[counter]['dstcountry']
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
        execute_sqlite_query(dbfile, query)
    return True


def main():
    """
    main function
    """
    # gets arguments from docopt
    arguments = docopt(__doc__)
    dbfile = arguments['<dbfile>']
    logfile = arguments['<logfile>']
    # create database
    if check_if_file_exists(dbfile):
        print "Error: %s exists already" % (dbfile)
        answer = raw_input("would you like to append to the dbfile? (y/n): ")
        if answer is 'n':
            print "exiting"
            sys.exit(2)
    else:
        create_table(dbfile)

    # read and append logfile
    f = open(logfile)
    loglist = read_fg_firewall_log(logfile)
    f.close()
    write_loglist_to_db(dbfile, loglist)

if __name__ == "__main__":
    main()
