from balami.base import BaseNode


class CountConstraint:
    def __init__(self, count: int, condition) -> None:
        self._count = count
        self._condition = condition

    def validate(self, nodes: list[BaseNode]) -> bool:
        if not self._condition or (self._condition and self._condition(nodes)):
            return len(nodes) <= self._count

        return True
