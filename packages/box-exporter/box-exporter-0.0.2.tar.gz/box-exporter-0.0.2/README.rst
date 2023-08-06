box-exporter
============

**A simple python command line application that can query any relational database
and upload the data to a folder on https://box.com**

This package will allow you to:

* Just write SQL
* Export results to box

This application attempts to make the common task of extracting data and uploading
to box.com as simple, reproducible, and maintainable as possible.

Basics
======

We'll assume for this quickstart that the working directory is ``/app``.

Set the following environmental variables.

::

    BOX_CLIENT_ID
    BOX_CLIENT_SECRET
    BOX_ENTERPRISE_ID
    BOX_RSA_PRIVATE_KEY_PASS
    BOX_RSA_PRIVATE_KEY_PATH
    BOX_JWT_KEY_ID
    BOX_FOLDER_ID
    DATABASE_URL

-- OR --

You can also copy the included .env.example file and insert the values.

::

    cp .env.example .env

Create a sql directory and ``*.sql`` file with the query you would like to use.

::

    mkdir sql
    echo "SELECT * FROM users" > /app/sql/query.sql

Run the box-exporter command with the correct arguments. If you have all the environmental
variables it's as easy as:

``boxex <query_file_path> <filename>``

Run the query

::

    boxex /app/sql/query.sql data_export.csv

A More Advanced Example
=======================

Being able to export a file to box at the commandline itself isn't really all
that useful if it cannot be done on a schedule. Typically someone will want to
run a query either hourly, daily, or weekly.

We can run exports with a specific filename and schedule using a combination of
a bash script and a crontab entry.

Create a bash script:

**/app/bin/export_data.sh**

::

    #!/bin/bash

    export BOX_CLIENT_ID=aboxclientid
    export BOX_CLIENT_SECRET=aboxclientsecret
    export BOX_ENTERPRISE_ID=anenterpriseid
    export BOX_RSA_PRIVATE_KEY_PASS=adevsecret
    export BOX_RSA_PRIVATE_KEY_PATH=/privatekey/path
    export BOX_JWT_KEY_ID=jwtkeyid
    export BOX_FOLDER_ID=123456
    export DATABASE_URL=postgres://postgres@localhost/db

    boxex /app/sql/query.sql research_export-$(date '+%Y-%m-%d').csv


Add the following line to your crontab file

::

    30  18  *   *   *   /app/bin/export_data.sh

The following will run everyday at 6:30PM

