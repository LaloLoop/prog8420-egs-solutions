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

## Author

Eduardo Gutiérrez Silva (LaloLoop)