import json


class Environment():
    """Erina's environment vars.

    Env vars save some parameters like session cookies and
    configuration parameters. Env vars are saved on json files so
    each component of the system (even they are executed independently)
    can access them and modify them on-the-fly.
    """

    def __init__(self):
        """Sets the json file path.
        """
        self.env_file = "_data/env.json"

    def load(self):
        """Loads env vars (reads the json file)
        """
        with open(self.env_file, "r") as f:
            self.variables = json.load(f)

    def get(self, var):
        """Gets an env var.

        Args:
            var (str): env var name

        Returns:
            mixed: var value (None if var is not set)
        """
        self.load()

        if var in self.variables:
            return self.variables[var]

        return None

    def set(self, var, val):
        """Sets env var value.

        Args:
            var (str): env var name
            val: var value
        """
        self.load()
        self.variables[var] = val

        with open(self.env_file, "w") as f:
            json.dump(self.variables, f, sort_keys=True, indent=4)
