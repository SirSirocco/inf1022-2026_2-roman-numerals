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


class Roman:
    def __init__(self):
        self.__DICT = ROMAN_DICT
        self.__ALLOWED_CHARS = self.__DICT.keys()
        self.__FREQUENCY = {key: 0 for key in self.__ALLOWED_CHARS}
        self.__parserM = ParserM()
        self.__parserC = ParserC()
        self.__parserX = ParserX()
        self.__parserI = ParserI()

    def is_valid(self, roman: str) -> bool:
        normalized = roman.strip().upper()
        return self.__lexical_analysis(normalized)

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

    def __lexical_analysis(self, normalized: str) -> bool:
        if self.__is_empty(normalized):
            return False

        self.__refresh_frequency()

        for char in normalized:
            if not self.__is_allowed_char(char):
                return False

            self.__update_frequency(char)
            if not self.__is_allowed_frequency(char):
                return False

        nucleusM, remainderM = self.__parserM.parse(normalized)
        nucleusC, remainderC = self.__parserC.parse(remainderM)
        nucleusX, remainderX = self.__parserX.parse(remainderC)
        nucleusI, remainderI = self.__parserI.parse(remainderX)

        print(nucleusM)
        print(nucleusC)
        print(nucleusX)
        print(nucleusI)

        if not self.__is_empty(remainderI) or None in [
            nucleusM,
            nucleusC,
            nucleusX,
            nucleusI,
        ]:
            return False

        return True


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

        m_counter = 0

        while string[m_counter] == M:
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
            if length > 1 and string[1] == M:
                nucleus = C + M
            elif length > 1 and string[1] == D:
                nucleus = C + D
            else:
                while c_counter + 1 < length and string[c_counter + 1] == C:
                    c_counter += 1
                    if c_counter == 2:
                        break
                nucleus = C + c_counter * C

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
                while x_counter + 1 < length and string[x_counter + 1] == X:
                    x_counter += 1
                    if x_counter == 2:
                        break
                nucleus = X + x_counter * X

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
                while i_counter + 1 < length and string[i_counter + 1] == I:
                    i_counter += 1
                    if i_counter == 2:
                        break
                nucleus = I + i_counter * I

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
