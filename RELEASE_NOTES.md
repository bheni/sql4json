## Release Notes ##

##### Version 0.3.0 May 20th 2014 #####

Features
- Added --log-mode for parsing each line as json input
- Added `__key__` keyword for retreiving all the keys at some given path

##### Version 0.2.5 December 30th 2013 #####

Bug Fixes
- Select order now preserved in csv output

##### Version 0.2.4 December 17th 2013 #####

Bug Fixes
- Fixes for issues discovered with OSX Mavericks related to the readline package.

##### Version 0.2.3 December 16th 2013 #####

Bug Fixes
- Fixed issue when root is an array and selecting from /

Features
- Added LIMIT clause

##### Version 0.2.2 December 16th 2013 #####

Features
- Added utility mpack2json.  Can now feed message pack data through mpack2json and pipe it to sql4json

##### Version 0.2.1 December 15th 2013 #####

Features
- Command line history support for interactive sessions

Notes
- Yet to be tested on Windows

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
