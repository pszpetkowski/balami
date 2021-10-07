import tokenize

from balami.base import BaseTokenDescriptor


class NameTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.NAME

    def match_token(self, py_token: tokenize.TokenInfo) -> str | None:
        actual_value = py_token.string
        if self._typ:
            return actual_value
        elif self._value == actual_value:
            return actual_value
        else:
            return None


class OpTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.OP

    def match_token(self, py_token: tokenize.TokenInfo) -> str | None:
        actual_value = py_token.string
        if self._typ:
            return actual_value
        elif self._value == actual_value:
            return actual_value
        else:
            return None


class CommaTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.COMMA


class LParTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.LPAR


class RParTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.RPAR


class StarTokenDescriptor(BaseTokenDescriptor):
    PY_TOKEN = tokenize.STAR
