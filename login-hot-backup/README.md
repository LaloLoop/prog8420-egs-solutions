# Hot Login

A simple CLI counting user's logins with a local DB and backing up its contents to a CSV file everytime a user access
it.

## Features

The app has the following features.

1. Create a new user.
2. Log in as an existing user.
3. Backup the DB after every login.

The app can be exited from the first menu by writing `exit`.

## Running the tests

To run the current tests, execute the following command

```shell
python -m unittest discover
```

Python 3.8.9 is being used for the development.

## Running the main application

You can run it by building the docker image locally.
```shell
docker build -t hot-login .
docker run -it hot-login
```

If you prefer python in your local machine, it be executed with the following command.

```shell
python main.py
```

## File paths

The application will write and read the following files, please keep them in that location
as they are not configurable at the moment.

**Written to project directory**
* `user.db`: The DB where the users' information is stored
* `userdb-backup.csv`: The backup of the `user.db`, written to the same directory.
* `chyper-code.xlsx`: The spreadsheet containing the cypher mapping.

### About cypher mapping

> ⚠️ Keep in mind that changing the contents of the `chyper-code.xlsx` file in an incompatible way, e.g. changing an 
> existing letter to a new value or deleting it, will cause your existing DB entries to no longer be ciphered 
> appropriately, and no new access counts will be processed. 

Only the first to columns of the file containing the cipher information are read, these columns
are meant to have the `USER TYPE` and `SYSTEM CONVERT` columns to support the ciphering.

## TODO
- [ ] Read cipher info from Excel file.

## Author

Eduardo Gutiérrez Silva (LaloLoop)