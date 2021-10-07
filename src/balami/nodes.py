from __future__ import annotations

from balami.base import BaseNode, ChildrenDescriptor
from balami.constraints import CountConstraint
from balami.tokens import (
    CommaTokenDescriptor,
    LParTokenDescriptor,
    NameTokenDescriptor,
    RParTokenDescriptor,
    StarTokenDescriptor,
)


class ModuleImportNode(BaseNode, register=False):
    __repr_fields__ = ["module", "alias"]
    exclusive_syntax = False
    PATTERN = [
        NameTokenDescriptor(typ=str, attr="module")
        | StarTokenDescriptor(value="*", attr="module"),
        NameTokenDescriptor(value="as", required=False),
        NameTokenDescriptor(typ=str, attr="alias", required=False),
    ]

    @staticmethod
    def is_star_import(nodes: list[ModuleImportNode]) -> bool:
        return any([n.module == "*" for n in nodes])


class ImportNode(BaseNode, register=True):
    __repr_fields__ = ["modules"]
    exclusive_syntax = True
    PATTERN = [
        NameTokenDescriptor(value="import"),
        ChildrenDescriptor(
            node=ModuleImportNode,
            separator=CommaTokenDescriptor(required=False),
            attr="modules",
            required=True,
        ),
    ]


class ImportFromNode(BaseNode, register=True):
    __repr_fields__ = ["from", "modules"]
    exclusive_syntax = True
    PATTERN = [
        NameTokenDescriptor(value="from"),
        NameTokenDescriptor(typ=str, attr="from"),
        NameTokenDescriptor(value="import"),
        LParTokenDescriptor(required=False),
        ChildrenDescriptor(
            constraints=[
                CountConstraint(count=1, condition=ModuleImportNode.is_star_import)
            ],
            node=ModuleImportNode,
            separator=CommaTokenDescriptor(required=False),
            attr="modules",
            required=True,
        ),
        RParTokenDescriptor(required=False),
    ]
