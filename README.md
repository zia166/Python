# To Do list

This is a basic to do list tool. It stores information in a simple text file:

```
Buy chips
Eat chips
```

and gives the user the ability to add, display, or "do" items from the list.

## About the test

There are some intentional bugs, and some missing features, which we'd like you to address.

We will review your changes as though they were made on a real project. This is an opportunity for you to show us your best work. We are looking not just for good code, but also for evidence of what working with you will be like:

- How do you communicate?
- How well have you identified the correct source of a bug?
- Does your new code behave as expected?
- Have you introduced any new bugs?

There is a test suite, which will help you with completing the task. Adding to the tests will help you to know whether your newly added features are working well.

If you have any trouble getting the project to work locally, please contact recruitment@torchbox.com.

## How it is assessed

Each bug fix or enhancement is worth a certain number of marks, for attributes such as effectiveness, comprehensiveness, maintainability, and testing, e.g. for a 7-mark task:

- 1 mark if you make a reasonable attempt at the solution (i.e. it works in the simplest case)
- 2 marks available for the solution fulfilling the stated requirements (i.e. the output matches the example given)
- 1 mark for the solution working in edge cases (i.e. with bad input, or missing data)
- 2 marks available for adding unit tests of the new behaviour, or updating existing unit tests to account for changed behaviour
- 1 mark for clean, maintainable code (i.e. not using anything overcomplicated, hard to understand, or approaches which are recommended against in Python)

After reviewing each individual task, there are also some general marks awarded overall for code quality, use of git, communication, etc.

### Clean code

We're looking for code that is easy to follow, and does not overcomplicate things.

Standard ways of doing things are good. For example, if you do a common task such as finding the biggest item in a list, we would prefer you to use Python's built in `max()` function. You don't need to write your own algorithm to work through the list. Use the Python standard library. You are unlikely to need to install additional packages.

Your code should not have unintended side effects. Every time you make a change, you should check that the to do list still behaves. You can do this manually, or by running the tests (see below).

### Communication

Each change (Bug 1, Enhancement 1 etc.) should be in its own commit, or multiple commits. You should not combine multiple features or fixes into one commit.

### Working code

A good tip is to test with the example given in the task description. If your code doesn't produce the same output as the example, maybe something is not right.

## Installation

Python 3.9 or higher is required.

You may like to use the example todo.txt and done.txt files, in which case run:

```bash
$ cp examples/todo.txt todo.txt
$ cp examples/done.txt done.txt
```

## Usage

All example commands assume you are in the project directory.

### List items

You can list all items with the command `list`

```
$ python todo.py list
0 Buy chips
1 Eat chips
---
2 item(s)
```

### Add items

You can add a new item with the command `add "[description]"`

```
$ python todo.py add "Tidy up"
$ python todo.py list
0 Buy chips
1 Eat chips
2 Tidy up
---
3 item(s)
```

### Do items

You can mark an item as done with the command `do [item number]`

```
$ python todo.py do 0
Done: Buy chips
$ python todo.py list
0 Eat chips
1 Tidy up
---
2 item(s)
```

### Done items

You can list done items with the command `done`

```
$ python todo.py done
0 Buy chips
---
1 item(s) done
```

## Testing

You can run tests with the module `test.py`

```
$ python test.py
...........
----------------------------------------------------------------------
Ran 11 tests in 0.050s

OK
$
```

Every time you make a change, you should check that the tests still pass. Sometimes a feature may change the behaviour slightly, requiring a change to existing tests.

If you add a new feature, you should consider adding a test for it. Tests can check things like the correct behaviour for good input, as well as making sure bad input doesn't create problems.

## Tasks

### Bug 1 (4 marks)

It is possible to create two entries by including a line break (i.e. pressing Enter before closing the quote marks):

```
$ python todo.py add "Hello,
dquote> World\!"
$ python todo.py list
0 Hello,
1 World!
```

This should be prevented, so that the entry appears as "Hello, World!". Note: there is already a failing test for this. Fixing the bug correctly will make that test pass.

### Bug 2 (7 marks)

Currently the "do" command fails when given a bad line number

```
$ python todo.py list
0 Hello, World!
1 Begin plans for world domination
2 Listen to Symphony for the New World
3 Improve Python todo project
---
3 item(s)
$ python todo.py do 6
Traceback (most recent call last):
  File "/home/nick/code/todo_list/todo.py", line 72, in <module>
    handler.handle()
  File "/home/nick/code/todo_list/todo.py", line 22, in handle
    action()
  File "/home/nick/code/todo_list/todo.py", line 61, in do
    f.write(items[args.line_number])
IndexError: list index out of range
```

This should be prevented, e.g. by showing a user friendly message:

```
$ python todo.py do 6
There is no item 6. Please choose a number from 0 to 3
```

### Enhancement 1 (6 marks)

When an item is done, append the date in the done.txt file.

```
$ python todo.py done
0 Add date to done file (2022-04-25)
---
1 item(s) done
```

### Enhancement 2 (6 marks)

The entries are listed

```
0 First line of todo.txt
1 Second line
2 Third line
```

Change the code so that the first entry is 1, the second 2, etc.

Note that you will need to make sure the `do` command works with the new numbering scheme.

### Enhancement 3 (5 marks)

Prevent different indentation, e.g.

```
9 Something
10 Something else
```

should instead appear as

```
 9 Something
10 Something else
```

Your fix should continue to work when there are 100 or 1000 entries, and so on.

### Enhancement 4 (4 marks)

Implement deletion, such that you can type:

```
$ python todo.py list
1 Plnat seedlings
2 Plant seedlings
---
2 item(s)
$ python todo.py delete 1
Deleted: Plnat seedlings
$ python todo.py list
1 Plant seedlings
---
1 item(s)
```

### Enhancement 5 (8 marks)

Add filtering: show only those lines containing the given string

```
$ python todo.py list world
8  Plan world domination
14 Listen to New World Symphony
```

The original line numbers should be displayed.

The filter argument should be optional; the command `todo.py list` should still work.

### Enhancement 6 (10 marks)

List items by priority. The format should be a single capital letter in brackets at the start of the line, but the original line numbers should be kept e.g.:

```
$ python todo.py list
2 (A) Most important thing
4 (E) Medium importance item
1 (Z) Least important thing
3 Unranked thing
5 Another unranked thing
```

Items of the same priority should be ordered by line number.

### Enhancement 7 (7 marks)

Enable assigning a priority to an item:

```
$ python todo.py pri 1 B
$ python todo.py list
2 (A) Most important thing
1 (B) Least important thing
4 (E) Medium importance item
3 Unranked thing
```

Your change should work with items which already have a priority, and those which have no priority yet assigned.
