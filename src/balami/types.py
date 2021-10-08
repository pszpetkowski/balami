from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypedDict, TypeVar

if TYPE_CHECKING:
    from balami.base import BaseNode, BaseTokenDescriptor, ChildrenDescriptor

TNode = TypeVar("TNode", bound="BaseNode")


class Constraint(Protocol):
    def validate(self, nodes: list[BaseNode]) -> bool:
        ...


class TokenStructureDict(TypedDict):
    descriptor: BaseTokenDescriptor | ChildrenDescriptor
    required: bool
