import re


class Command():
    """Input command recognition helper.

    This class will help to recognize the input command.
    Looking for patterns or keywords in the input.
    """

    def __init__(self, value):
        """Sets self.value

        Args:
            value (str): input value
        """
        self.value = value.lower()

    def eq(self, *args):
        """Checks if self.value is equal to some of the given values.

        Args:
            args (str): values to compare with self.value

        Returns:
            boolean: True if some of the given 'args' is equal to self.value
        """
        for value in args:
            if self.value == value.lower():
                return True

        return False

    def has(self, n, *args):
        """Look for strings in self.value

        Check if self.value contains 'n' number (or more)
        of the given values (args).

        Args:
            n (int): minimum number of strings than self.value should contain
            *args (str): Values to look for

        Returns:
            boolean: True if self.value contains 'n' number of the given args
        """
        matches = 0

        for e in args:
            if e.lower() in self.value:
                matches += 1

        if matches >= n:
            return True

        return False

    def find(self, expr):
        """Find a match on self.value for the given regular expresion.

        Args:
            expr (str): Regular expresion

        Returns:
            mixed: False if there is not matches for the regular expr.
                   str if there is a match (value of the match)
        """
        result = re.search(expr, self.value)

        if result:
            return result.group()

        else:
            return False

class Args():
    """Input args parse helper

    When handler gets a message the input is stripped by whitespaces
    first item of the array is the 'command' the rest of the items
    are 'args'. This class provides some utilities to access and validate
    this args easily
    """
    def __init__(self, args):
        """Sets args
        """
        self.args = args

    def get(self, index):
        """Get an arg

        Args:
            index (int): index of the arg
        """
        if len(self.args) > index:
            return self.args[index]

        else:
            return None

    def whole(self):
        """Gets all args as string

        Returns:
            string: args array as string joined by whitespaces.
        """
        return self.args.join(" ")

    def any(self):
        """Checks if there is any arg.

        Returns:
            boolean: True if there are args
        """
        if len(self.args) > 0:
            return True

        return False

    def isint(self, value):
        """Checks if an string is a number.

        Args:
            value (str): string to check if it is a number

        Returns:
            boolean: True if given string is a number
        """
        try:
            value = int(value)
            return True

        except ValueError:
            return False

        except TypeError:
            return False

    def match(self, expr, value):
        """Check if given value matches given regular expresion.

        Args:
            expr (str): Regular expresion
            value (str): value to validate

        Returns:
            boolean: True if value matches with given regular expresion
        """
        if not value:
            return False

        return re.match(expr, str(value))
