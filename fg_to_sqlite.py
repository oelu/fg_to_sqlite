#!/usr/local/bin/python2.7
""" fg_to_sqlite.py
parses a fortigate log to a sqlite db file
Usage:
      fg_to_sqlite.py (-l <logfile> | --logfile <logfile>)
      fg_to_sqlite.py (-d <dbfile> | --dbfile <dbfile>)

"""
__author__ = 'olivier'

# import statements
from docopt import docopt
import sqlite3


def create_table(cursor):
    """
    creates an empty fortiguard log database
    """

    statement = '''
    CREATE TABLE log(
    id      TEXT    PRIMARY KEY,
    date    DATE,
    time    TIME,
    logid   TEXT,
    tpye    TEXT,
    subtype TEXT,
    level   TEXT,
    vd      TEXT,
    srcip   TEXT,
    srcport TEXT,
    srcintf TEXT,
    dstip   TEXT,
    dstport TEXT,
    dstintf TEXT,
    sessionid   TEXT,
    status  TEXT,
    policyid    TEXT,
    dstcountry  TEXT,
    srccountry  TEXT,
    trandisp    TEXT,
    serivce TEXT,
    proto   TEXT,
    duration    TEXT,
    sendbyte    TEXT,
    rcvdbyte    TEXT)
    '''
    cursor.execute(statement)
    return None


def main():
    """
    main function
    """
    # gets arguments from docopt
    arguments = docopt(__doc__)
    dbfile = arguments['<dbfile>']
    print dbfile
    logfile = arguments['<logfile>']
    print logfile

    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    create_table(cursor)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
