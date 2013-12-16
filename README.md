## About ##

sql4json was originally developed as a cli to help work with json data in a terminal session.  Often json data pulled in from curl, cat, or other command line tools isn't formatted, and is difficult to get the data you are interested in.  sql4json looks to tackle the problem by allowing you to send data via a pipe, or an input redirect, and get the data you are interested using SQL syntax.

In choosing to make this project public I have refactored it so that the sql4json package can be imported and used as a library to access json, or dictionary data.

[Release Notes](https://github.com/bheni/sql4json/blob/master/RELEASE_NOTES.md) (Newest Version: 0.2.1 Released 2013.12.15)

## Installation ##

    sudo pip install sql4json

## Update ##

    sudo pip install --upgrade sql4json
    
## Using the sql4json package in your code ##
##### Querying JSON  #####

    from sql4json.sql4json import *
    
    query = Sql4Json(json_str, sql_str)
    results_dictionary = query.get_results()
    print str(query)

##### Querying data in a Dictionary #####

    from data_query_engine import DataQueryEngine
    
    query = DataQueryEngine(dictionary_with_data, sql_str)
    results_dictionary = query.get_results()

## Command Line Usage ##

sql4json options [SQL*]

\* If SQL is not specified on the command line, an interactive session will begin where
you will be prompted to provide SQL queries. Multiple queries can be run on the same data
set until "quit" or "exit" is entered

options:<br>
--help             - Prints help message<br>
--csv              - Flattens data and outputs it as a csv<br>
--csv-with-headers - Flattens data and outputs it as a csv with the first row being the column headers<br>
  
## Getting Data to sql4json ##

##### JSON From File #####

    cat input_file.json|sql4json "SELECT * FROM some/place WHERE condition==true"
or

    sql4json "SELECT * FROM some/place WHERE condition==true" <input_file.json
    
##### JSON From the web #####

    curl http://httpbin.org/get|sql4json "SELECT * FROM headers"
    
##### JSON From the command line #####

    echo '{"key":"value", "key2":"value 2"}'|sql4json "SELECT *"
    
## Supported SQL Statements ##

Currently sql4json supports select, from, and where clauses which are very similar those seen in standard sql.  The difference being that these statements need to work on a hierarchical data set.  This is supported by using one of the path seperaters '.', '/', or '\'.

##### SELECT Clause #####

The SELECT clause is a comma seperated list of hierarchical elements which are relative to the path specified in the FROM clause

##### FROM Clause #####

The FROM clause specifies the root of the query.  If the root is an array the query is run over each item in the array.  Only one FROM clause can be specified, and all paths specified in the SELECT or WHERE clauses are evaluated relative to this path

##### WHERE Clause #####

The WHERE clause allows you to limit the data in the result sets. Supported operators are "==", "!=", ">", "<", ">=", "<=", "&&", "and", "||", "or", "in", "!" and supports parenthesis for orderring.

## Major Contributors ##

- Jason Gregori
