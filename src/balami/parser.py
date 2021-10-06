import tokenize
from io import StringIO

from balami.base import NODE_REGISTRY, BaseNode


class Parser:
    def __init__(self) -> None:
        self._cached_lines: dict[str, BaseNode] = {}

    def run(self, s: str) -> list[BaseNode]:
        tokens = tokenize.generate_tokens(StringIO(s).readline)
        nodes: list[BaseNode] = []
        node_tokens: list[tokenize.TokenInfo] = []
        while (token := next(tokens)).type != tokenize.ENDMARKER:
            if token.type in (tokenize.NL, tokenize.INDENT):
                # TODO: Add support
                continue

            if token.type == tokenize.NEWLINE and node_tokens:
                token_line_hash = self._get_token_line_key(node_tokens)
                node = self._cached_lines.get(token_line_hash)
                if node:
                    nodes.append(node)
                    node_tokens = []
                    continue

                for node_cls in NODE_REGISTRY:
                    try:
                        node = node_cls.match(node_tokens.copy())
                    except (RuntimeError, ValueError):
                        node = None
                    if node:
                        self._cached_lines[token_line_hash] = node
                        nodes.append(node)
                        node_tokens = []
                        break
                else:
                    raise RuntimeError("Could not parse")

            if token.type != tokenize.NEWLINE:
                node_tokens.append(token)

        return nodes

    def _get_token_line_key(self, tokens: list[tokenize.TokenInfo]) -> str:
        cache_string = ""
        for token in tokens:
            cache_string += f"{token.type}{token.string}"

        return cache_string
