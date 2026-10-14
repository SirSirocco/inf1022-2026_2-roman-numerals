from .constants import *
from .parser import ParserM, ParserC, ParserX, ParserI


class Roman:
    def __init__(self):
        self.__INTEGER_INVALID = None
        self.__ROMAN_INVALID = None
        self.__parsers = [ParserM(), ParserC(), ParserX(), ParserI()]
        self.__value2nucleus = [v2n_m, v2n_c, v2n_x, v2n_i]
        self.__nucleus2value = [n2v_m, n2v_c, n2v_x, n2v_i]

    def is_valid_integer(self, integer: int) -> bool:
        return INTEGER_MIN <= integer <= INTEGER_MAX

    def is_valid_roman(self, roman: str) -> bool:
        normalized = roman.strip().upper()
        is_valid, _ = self.__lexical_analysis(normalized)
        return is_valid

    def integer2roman(self, integer: int) -> str | None:
        if not self.is_valid_integer(integer):
            return self.__INTEGER_INVALID
        roman = ""
        for map in self.__value2nucleus:
            roman += map(integer)
        return roman

    def roman2integer(self, roman: str) -> int | None:
        is_valid, nucleuses = self.__lexical_analysis(roman)
        if not is_valid:
            return self.__ROMAN_INVALID
        integer = 0
        for map, nucleus in zip(self.__nucleus2value, nucleuses):
            integer += map(nucleus)
        return integer

    def __is_empty(self, normalized: str) -> bool:
        return len(normalized) == 0

    def __is_allowed_char(self, char: chr) -> bool:
        return char in ALLOWED_CHARS

    def __are_allowed_chars(self, normalized: str) -> bool:
        for char in normalized:
            if not self.__is_allowed_char(char):
                return False
        return True

    def __is_parseable(self, normalized: str) -> bool:
        return not self.__is_empty(normalized) and self.__are_allowed_chars(normalized)

    def __parse(self, normalized: str) -> tuple[list[str | None], str]:
        nucleuses = list()
        remainder = normalized
        for parser in self.__parsers:
            nucleus, remainder = parser.parse(remainder)
            nucleuses.append(nucleus)
        return nucleuses, remainder

    def __parsing_successful(self, nucleuses: list[str | None], remainder: str) -> bool:
        return self.__is_empty(remainder) and None not in nucleuses

    def __lexical_analysis(
        self, normalized: str
    ) -> tuple[bool, None | list[str | None]]:
        if not self.__is_parseable(normalized):
            return False, None
        nucleuses, remainder = self.__parse(normalized)
        return self.__parsing_successful(nucleuses, remainder), nucleuses
