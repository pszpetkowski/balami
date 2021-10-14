from __future__ import annotations

import tokenize
from typing import TYPE_CHECKING, Callable, Protocol, TypedDict, TypeVar

if TYPE_CHECKING:
    from balami.base import BaseNode, BaseTokenDescriptor, ChildrenDescriptor

TNode = TypeVar("TNode", bound="BaseNode")

ConstraintCondition = Callable[[list[TNode]], bool]

TokenInfo = tokenize.TokenInfo


class Constraint(Protocol):
    def validate(self, nodes: list[TNode]) -> bool:
        ...


class TokenStructureDict(TypedDict):
    descriptor: BaseTokenDescriptor | ChildrenDescriptor
    required: bool
