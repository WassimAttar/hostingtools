# MysqlDefrag

Defragmentation of Mysql databases with MyISAM and InnoDB engines.

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [USE CASES](#use-cases)

### DESCRIPTION
**mysqldefrag** checks, analyses, optimizes and repairs mysql databases with MyISAM and InnoDB engines.

An alert is raised if a table is corrupted or an error occurs.

A report can be sent by email.

A dump of the databases is also available for backup.

The script is compatible with python 2 and 3.

This script is designed to run daily as a cronjob to check the health of databases.

### INSTALLATION
Download the script

    wget https://github.com/WassimAttar/hostingtools/raw/master/mysqldefrag.py

Make sure you have installed python-mysqldb or python-mysql.connector modules.

The mysql root password is saved in the mysql config file /root/.my.cnf

Check that you have this entry

    [client]
    password=p4ss0rD

### USE CASES
Silent mode : checks, analyses, optimizes and repairs all mysql databases

    python mysqldefrag.py

Verbose mode : checks, analyses, optimizes and repairs all mysql databases with short details

    python mysqldefrag.py -v
    ----------------------------------
    DataBase : `wp-tech`
    77 CHECK in 1.214 seconds
    77 ANALYZE in 0.035 seconds
    75 OPTIMIZE in 7.659 seconds
    75 REPAIR in 0.112 seconds
    ----------------------------------

More verbose mode : checks, analyses, optimizes and repairs all mysql databases with long details

    python mysqldefrag.py -vv
    ----------------------------------
    DataBase : `wp-tech`
    19 ANALYZE in 0.021 seconds
    ANALYZE `commentmeta` InnoDB OK
    ANALYZE `comments` InnoDB OK
    ANALYZE `links` InnoDB OK
    ANALYZE `options` InnoDB OK
    ANALYZE `postmeta` InnoDB OK
    ANALYZE `posts` InnoDB OK
    ANALYZE `signups` InnoDB OK
    ANALYZE `term_relationships` InnoDB OK
    ANALYZE `term_taxonomy` InnoDB OK
    ANALYZE `terms` InnoDB OK
    ANALYZE `usermeta` InnoDB OK
    ANALYZE `users` InnoDB OK

Send report by mail : checks, analyses, optimizes and repairs all mysql databases with short details sent by mail

    python mysqldefrag.py --email john@doe.com

Dumps databases for backup : checks, analyses, optimizes and repairs all mysql databases and dump them into a folder

    python mysqldefrag.py --dumppath /root/dump_database/

Main use of mysqldefrag, daily cronjob : checks, analyses, optimizes and repairs all mysql databases, dump them into a folder and sends a report by mail at 4 AM

    0 4 * * * python mysqldefrag.py --email john@doe.com --dumppath /root/dump_database/


# MysqlUp

Checks if Mysql is up.

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [USE CASES](#use-cases)

### DESCRIPTION
**mysqlup** checks if mysql is up.

An alert is raised if mysql is down and can be sent by email.

The script is compatible with python 2 and 3.

This script is designed to run as a cronjob to check if mysql is up.

### INSTALLATION
Download the script

    wget https://github.com/WassimAttar/hostingtools/raw/master/mysqlup.py

Make sure you have installed python-mysqldb or python-mysql.connector modules.

The mysql root password is saved in the mysql config file /root/.my.cnf

Check that you have this entry

    [client]
    password=p4ss0rD

### USE CASES
Silent mode : checks if mysql is down, in this case, mysql is restarted.

    python mysqlup.py

Verbose mode : checks if mysql is down, in this case, mysql is restarted.

    python mysqlup.py -v
    ----------------------------------
    Mysql Down
    Restarting
    ----------------------------------

Send alert by mail

    python mysqlup.py --email john@doe.com

Main use of mysqlup, daily cronjob : send alert by mail if mysql is down

    * * * * * python mysqlup.py --email john@doe.com

# DeleteOldBackup

Deletes old backups when hard drive is full.

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [USE CASES](#use-cases)

### DESCRIPTION
**deleteoldbackup** frees space of old backups.

The script is compatible with python 2 and 3.

This script is designed to run daily as a cronjob to check the free space.

### INSTALLATION
Download the script

    wget https://github.com/WassimAttar/hostingtools/raw/master/deleteoldbackup.py

### USE CASES
Silent mode : frees space.

    python deleteoldbackup.py

Verbose mode : frees space and echoes details.

    python deleteoldbackup.py -v
    ----------------------------------
		Free space before : 35Go
		Free space after : 43Go
		Freed space : 8Go
		---------------------
		delete 2016-06-01 : 4Go
		delete 2016-06-02 : 3Go
		delete 2016-06-03 : 1Go
    ----------------------------------

Send alert by mail

    python deleteoldbackup.py --email john@doe.com

Main use of deleteoldbackup, daily cronjob : send alert by mail when space is freed

    * * * * * python deleteoldbackup.py --email john@doe.com