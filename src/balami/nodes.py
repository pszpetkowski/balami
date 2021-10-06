from balami.base import BaseNode, ChildrenDescriptor
from balami.tokens import NameTokenDescriptor, OpTokenDescriptor


class ModuleImportNode(BaseNode, register=False):
    __repr_fields__ = ["module", "alias"]
    exclusive_syntax = False
    PATTERN = [
        NameTokenDescriptor(typ=str, attr="module"),
        NameTokenDescriptor(value="as", required=False),
        NameTokenDescriptor(typ=str, attr="alias", required=False),
    ]


class ImportNode(BaseNode, register=True):
    __repr_fields__ = ["modules"]
    exclusive_syntax = True
    PATTERN = [
        NameTokenDescriptor(value="import"),
        ChildrenDescriptor(
            node=ModuleImportNode,
            separator=OpTokenDescriptor(value=",", required=False),
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
        OpTokenDescriptor(value="(", required=False),
        ChildrenDescriptor(
            node=ModuleImportNode,
            separator=OpTokenDescriptor(value=",", required=False),
            attr="modules",
            required=True,
        ),
        OpTokenDescriptor(value=")", required=False),
    ]
