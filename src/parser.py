from abc import ABC, abstractmethod
from .constants import I, V, X, L, C, D, M


class Parser(ABC):
    @abstractmethod
    def automaton(self, string: str) -> str | None:
        pass

    def automaton_complex(
        self,
        string: str,
        initial_cyclic_char: chr,
        initial_non_cyclic_char: chr,
        initial_invalid_chars: list[chr],
        previous_nucleus_char: chr,
        max_cycle: int,
    ) -> str | None:
        length = len(string)

        if self.is_empty(string):
            nucleus = ""
        elif string[0] == initial_cyclic_char:
            if 1 < length and string[1] == previous_nucleus_char:
                nucleus = initial_cyclic_char + previous_nucleus_char
            elif 1 < length and string[1] == initial_non_cyclic_char:
                nucleus = initial_cyclic_char + initial_non_cyclic_char
            else:
                nucleus = self.__automaton_simple_cycle_aux(
                    string, length, initial_cyclic_char, max_cycle
                )
        elif string[0] == initial_non_cyclic_char:
            nucleus = initial_non_cyclic_char + self.__automaton_simple_cycle_aux(
                string[1:], length - 1, initial_cyclic_char, max_cycle
            )
        elif string[0] in initial_invalid_chars:
            nucleus = None
        else:
            nucleus = ""
        return nucleus

    def automaton_simple_cycle(self, string: str, char: chr, max_count: int) -> str:
        length = len(string)
        count = 0

        if self.is_empty(string):
            return ""

        while count < length and string[count] == char:
            count += 1
            if count == max_count:
                break
        return count * char

    def is_empty(self, string: str) -> bool:
        return string == ""

    def parse(self, string: str) -> tuple[str | None, str]:
        nucleus = self.automaton(string)
        if nucleus == None:
            return nucleus, ""
        return nucleus, self.remove_nucleus(string, nucleus)

    def remove_nucleus(self, string: str, nucleus: str) -> str:
        return string[len(nucleus) :]

    def __automaton_simple_cycle_aux(
        self, string: str, length: int, char: chr, max_count: int
    ) -> str:
        count = 0
        while count < length and string[count] == char:
            count += 1
            if count == max_count:
                break
        return count * char


class ParserM(Parser):
    def automaton(self, string: str) -> str | None:
        return self.automaton_simple_cycle(string, M, 3)


class ParserC(Parser):
    def automaton(self, string: str) -> str | None:
        return self.automaton_complex(string, C, D, [M], M, 3)


class ParserX(Parser):
    def automaton(self, string: str) -> str | None:
        return self.automaton_complex(string, X, L, [M, D, C], C, 3)


class ParserI(Parser):
    def automaton(self, string: str) -> str | None:
        return self.automaton_complex(string, I, V, [M, D, C, L, X], X, 3)
