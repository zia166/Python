import argparse

import settings


class Handler:
    def __init__(self):
        self.todo_file = settings.TODO_FILE
        self.done_file = settings.DONE_FILE

    def handle(self):
        """Interpret the first command line argument, and redirect."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["add", "list", "delete", "do", "done"],
            help="The action to take",
        )
        parser.add_argument("other", nargs="?")
        args = parser.parse_args()

        action = getattr(self, args.action)
        action()

    def list(self):
        """Show all items in the todo file."""
        with open(self.todo_file) as f:
            items = f.readlines()
        for i, line in enumerate(items):
            print(f"{i} {line.strip()}")
        print(f"---\n{len(items)} item(s)")

    def done(self):
        """Show all items in the done file."""
        with open(self.done_file) as f:
            items = f.readlines()
        for i, line in enumerate(items):
            print(f"{i} {line.strip()}")
        print(f"---\n{len(items)} item(s) done")

    def add(self):
        """Add a new item to the todo file."""
        ### ....Bug 1 ...
        def singleLine(string):
            return " ".join([word[:] for word in string.split()])

        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add"])
        parser.add_argument("item", type=singleLine)
        args = parser.parse_args()
        with open(self.todo_file, "a") as f:
            f.write(args.item + "\n")

    def do(self):
        """Move an item from the todo file to the done file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["do"])
        parser.add_argument("line_number", type=int)
        args = parser.parse_args()

        # Read in all the todo items
        with open(self.todo_file, "r") as f:
            items = f.readlines()

        # Append the done item to the done file
        # ..bug 2...IndexError avoided
        with open(self.done_file, "a") as f:
            try:
                f.write(items[args.line_number])
            except IndexError:

                print(
                    f"There is no item {args.line_number}. Please choose a number from 0 to {len(items)-1}"
                )
                return

        # Write out all but the done items
        with open(self.todo_file, "w") as f:
            new_todos = "".join(
                items[: args.line_number] + items[args.line_number + 1 :]
            )
            f.write(new_todos)

        print(f"Done: {items[args.line_number].strip()}")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
