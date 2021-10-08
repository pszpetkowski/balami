from __future__ import annotations

from balami.base import BaseNode, ChildrenDescriptor
from balami.constraints import FuncConstraint, MaxCountConstraint
from balami.tokens import (
    CommaTokenDescriptor,
    LParTokenDescriptor,
    NameTokenDescriptor,
    RParTokenDescriptor,
    StarTokenDescriptor,
)


class ModuleImportNode(BaseNode, register=False):
    def __init__(self, module: str, alias: str | None = None) -> None:
        self.module = module
        self.alias = alias

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

    @staticmethod
    def star_import_no_alias(nodes: list[ModuleImportNode]) -> bool:
        for node in nodes:
            if node.module == "*" and node.alias:
                return False
        return True


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
                MaxCountConstraint(max=1, condition=ModuleImportNode.is_star_import),
                FuncConstraint(func=ModuleImportNode.star_import_no_alias),
            ],
            node=ModuleImportNode,
            separator=CommaTokenDescriptor(required=False),
            attr="modules",
            required=True,
        ),
        RParTokenDescriptor(required=False),
    ]
