from datetime import datetime
import argparse
import re
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

        def hyphenated(string):
            return " ".join([word[:] for word in string.casefold().split()])

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            nargs="?",
            choices=["list"],
        )
        parser.add_argument(
            "search",
            default=None,
            type=hyphenated,
        )
        args = parser.parse_args()
        print(args.action)
        if args.action is None:
            with open(self.todo_file, "r") as f:
                items = f.readlines()
                item1, item2 = [], []
                index1, index2 = [], []
                for i, line in enumerate(
                    items, start=1
                ):  ##Enhancement 2 The entries are listed First entry 1

                    if line.startswith(
                        "("
                    ):  ### Enhancement 6 ..List items by priority.
                        result = line[line.find("(") + 1 : line.find(")")]
                        item1.append(line)
                        index1.append(i)
                        item1 = sorted(item1)
                    else:
                        item2.append(line)
                        index2.append(i)

                i = 0
                for line in item1:
                    ##Enhancement 3 Prevent different indentation
                    print(f"{index1[i]:{2 if i<=9 else 0}} {line}")
                    i = i + 1
                i = 0
                for val in item2:
                    print(f"{index2[i]:{2 if i<=9 else 0}} {val}")
                    i = i + 1
        else:
            with open(self.todo_file, "r") as f:
                items = f.readlines()
                ### Enhancement 5 Add filtering
                for i, lines in enumerate(items, start=1):
                    result = re.findall(args.search, lines, flags=re.IGNORECASE)
                    if result:
                        print(f"{i:{2 if i<=9 else 0}} {lines.strip()}")

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
                #### Enhancement 1 append the date in the done.txt file.
                current_datetime = datetime.now()

                f.write(
                    "\n %s (%s)"
                    % (
                        items[args.line_number - 1].strip(),
                        current_datetime.strftime("%d-%m-%Y"),
                    )
                )
            except IndexError:

                print(
                    f"There is no item {args.line_number}. Please choose a number from 1 to {len(items)}"
                )
                return

        # Write out all but the done items
        with open(self.todo_file, "w") as f:
            new_todos = "".join(
                items[: args.line_number] + items[args.line_number + 1 :]
            )
            f.write(new_todos)

        print(f"Done: {items[args.line_number-1].strip()}")

    ### Enhancement 4 Implement deletion

    def delete(self):

        """delete item from todo file."""
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["delete"])
        parser.add_argument("item", type=int)
        args = parser.parse_args()

        with open(self.todo_file, "r") as f:
            items = f.readlines()
            with open(self.todo_file, "w") as f:
                for line, data in enumerate(items, start=1):
                    if line != args.item:
                        f.write(data)
        print(f"Deleted: {items[args.item -1].strip()}")


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
