from prompters import MainPrompter
from reducers import main_reducer
from render import MainRenderer
from store import Store


def main():
    store = Store(reducer=main_reducer)
    main_renderer = MainRenderer()
    main_prompter = MainPrompter(store)

    while not store.state['exit']:
        render = main_renderer.render(store.state)
        print(render)

        # TODO Note 1. Issue with user data-entry must be managed by the application
        main_prompter.prompt(store.state)

    exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
