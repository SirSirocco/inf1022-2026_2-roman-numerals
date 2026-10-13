from abc import ABC, abstractmethod

I = "I"
V = "V"
X = "X"
L = "L"
C = "C"
D = "D"
M = "M"
VAL = "val"
F_MAX = "f_max"

ROMAN_DICT = {
    I: {VAL: 1, F_MAX: 3},
    V: {VAL: 5, F_MAX: 1},
    X: {VAL: 10, F_MAX: 4},
    L: {VAL: 50, F_MAX: 1},
    C: {VAL: 100, F_MAX: 4},
    D: {VAL: 500, F_MAX: 1},
    M: {VAL: 1000, F_MAX: 4},
}

M_DICT = {0: "", 1: M, 2: 2 * M, 3: 3 * M}

M_NUCLEUS_DICT = {"": 0, M: 1000, 2 * M: 2000, 3 * M: 3000}

C_DICT = {
    0: "",
    100: C,
    200: 2 * C,
    300: 3 * C,
    400: C + D,
    500: D,
    600: D + C,
    700: D + 2 * C,
    800: D + 3 * C,
    900: C + M,
}

C_NUCLEUS_DICT = {
    "": 0,
    C: 100,
    2 * C: 200,
    3 * C: 300,
    C + D: 400,
    D: 500,
    D + C: 600,
    D + 2 * C: 700,
    D + 3 * C: 800,
    C + M: 900,
}

X_DICT = {
    0: "",
    10: X,
    20: 2 * X,
    30: 3 * X,
    40: X + L,
    50: L,
    60: L + X,
    70: L + 2 * X,
    80: L + 3 * X,
    90: X + C,
}

X_NUCLEUS_DICT = {
    "": 0,
    X: 10,
    2 * X: 20,
    3 * X: 30,
    X + L: 40,
    L: 50,
    L + X: 60,
    L + 2 * X: 70,
    L + 3 * X: 80,
    X + C: 90,
}

I_DICT = {
    0: "",
    1: I,
    2: 2 * I,
    3: 3 * I,
    4: I + V,
    5: V,
    6: V + I,
    7: V + 2 * I,
    8: V + 3 * I,
    9: I + X,
}

I_NUCLEUS_DICT = {
    "": 0,
    I: 1,
    2 * I: 2,
    3 * I: 3,
    I + V: 4,
    V: 5,
    V + I: 6,
    V + 2 * I: 7,
    V + 3 * I: 8,
    I + X: 9,
}


class Roman:
    def __init__(self):
        self.__DICT = ROMAN_DICT
        self.__ALLOWED_CHARS = self.__DICT.keys()
        self.__FREQUENCY = {key: 0 for key in self.__ALLOWED_CHARS}
        self.__INTEGER_INVALID = None
        self.__INTEGER_MAX = 3999
        self.__INTEGER_MIN = 1
        self.__ROMAN_INVALID = None
        self.__parserM = ParserM()
        self.__parserC = ParserC()
        self.__parserX = ParserX()
        self.__parserI = ParserI()
        self.__deparsers = [
            self.__get_nucleus_m,
            self.__get_nucleus_c,
            self.__get_nucleus_x,
            self.__get_nucleus_i,
        ]
        self.__inverse_deparsers = [
            M_NUCLEUS_DICT,
            C_NUCLEUS_DICT,
            X_NUCLEUS_DICT,
            I_NUCLEUS_DICT,
        ]

    def is_valid_roman(self, roman: str) -> bool:
        normalized = roman.strip().upper()
        is_valid, nucleuses = self.__lexical_analysis(normalized)
        return is_valid

    def is_valid_integer(self, integer: str) -> bool:
        return self.__INTEGER_MIN <= integer <= self.__INTEGER_MAX

    def integer2roman(self, integer: int) -> str | None:
        if not self.is_valid_integer(integer):
            return self.__INTEGER_INVALID
        roman = ""

        for deparser in self.__deparsers:
            roman += deparser(integer)

        return roman

    def roman2integer(self, string: str) -> int | None:
        is_valid, nucleuses = self.__lexical_analysis(string)
        if not is_valid:
            return self.__ROMAN_INVALID
        integer = 0
        for i, deparser in enumerate(self.__inverse_deparsers):
            integer += deparser[nucleuses[i]]
        return integer

    def __get_nucleus_m(self, integer: int) -> str:
        return M_DICT[integer // 1000]

    def __get_nucleus_c(self, integer: int) -> str:
        return C_DICT[integer % 1000 - integer % 100]

    def __get_nucleus_x(self, integer: int) -> str:
        return X_DICT[integer % 100 - integer % 10]

    def __get_nucleus_i(self, integer: int) -> str:
        return I_DICT[integer % 10]

    def __is_empty(self, normalized: str) -> bool:
        return len(normalized) == 0

    def __is_allowed_char(self, char: chr) -> bool:
        return char in self.__ALLOWED_CHARS

    def __is_allowed_frequency(self, char: chr) -> bool:
        return self.__FREQUENCY[char] <= self.__DICT[char][F_MAX]

    def __refresh_frequency(self) -> None:
        for key in self.__FREQUENCY.keys():
            self.__FREQUENCY[key] = 0

    def __update_frequency(self, char: chr) -> None:
        self.__FREQUENCY[char] += 1

    def __lexical_analysis(
        self, normalized: str
    ) -> tuple[bool, list[str | None] | None]:
        if self.__is_empty(normalized):
            return False, None

        self.__refresh_frequency()

        for char in normalized:
            if not self.__is_allowed_char(char):
                return False, None

            self.__update_frequency(char)
            if not self.__is_allowed_frequency(char):
                return False, None

        nucleus_m, remainder_m = self.__parserM.parse(normalized)
        nucleus_c, remainder_c = self.__parserC.parse(remainder_m)
        nucleus_x, remainder_x = self.__parserX.parse(remainder_c)
        nucleus_i, remainder_i = self.__parserI.parse(remainder_x)
        nucleuses = [
            nucleus_m,
            nucleus_c,
            nucleus_x,
            nucleus_i,
        ]

        if not self.__is_empty(remainder_i) or None in nucleuses:
            return False, nucleuses

        return True, nucleuses


class Parser(ABC):
    def remove_nucleus(self, string: str, nucleus: str) -> str:
        return string[len(nucleus) :]

    def is_empty(self, string: str) -> bool:
        return string == ""

    @abstractmethod
    def parse(self, string: str) -> str | None:
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
