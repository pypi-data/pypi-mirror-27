from enum import Enum
class NodeType(Enum):
    ACTION = 0
    CONDITIONAL = 1

class ActionType(Enum):
    END = 0
    ADD = 1
    PUSH_LEFT = 2
    SUBTRACT_LEFT = 3
    PUSH_RIGHT = 4
    SUBTRACT_RIGHT = 5
    PRINT = 6
    READ = 7

class Action:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

class Statement:
    def __init__(self):
        self.kind = None
        self.if_zero = None
        self.if_else = None
        self.next = None
        self.actions = []

    def add_action(self, kind, register):
        if register > 0:
            self.actions.push(Action(ActionType.ADD, register))
        self.actions.push(Action(kind))
