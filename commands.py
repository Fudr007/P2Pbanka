from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, command_line: str):
        self.command_line = command_line

    @abstractmethod
    def execute(self) -> str:
        pass

class BCCommand(Command):
    def execute(self) -> str:
        return "BC 0.0.0.0"

class ACCommand(Command):
    def execute(self) -> str:
        return "AC 0/0.0.0.0"

class ADCommand(Command):
    def execute(self) -> str:
        return "AD"

class AWCommand(Command):
    def execute(self) -> str:
        return "AW"

class ABCommand(Command):
    def execute(self) -> str:
        return "AB 0000"

class ARCommand(Command):
    def execute(self) -> str:
        return "AR"

class BACommand(Command):
    def execute(self) -> str:
        return "BA 1"

class BNCommand(Command):
    def execute(self) -> str:
        return "BN 1"