# Online Bank

This is a simple implementation of the functions expected from an online banking system. The program is not truly 
"online" as it simulates everything locally.

## Features

The App is Console based, meaning you can execute it in every console where Python 3 runs.
The available Banking features are:

1. Create a Bank account
2. Perform an account deposits
3. Perform an account withdraws
4. Perform account transfers

You can quit the application by entering the right option when available.

## Business rules

Some important business rules the program handles are:

* User input is validated and manage according to the operation being performed.
* Negative balance are not permitted.
* Multiple accounts can be created by the running user.

## Running the tests

To run the current tests, execute the following command

```shell
python -m unittest discover
```

Python 3.8.9 is being used for the development.

## Running the main application

The main app can be executed with the following command.

```shell
python main.py
```