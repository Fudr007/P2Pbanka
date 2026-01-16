from commands import *

class CommandDistribution:
    def __init__(self):
        self.commands = {
            "BC": BCCommand,
            "AC": ACCommand,
            "AD": ADCommand,
            "AW": AWCommand,
            "AB": ABCommand,
            "AR": ARCommand,
            "BA": BACommand,
            "BN": BNCommand,
        }

    def distribute(self, line: bytes):
        if not line.decode("utf-8").strip():
            return "ER Empty command"

        code = line[:2]
        code = code.decode("utf-8")
        content = line[2:]
        content = content.decode("utf-8").strip()

        if code in self.commands:
            return self.commands[code](content).execute()
        return "ER Unknown command"