from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
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
        left, right = map(
            lambda arg: f"({str(arg)})" if type(arg) is not Constant else str(arg),
            (self.arg1, self.arg2),
        )
        return f"{left} {self.symbol} {right}"

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


class CommutativeOperation(BinaryOperation):
    def __init__(self: CommutativeOperation, *args: Expression) -> None:
        super().__init__(*args)
        self.args = FrozenMultiset(args)  # Ignores order in hashing


class Addition(CommutativeOperation):
    symbol = "+"

    def eval(self: Addition) -> Real:
        return self.arg1.eval() + self.arg2.eval()


class Subtraction(BinaryOperation):
    symbol = "-"

    def eval(self: Subtraction) -> Real:
        return self.arg1.eval() - self.arg2.eval()


class Multiplication(CommutativeOperation):
    symbol = "*"

    def eval(self: Multiplication) -> Real:
        return self.arg1.eval() * self.arg2.eval()


class Division(BinaryOperation):
    symbol = "/"

    def eval(self: Division) -> Real:
        return self.arg1.eval() / self.arg2.eval()
