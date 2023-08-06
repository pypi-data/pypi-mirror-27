"""This module contains `docker container logs` class"""

from .command import Command


class Logs(Command):
    """This class implements `docker container logs` command"""

    name = "container logs"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["since"] == 0:
            # since cannot be 0, ref: https://github.com/docker/docker-py/blob/9d23278643cb6b4a097e833915a73ab9a2eba10d/docker/api/container.py#L837
            args["since"] = None
        if args["tail"] != 'all':
            args["tail"] = int(args["tail"])
        if args["follow"]:
            args["stream"] = True
            for line in self.client.logs(**args):
                print line,
            self.settings[self.name] = ""
        else:
            logs = self.client.logs(**args)
            self.settings[self.name] = logs if logs else "\r"

    def final(self):
        return self.settings[self.name]
