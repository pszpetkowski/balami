from __future__ import annotations

import tokenize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balami.types import Constraint, TNode, TokenStructureDict

NODE_REGISTRY: list[type[BaseNode]] = []


class BaseDescriptor:
    def __init__(self, attr: str | None = None, required: bool = True) -> None:
        self.attr = attr
        self.required = required


class ChildrenDescriptor(BaseDescriptor):
    def __init__(
        self,
        node: type[BaseNode],
        separator: BaseTokenDescriptor,
        attr: str,
        required: bool = True,
        constraints: list[Constraint] | None = None,
    ) -> None:
        self.node = node
        self.separator = separator
        self.attr = attr
        self.required = required
        self.constraints = constraints or []


class BaseTokenDescriptor(BaseDescriptor):
    PY_TOKEN: int

    def __init__(
        self,
        value: str | None = None,
        typ: type | None = None,
        attr: str | None = None,
        required: bool = True,
    ) -> None:
        if value and typ:
            raise RuntimeError("cannot provide both expected value and type")

        self._value = value
        self._typ = typ
        self.alt: list[BaseTokenDescriptor] = []
        super().__init__(attr, required)

    def __or__(self, other: BaseTokenDescriptor) -> BaseTokenDescriptor:
        self.alt.append(other)
        return self

    def match_token(self, py_token: tokenize.TokenInfo) -> str | None:
        return py_token.string


class BaseNode:
    __repr_fields__: list[str]
    exclusive_syntax: bool
    PATTERN: list[BaseTokenDescriptor | ChildrenDescriptor]
    _py_structure: list[TokenStructureDict]
    parent_attr: str

    def __init_subclass__(cls, register: bool) -> None:
        cls._py_structure = []
        for descriptor in cls.PATTERN:
            cls._py_structure.append(
                {"descriptor": descriptor, "required": descriptor.required}
            )
        if register:
            NODE_REGISTRY.append(cls)

    def __init__(self, **kwargs: dict[str, str]) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        values = [
            f"{field_name}={getattr(self, field_name, 'None')}"
            for field_name in self.__repr_fields__
        ]
        return f"<{type(self).__name__ }({', '.join(values)})>"

    @classmethod
    def match(
        cls: type[TNode], py_tokens: list[tokenize.TokenInfo], exhausting: bool = True
    ) -> TNode | None:
        pattern_tokens, matched_tokens, child_nodes = cls._match_structure(
            py_tokens, exhausting
        )
        instance_data: dict[str, str] = {}
        for ix, py_token in enumerate(matched_tokens):
            attr = pattern_tokens[ix].attr
            value = pattern_tokens[ix].match_token(py_token)
            if not value:
                # TODO: Add exclusive_syntax related instructions
                return None

            if attr:
                instance_data[attr] = value

        children_data: dict[str, list[BaseNode]] = {}
        for node in child_nodes:
            if node.parent_attr not in children_data:
                children_data[node.parent_attr] = []
            children_data[node.parent_attr].append(node)
        return cls(**children_data, **instance_data)

    @classmethod
    def _match_structure(
        cls, py_tokens: list[tokenize.TokenInfo], exhausting: bool
    ) -> tuple[list[BaseTokenDescriptor], list[tokenize.TokenInfo], list[BaseNode]]:
        pattern_tokens: list[BaseTokenDescriptor] = []
        matched_tokens: list[tokenize.TokenInfo] = []
        child_nodes: list[BaseNode] = []
        for descriptor_structure in cls._py_structure:
            pattern_descriptor = descriptor_structure["descriptor"]
            descriptor_required = descriptor_structure["required"]
            found_token = py_tokens[0] if py_tokens else None

            # If all remaining tokens in structure are optional it's ok.
            # Otherwise structure is not matched
            if found_token is None:
                if not descriptor_required:
                    continue
                raise RuntimeError("Structure not matched")

            # Handle case when descriptor contains children
            if isinstance(pattern_descriptor, ChildrenDescriptor):
                child_nodes.extend(
                    cls._handle_children_descriptor(pattern_descriptor, py_tokens)
                )
                continue

            # Otherwise simply handle the simple descriptor
            # respecting the required property
            pattern_token, matched_token = cls._handle_token_descriptor(
                pattern_descriptor, descriptor_required, found_token, py_tokens
            )
            if pattern_token and matched_token:
                pattern_tokens.append(pattern_token)
                matched_tokens.append(matched_token)

        if exhausting and py_tokens:
            raise RuntimeError("Structure not matched")

        return pattern_tokens, matched_tokens, child_nodes

    @classmethod
    def _handle_token_descriptor(
        cls,
        pattern_descriptor: BaseTokenDescriptor,
        descriptor_required: bool,
        found_token: tokenize.TokenInfo,
        py_tokens: list[tokenize.TokenInfo],
    ) -> tuple[BaseTokenDescriptor | None, tokenize.TokenInfo | None]:
        pattern_token, matched_token = None, None
        if not descriptor_required:
            if pattern_descriptor.PY_TOKEN == found_token.exact_type:
                pattern_token = pattern_descriptor
                matched_token = found_token
                del py_tokens[0]
        elif pattern_descriptor.PY_TOKEN == found_token.exact_type:
            pattern_token = pattern_descriptor
            matched_token = found_token
            del py_tokens[0]
        elif pattern_descriptor.PY_TOKEN != found_token.exact_type:
            for descriptor in pattern_descriptor.alt:
                return cls._handle_token_descriptor(
                    descriptor, descriptor_required, found_token, py_tokens
                )
            raise RuntimeError("Structure not matched")

        return pattern_token, matched_token

    @classmethod
    def _handle_children_descriptor(
        cls, pattern_descriptor: ChildrenDescriptor, py_tokens: list[tokenize.TokenInfo]
    ) -> list[BaseNode]:
        nodes: list[BaseNode] = []
        while True:
            try:
                node = pattern_descriptor.node.match(py_tokens, exhausting=False)
                if node is None:
                    raise ValueError("child node matched structure but not value")
                node.parent_attr = pattern_descriptor.attr
                nodes.append(node)
            except RuntimeError:
                break
            found_token = py_tokens[0] if py_tokens else None
            if (
                found_token
                and pattern_descriptor.separator.PY_TOKEN == found_token.exact_type
            ):
                del py_tokens[0]

        for constraint in pattern_descriptor.constraints:
            if not constraint.validate(nodes):
                raise SyntaxError("Constraint error")
        return nodes
