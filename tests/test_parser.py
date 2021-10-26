from typing import cast

import pytest

from balami import Balami
from balami.nodes import ImportNode


@pytest.fixture(scope="session")
def parser() -> Balami:
    return Balami()


def test_parse_empty_string(parser: Balami):
    assert parser.parse_str("") == []


@pytest.mark.parametrize("data", [13, True, 3.14])
def test_parse_invalid_data_type(parser: Balami, data: int | bool | float):
    with pytest.raises(TypeError):
        parser.parse_str(data)  # type: ignore


def test_parse_simple_module_import(parser: Balami):
    nodes = parser.parse_str("import foo")
    assert len(nodes) == 1
    import_node = cast(ImportNode, nodes[0])
    assert len(import_node.modules) == 1
    assert import_node.modules[0].module == "foo"
    assert import_node.modules[0]._as is None  # type: ignore
    assert import_node.modules[0].alias is None
