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
            choices=["add", "list", "delete", "do", "done", "pri"],
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
            default="None",
            type=hyphenated,
        )

        try:
            args, unknown = parser.parse_known_args()
        except SystemExit:
            args = parser.parse_args(["action"])
            pass

        if args.action is None:
            with open(self.todo_file, "r") as f:
                items = f.readlines()
                item1, item2 = [], []
                index1, index2 = [], []
                item = []
                for i, line in enumerate(
                    items, start=1
                ):  ##Enhancement 2 The entries are listed First entry 1

                    if line.startswith("("):
                        ### Enhancement 6 ..List items by priority.
                        result = line[line.find("(") + 1 : line.find(")")]
                        ## To sort only with priorty letter
                        if len(result) <= 1:
                            item1.append(line)
                            item1 = sorted(item1)
                        else:
                            item2.append(line)
                            # index2.append(i)
                    else:
                        item2.append(line)
                        # index2.append(i)

            ##Enhancement 3 Prevent different indentation
            for line in item1:
                if line in items:
                    print(
                        f"{items.index(line)+1:{2 if items.index(line)+1<=9 else 0}} {line.strip()} "
                    )

            for line in item2:
                if line in items:
                    print(
                        f"{items.index(line)+1:{2 if items.index(line)+1<=9 else 0}} {line.strip()}"
                    )

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
        args, unknown = parser.parse_known_args()
        # print(args.item)
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
                items[: args.line_number - 1] + items[args.line_number :]
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

    ### Enhancement 7 Enable assigning a priority to an item
    def pri(self):

        parser = argparse.ArgumentParser()
        parser.add_argument("pri", choices=["pri"])
        parser.add_argument("line_number")
        args = parser.parse_args()

        with open(self.todo_file, "r+") as f:
            items = f.readlines()
            val = int(args.line_number[0]) - 1

            for line, data in enumerate(items):
                if line == val:
                    if data.startswith("("):
                        print(f"({args.line_number[1]}) {data[4:].strip()}")
                        items[line] = (
                            f"({args.line_number[1]})" + " " + data[4:].strip() + "\n"
                        )
                        print("yes")
                    else:
                        print(f"({args.line_number[1]}) {data.strip()}")
                        items[line] = (
                            f"({args.line_number[1]})" + " " + data.strip() + "\n"
                        )
                        print("NO")

            f.seek(0)
            for data in items:
                f.write(data)


if __name__ == "__main__":
    handler = Handler()
    handler.handle()
