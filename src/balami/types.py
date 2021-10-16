import tokenize
from collections import defaultdict
from typing import Callable, Protocol, TypedDict, TypeVar

from balami.base import BaseNode, BaseTokenDescriptor, ChildrenDescriptor

TNode = TypeVar("TNode", bound="BaseNode")

ConstraintCondition = Callable[[list[TNode]], bool]

TokenInfo = tokenize.TokenInfo

ChildNodesDict = defaultdict[str, list[BaseNode]]


class Constraint(Protocol):
    def validate(self, nodes: list[TNode]) -> bool:
        ...


class TokenStructureDict(TypedDict):
    descriptor: BaseTokenDescriptor | ChildrenDescriptor
    required: bool
