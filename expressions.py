from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Real


@dataclass(frozen=True, eq=True)
class Expression(ABC):
    args: tuple[Expression]

    @abstractmethod
    def eval(self: Expression) -> Real:
        """Evaluates the Expression"""
        pass


@dataclass
class Constant(ABC):
    def eval(self: Expression) -> Real:
        return self.args[0]


@dataclass
class Addition(Expression):
    def eval(self: Addition) -> Real:
        return self.args[0] + self.args[1]


@dataclass
class Substraction(Expression):
    def eval(self: Substraction) -> Real:
        return self.args[0] - self.args[1]


@dataclass
class Multiplication(Expression):
    def eval(self: Multiplication) -> Real:
        return self.args[0] * self.args[1]


@dataclass
class Division(Expression):
    def eval(self: Division) -> Real:
        return self.args[0] / self.args[1]
