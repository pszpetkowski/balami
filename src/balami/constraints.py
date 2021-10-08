from typing import Generic

from balami.types import ConstraintCondition, TNode


class MaxCountConstraint(Generic[TNode]):
    def __init__(self, max: int, condition: ConstraintCondition[TNode]) -> None:
        self._max = max
        self._condition = condition

    def validate(self, nodes: list[TNode]) -> bool:
        if not self._condition or (self._condition and self._condition(nodes)):
            return len(nodes) <= self._max

        return True


class FuncConstraint(Generic[TNode]):
    def __init__(self, func: ConstraintCondition[TNode]) -> None:
        self._func = func

    def validate(self, nodes: list[TNode]) -> bool:
        return self._func(nodes)
