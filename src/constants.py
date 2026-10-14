I = "I"
V = "V"
X = "X"
L = "L"
C = "C"
D = "D"
M = "M"
VALUE = "val"
FREQUENCY_MAX = "f_max"
INTEGER_MAX = 3999
INTEGER_MIN = 1

ROMAN_DICT = {
    I: {VALUE: 1, FREQUENCY_MAX: 3},
    V: {VALUE: 5, FREQUENCY_MAX: 1},
    X: {VALUE: 10, FREQUENCY_MAX: 4},
    L: {VALUE: 50, FREQUENCY_MAX: 1},
    C: {VALUE: 100, FREQUENCY_MAX: 4},
    D: {VALUE: 500, FREQUENCY_MAX: 1},
    M: {VALUE: 1000, FREQUENCY_MAX: 4},
}
ALLOWED_CHARS = ROMAN_DICT.keys()

NUCLEUS_2_VALUE_M_DICT = {"": 0, M: 1000, 2 * M: 2000, 3 * M: 3000}
VALUE_2_NUCLEUS_M_DICT = {0: "", 1: M, 2: 2 * M, 3: 3 * M}


def n2v_m(nucleus: str) -> int:
    return NUCLEUS_2_VALUE_M_DICT[nucleus]


def v2n_m(integer: int) -> str:
    return VALUE_2_NUCLEUS_M_DICT[integer // 1000]


NUCLEUS_2_VALUE_C_DICT = {
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
VALUE_2_NUCLEUS_C_DICT = {
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


def n2v_c(nucleus: str) -> int:
    return NUCLEUS_2_VALUE_C_DICT[nucleus]


def v2n_c(integer: int) -> str:
    return VALUE_2_NUCLEUS_C_DICT[integer % 1000 - integer % 100]


NUCLEUS_2_VALUE_X_DICT = {
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
VALUE_2_NUCLEUS_X_DICT = {
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


def n2v_x(nucleus: str) -> int:
    return NUCLEUS_2_VALUE_X_DICT[nucleus]


def v2n_x(integer: int) -> str:
    return VALUE_2_NUCLEUS_X_DICT[integer % 100 - integer % 10]


NUCLEUS_2_VALUE_I_DICT = {
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
VALUE_2_NUCLEUS_I_DICT = {
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


def n2v_i(nucleus: str) -> int:
    return NUCLEUS_2_VALUE_I_DICT[nucleus]


def v2n_i(integer: int) -> str:
    return VALUE_2_NUCLEUS_I_DICT[integer % 10]
