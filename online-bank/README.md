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

The easiest way to run the app is by downloading the built artifact available from the main repo:

```shell
docker pull ghcr.io/laloloop/scottys-bank:main
```

If Docker is available in your machine, you can run it by building the docker image locally.
```shell
docker build -t scottys-bank .
docker run -it scottys-bank
```

If you prefer python in your local machine, it be executed with the following command.

```shell
python main.py
```

## App concepts

The app is built with the following entities in mind:

* **Store**: Manages the application state, mainly calling to the business rules and UI.
* **Reducers**: Control the overall execution of the application, with events being dispatched to the store. They are meant 
to be pure functions, that is, given a certain state and action, they always produce the same output state.
* **Actions**: Actions are message objects, meaning that they carry a purpose and a body to help alter the application 
state.
* **Renderers**: Components only outputting a string based on the current application's state.
* **Prompters**: Same as Renderers but with the ability to obtain user input, format it and validate it.
* **Entities**: Contain the business rules to be called by the _Reducers_.

## Adding new functionality

To add new functionality consisting of a business rule and an interface to allow the user to execute it is generally 
done in the following way:

1. Add reducer to call the underlying entities and business rules.
2. Add reducer to modify the prompters, e.g. disable the menu and enable the new prompter.
3. Modify / add prompters to allow the users to interact with the new feature.
4. Dispatch actions within existing prompters or add them to the main menu as needed.

## Author

Eduardo Gutiérrez Silva (LaloLoop)