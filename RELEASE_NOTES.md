## Release Notes ##

##### Version 0.2 December 15th 2013 #####

Features
- FlatData class for flattenning hierarchical data
- new command line options --help, --csv, --csv-with-headers
- interactive session - When no SQL is specified on the command line you will be prompted to specify a query.  Once that query completes you will be prompted for another.  You will continue to be prompted for new queries until 'exit' or 'quit' are specified as the command.  All queries are run on the same data set.

Known Issues
- No command history support in interactive sessions which sucks

##### Version 0.1 December 12th 2013 #####

Initial release with base functionality. Features Include:
- Framework for boolean expression evaluation
- Package for querying hierarchical python data
- Helper classes specifically for JSON
- SQL select from and where clauses
- CLI for working with json data sent to stdin
- Pip install support
 
Known Issues
- Does not handle multiple objects with the same path properly (Which occurs with arrays)
