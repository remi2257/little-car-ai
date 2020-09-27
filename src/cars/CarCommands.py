from enum import Enum


class Command(Enum):
    pass


class CommandDir(Command):
    LEFT = 1
    NONE = 2
    RIGHT = 3


class CommandGas(Command):
    BRAKE = 1
    OFF = 2
    ON = 3
