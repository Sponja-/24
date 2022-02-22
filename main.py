from functools import lru_cache
from itertools import product
from numbers import Real
from typing import Iterable
from more_itertools import powerset
from multiset import FrozenMultiset
from pprint import pprint

from expressions import (
    Addition,
    Constant,
    Division,
    Expression,
    Multiplication,
    Subtraction,
)


binary_operations = (Addition, Subtraction, Multiplication, Division)


@lru_cache
def generate_operations(numbers: FrozenMultiset) -> set[Expression]:
    if len(numbers) == 1:
        elem = next(iter(numbers))
        return set([Constant(elem)])
    else:
        result = set([])
        for s in filter(lambda s: len(s) not in (0, len(numbers)), powerset(numbers)):
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
    print("\nSolutions:")
    print(
        "\n".join(
            [
                str(op).removeprefix("(").removesuffix(")")
                for op in filter_operations(all_ops, 24)
            ]
        )
    )
