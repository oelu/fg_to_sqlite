# fg_log_to_sqlite.py
Converts a fortigate log to an sqlite db file. If the db file allready exists, 
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
