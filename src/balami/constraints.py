from typing import Callable

from balami.types import TNode


class CountConstraint:
    def __init__(self, count: int, condition: Callable[[list[TNode]], bool]) -> None:
        self._count = count
        self._condition = condition

    def validate(self, nodes: list[TNode]) -> bool:
        if not self._condition or (self._condition and self._condition(nodes)):
            return len(nodes) <= self._count

        return True
