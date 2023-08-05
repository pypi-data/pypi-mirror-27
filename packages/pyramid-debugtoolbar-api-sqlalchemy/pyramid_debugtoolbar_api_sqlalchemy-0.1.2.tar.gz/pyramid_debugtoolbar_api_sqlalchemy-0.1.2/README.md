pyramid_debugtoolbar_api_sqlalchemy
===================================

This allows for .csv output of sqlalchemy logging.
This package can be useful as part of test suites, allowing developers to run a series of tests and log the SqlAlchemy performance.

If you are using the debugtoolbar directly:

* If SqlAlchemy queries exist on the request, a "SqlAlchemy CSV" tab will appear.  That will prompt you for queries.

If you are scripting:

* The urls are generated in a machine-friendly format, so you can regex the `request_id` off a page and pull it from the API.  this is explained below:


NOTES:
======

This packages requires pyramid_debugtoolbar 4.0 or newer


How to use this package
=======================


Update your ENVIRONMENT.ini file

    debugtoolbar.includes = pyramid_debugtoolbar_api_sqlalchemy

You MUST be using `pyramid_debugtoolbar` with the SqlAlchemy panel enabled.  This just piggybacks on the existing module's work to log queries.

You MUST use `debugtoolbar.includes`.  This will not work properly via `pyramid.includes`

You can access a csv of the SqlAlchemy report via the following url hack:

    url_html = '/_debug_toolbar/{request_id}'
    url_api =  '/_debug_toolbar/api-sqlalchemy/sqlalchemy-{request_id}.csv'
    
The file will be downloaded and offer a content-disposition as:

    sqlalchemy-{request_id}.csv

The CSV columns are:

* execution timing
* sqlalchemy query
* query params (json encoded)