from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from numbers import Real
from typing import Iterable

from multiset import FrozenMultiset
from more_itertools import nth


class Expression(ABC):
    def __init__(self: Expression, *args: Expression | Real) -> None:
        self.args: Iterable[Expression | Real] = args

    @abstractmethod
    def eval(self: Expression) -> Real:
        """Evaluates the Expression"""
        pass

    @abstractmethod
    def __str__(self: Expression) -> str:
        pass

    def __hash__(self: Expression):
        return hash((self.args, type(self)))

    def __eq__(self: Expression, other: Expression):
        return type(self) is type(other) and self.args == other.args


class Constant(Expression):
    def __init__(self: Expression, arg: Real) -> None:
        super().__init__(arg)

    def eval(self: Expression) -> Real:
        return self.value

    def __str__(self: Expression) -> str:
        return str(self.value)

    @property
    def value(self: Constant) -> Real:
        return self.args[0]


class BinaryOperation(Expression):
    def __init__(self: BinaryOperation, *args: Expression) -> None:
        super().__init__(*args)

    def __str__(self: BinaryOperation) -> str:
        return "(" + f" {self.symbol} ".join(map(str, self.args)) + ")"

    @property
    def arg1(self: BinaryOperation) -> Expression:
        return nth(self.args, 0)

    @property
    def arg2(self: BinaryOperation) -> Expression:
        return nth(self.args, 1)

    @property
    @abstractmethod
    def symbol(self: BinaryOperation) -> str:
        pass


class CommutativeAssociativeOperation(BinaryOperation):
    def __init__(self: CommutativeAssociativeOperation, *args: Expression) -> None:
        super().__init__(*args)

        # Association rules
        if type(self.arg2) is type(self):
            self.args = (self.arg1, *self.arg2.args)
        if type(self.arg1) is type(self):
            first, *rest = self.args
            self.args = (*first.args, *rest)
        
        self.args = FrozenMultiset(self.args)  # Ignores order in hashes


class Addition(CommutativeAssociativeOperation):
    symbol = "+"

    def eval(self: Addition) -> Real:
        return sum(arg.eval() for arg in self.args)


class Subtraction(BinaryOperation):
    symbol = "-"

    def eval(self: Subtraction) -> Real:
        return self.arg1.eval() - self.arg2.eval()


class Multiplication(CommutativeAssociativeOperation):
    symbol = "*"

    def eval(self: Multiplication) -> Real:
        return reduce(lambda x, y: x * y, [arg.eval() for arg in self.args])


class Division(BinaryOperation):
    symbol = "/"

    def eval(self: Division) -> Real:
        return self.arg1.eval() / self.arg2.eval()
