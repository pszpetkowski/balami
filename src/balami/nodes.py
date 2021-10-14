from __future__ import annotations

from balami.base import BaseNode, ChildrenDescriptor
from balami.constraints import MaxCountConstraint
from balami.errors import ValidationError
from balami.tokens import (
    CommaTokenDescriptor,
    LParTokenDescriptor,
    NameTokenDescriptor,
    RParTokenDescriptor,
    StarTokenDescriptor,
)


class ModuleImportNode(BaseNode, register=False):
    def __init__(self, module: str, _as: str | None, alias: str | None = None) -> None:
        self.module = module
        self._as = _as
        self.alias = alias

    __repr_fields__ = ["module", "alias"]
    exclusive_syntax = False
    PATTERN = [
        NameTokenDescriptor(typ=str, attr="module")
        | StarTokenDescriptor(value="*", attr="module"),
        NameTokenDescriptor(value="as", attr="_as", required=False),
        NameTokenDescriptor(typ=str, attr="alias", required=False),
    ]

    def validate(self) -> list[ValidationError]:
        errors: list[ValidationError] = []

        if self._as and not self.alias:
            errors.append(
                ValidationError("Keyword 'as' was provided but no alias was found")
            )

        if self.module == "*" and self.alias:
            errors.append(ValidationError("Star import cannot be aliased"))

        return errors

    @staticmethod
    def is_star_import(nodes: list[ModuleImportNode]) -> bool:
        return any([n.module == "*" for n in nodes])


class ImportNode(BaseNode, register=True):
    __repr_fields__ = ["modules"]
    exclusive_syntax = True
    PATTERN = [
        NameTokenDescriptor(value="import"),
        ChildrenDescriptor(
            constraints=[
                MaxCountConstraint(max=0, condition=ModuleImportNode.is_star_import),
            ],
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
            ],
            node=ModuleImportNode,
            separator=CommaTokenDescriptor(required=False),
            attr="modules",
            required=True,
        ),
        RParTokenDescriptor(required=False),
    ]
