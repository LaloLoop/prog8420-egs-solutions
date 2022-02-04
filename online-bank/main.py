def say_hi(username):
    print("Hi", username, sep=",", end="!\n")


def main():

    while True:
        print("""
        What would you like to do today?
        1. Say hi!
        2. Exit
        """)

        # TODO Note 1. Issue with user data-entry must be managed by the application
        option = input(">")

        # 5. Quit Application
        if option == "2":
            print("See you later!")
            break
        elif option == "1":
            username = input("What's your name?")
            say_hi(username)
        else:
            print("Sorry, I cannot help you with that!")

    exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
