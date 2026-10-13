from abc import ABC, abstractmethod
from .constants import *


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


class Parser(ABC):
    def remove_nucleus(self, string: str, nucleus: str) -> str:
        return string[len(nucleus) :]

    def is_empty(self, string: str) -> bool:
        return string == ""

    @abstractmethod
    def parse(self, string: str) -> tuple[str | None, str]:
        pass


class ParserM(Parser):
    def parse(self, string: str) -> tuple[str | None, str]:
        if self.is_empty(string):
            return "", ""

        length = len(string)
        m_counter = 0

        while m_counter < length and string[m_counter] == M:
            m_counter += 1
            if m_counter == 3:  # Stack automaton
                break
        nucleus = m_counter * M

        return nucleus, self.remove_nucleus(string, nucleus)


class ParserC(Parser):
    def parse(self, string: str) -> tuple[str | None, str]:
        if self.is_empty(string):
            return "", ""

        length = len(string)
        c_counter = 0

        if string[0] == C:
            c_counter += 1
            if length > 1 and string[1] == M:
                nucleus = C + M
            elif length > 1 and string[1] == D:
                nucleus = C + D
            else:
                while c_counter < length and string[c_counter] == C:
                    c_counter += 1
                    if c_counter == 3:
                        break
                nucleus = c_counter * C

        elif string[0] == D:
            while c_counter + 1 < length and string[c_counter + 1] == C:
                c_counter += 1
                if c_counter == 3:
                    break
            nucleus = D + c_counter * C

        elif string[0] == M:
            return None, ""

        else:
            nucleus = ""

        return nucleus, self.remove_nucleus(string, nucleus)


class ParserX(Parser):
    def parse(self, string: str) -> tuple[str | None, str]:
        if self.is_empty(string):
            return "", ""

        length = len(string)
        x_counter = 0

        if string[0] == X:
            x_counter += 1
            if length > 1 and string[1] == C:
                nucleus = X + C
            elif length > 1 and string[1] == L:
                nucleus = X + L
            else:
                while x_counter < length and string[x_counter] == X:
                    x_counter += 1
                    if x_counter == 3:
                        break
                nucleus = x_counter * X

        elif string[0] == L:
            while x_counter + 1 < length and string[x_counter + 1] == X:
                x_counter += 1
                if x_counter == 3:
                    break
            nucleus = L + x_counter * X

        elif string[0] in [M, D, C]:
            return None, ""

        else:
            nucleus = ""

        return nucleus, self.remove_nucleus(string, nucleus)


class ParserI(Parser):
    def parse(self, string: str) -> tuple[str | None, str]:
        if self.is_empty(string):
            return "", ""

        length = len(string)
        i_counter = 0

        if string[0] == I:
            i_counter += 1
            if length > 1 and string[1] == X:
                nucleus = I + X
            elif length > 1 and string[1] == V:
                nucleus = I + V
            else:
                while i_counter < length and string[i_counter] == I:
                    i_counter += 1
                    if i_counter == 3:
                        break
                nucleus = i_counter * I

        elif string[0] == V:
            while i_counter + 1 < length and string[i_counter + 1] == I:
                i_counter += 1
                if i_counter == 3:
                    break
            nucleus = V + i_counter * I

        elif string[0] in [M, D, C, L, X]:
            return None, ""

        else:
            nucleus = ""

        return nucleus, self.remove_nucleus(string, nucleus)
