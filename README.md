# fg_log_to_sqlite.py
Converts a fortigate log to an sqlite db file. If the db file already exists, 
the script asks if you would like to append to the dbfile.

## Usage

    Usage:fg_to_sqlite
        fg_to_sqlite.py (-l <logfile>)
                        (-d <dbfile>)
    Options:
            -h --help  show help message

## Example

    $ ./fg_to_sqlite.py -l fg.log -d db.db
    Error: db.db exists already
    would you like to append to the dbfile? (y/n): y
    added 29 records to log.db

    $ ./fg_to_sqlite.py -l fg.log -d log.db
    added 29 records to log.db

## Database Contents
The resulting database will have the table *log* where all log entries are saved. 
The table structure looks as follows: 

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


## SQLITE Usage
open the db file: 

    sqlite3 fg.log

print all records: 

    sqlite> SELECT * FROM log;

print only records with “server_lan” as source interface:

    sqlite> SELECT * FROM log WHERE srcintf=”server_lan”;

print only records with source ip 192.168.1.10 and destination interface wan1:

    sqlite> SELECT * FROM log WHERE srcip=”192.168.1.10” and dstintf=”wan1”;

print only blocked records:

    sqlite> SELECT * FROM log WHERE status=”deny”;
