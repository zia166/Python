import sys
import unittest
from io import StringIO
from textwrap import dedent
from unittest.mock import call, mock_open, patch

from todo import Handler


class PrintTestCase(unittest.TestCase):
    """A custom TestCase to capture print output, and make assertions about it."""

    def run(self, result=None):
        with patch.object(sys, "stdout", new_callable=StringIO) as mock_stdout:
            self.mock_stdout = mock_stdout
            super().run(result)

    def assertPrinted(self, expected):
        self.assertEqual(self.mock_stdout.getvalue(), expected)


class TestList(PrintTestCase):
    def test_action(self):
        """Test that the list() method is called"""
        testargs = ["todo.py", "list"]
        with patch.object(sys, "argv", testargs):
            handler = Handler()
            with patch.object(handler, "list") as mock_list:
                handler.handle()
                mock_list.assert_called_once_with()

    def test_basic(self):
        with patch("todo.open", mock_open(read_data="One\nTwo\n")):
            Handler().list()
        expected = dedent(
            """\
            0 One
            1 Two
            ---
            2 item(s)
            """
        )
        self.assertPrinted(expected)

    def test_empty(self):
        """Ensure that an empty file prints only the summary"""
        with patch("todo.open", mock_open()):
            Handler().list()
        expected = dedent(
            """\
            ---
            0 item(s)
            """
        )
        self.assertPrinted(expected)

    def test_a_long_list(self):
        """Test that we can show a long list going into double figures"""
        with patch(
            "todo.open",
            mock_open(
                read_data="One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen\nEleven"
            ),
        ):
            Handler().list()
        expected = dedent(
            """\
            0 One
            1 Two
            2 Three
            3 Four
            4 Five
            5 Six
            6 Seven
            7 Eight
            8 Nine
            9 Ten
            10 Eleven
            ---
            11 item(s)
            """
        )
        self.assertPrinted(expected)


class TestAdd(PrintTestCase):
    def test_action(self):
        """Test that the add() method is called"""
        testargs = ["todo.py", "add", "Do things"]
        with patch.object(sys, "argv", testargs):
            handler = Handler()
            with patch.object(handler, "add") as mock_add:
                handler.handle()
                mock_add.assert_called_once_with()

    def test_file_handling(self):
        """Test that the file is opened in 'a' mode in a context manager"""
        m = mock_open()
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "add", "Foo"]):
                Handler().add()
        self.assertEqual(m.mock_calls[0], call("todo.txt", "a"))
        self.assertEqual(m.mock_calls[1], call().__enter__())

    def test_basic(self):
        m = mock_open()
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "add", "New item"]):
                Handler().add()
        self.assertEqual(m.mock_calls[2], call().write("New item\n"))
        self.assertPrinted("")

    def test_newline(self):
        """Test that the file ends with a newline character

        This is implicitly tested in test_basic, but for regression test purposes we
        test it explicitly here.
        """
        m = mock_open()
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "add", "Foo"]):
                Handler().add()
        # The file is opened in "append" mode
        self.assertEqual(m.mock_calls[0], call("todo.txt", "a"))
        # The final character written is a newline character
        self.assertTrue(m.mock_calls[2].args[0].endswith("\n"))

    def test_line_breaks_are_ignored(self):
        m = mock_open()
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "add", "New\nitem"]):
                Handler().add()
        self.assertEqual(m.mock_calls[2], call().write("New item\n"))
        self.assertPrinted("")


class TestDo(PrintTestCase):
    def assertAppendedToDoneFile(self, mock_open, text):
        """Utility method to assert the given text is appended to the done.txt file"""
        self.assertEqual(mock_open.mock_calls[4], call("done.txt", "a"))
        self.assertEqual(mock_open.mock_calls[6], call().write(text))

    def assertWrittenToTodoFile(self, mock_open, text):
        """Utility method to assert the given text is writen to the todo.txt file"""
        self.assertEqual(mock_open.mock_calls[8], call("todo.txt", "w"))
        self.assertEqual(mock_open.mock_calls[10], call().write(text))

    def test_action(self):
        """Test that the do() method is called"""
        testargs = ["todo.py", "do", "1"]
        with patch.object(sys, "argv", testargs):
            handler = Handler()
            with patch.object(handler, "do") as mock_do:
                handler.handle()
                mock_do.assert_called_once_with()

    def test_file_handling_sequence(self):
        """Tests of the todo file handling sequence"""
        m = mock_open(read_data="One\nTwo\nThree\n")
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "do", "1"]):
                Handler().handle()
        self.maxDiff = None
        expected_calls = [
            call("todo.txt", "r"),  # open todo.txt in read mode
            call().__enter__(),
            call().readlines(),  # read todo.txt
            call().__exit__(None, None, None),
            call("done.txt", "a"),  # open done.txt in append mode
            call().__enter__(),
            call().write("Two\n"),  # write "Two" to done.txt
            call().__exit__(None, None, None),
            call("todo.txt", "w"),
            call().__enter__(),
            call().write("One\nThree\n"),  # write "One\nThree\n" to todo.txt
            call().__exit__(None, None, None),
        ]
        for actual, expected in zip(m.mock_calls, expected_calls):
            self.assertEqual(actual, expected)
        self.assertListEqual(m.mock_calls, expected_calls)

    def test_doing_the_first_item(self):
        m = mock_open(read_data="One\nTwo\nThree\n")
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "do", "0"]):
                Handler().handle()

        self.assertEqual(len(m.mock_calls), 12)
        self.assertAppendedToDoneFile(m, "One\n")
        self.assertWrittenToTodoFile(m, "Two\nThree\n")
        self.assertPrinted("Done: One\n")

    def test_doing_the_last_item(self):
        m = mock_open(read_data="One\nTwo\nThree\n")
        with patch("todo.open", m):
            with patch.object(sys, "argv", ["todo.py", "do", "2"]):
                Handler().handle()

        self.assertEqual(len(m.mock_calls), 12)
        self.assertAppendedToDoneFile(m, "Three\n")
        self.assertWrittenToTodoFile(m, "One\nTwo\n")
        self.assertPrinted("Done: Three\n")


if __name__ == "__main__":
    unittest.main()
