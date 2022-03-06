from functools import cache
from itertools import product
from numbers import Real
from typing import Iterable

from multiset import FrozenMultiset

from expressions import (
    Addition,
    Constant,
    Division,
    Expression,
    Multiplication,
    Subtraction,
)
from utils import strict_powerset


binary_operations = (Addition, Subtraction, Multiplication, Division)


@cache
def generate_operations(numbers: FrozenMultiset) -> set[Expression]:
    if len(numbers) == 1:
        elem = next(iter(numbers))
        return set([Constant(elem)])
    else:
        result = set([])
        for s in strict_powerset(numbers):
            setA = FrozenMultiset(s)
            setB = numbers - setA
            for arg1, arg2 in product(*map(generate_operations, (setA, setB))):
                result |= set(op_type(arg1, arg2) for op_type in binary_operations)
        return result


def filter_operations(
    operations: Iterable[Expression], target: Real
) -> set[Expression]:
    result = set([])
    for op in operations:
        try:
            if op.eval() == target:
                result.add(op)
        except ZeroDivisionError:
            pass
    return result


if __name__ == "__main__":
    cards = map(int, input("Space-separated card values:\n").split())
    all_ops = generate_operations(FrozenMultiset(cards))
    if len(all_ops) > 0:
        print("\nSolutions:")
        print(
            "\n".join(
                [
                    str(op).removeprefix("(").removesuffix(")")
                    for op in filter_operations(all_ops, 24)
                ]
            )
        )
    else:
        print("No Solutions")
