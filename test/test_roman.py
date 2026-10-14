from src.roman import Roman


class TestRoman:
    roman = Roman()
    min_val = 1
    max_val = 3999

    def test_INTEGER_2_ROMAN_converts_each_char_in_ivxlcdm(self):
        assert self.roman.integer2roman(1) == "I"
        assert self.roman.integer2roman(5) == "V"
        assert self.roman.integer2roman(10) == "X"
        assert self.roman.integer2roman(50) == "L"
        assert self.roman.integer2roman(100) == "C"
        assert self.roman.integer2roman(500) == "D"
        assert self.roman.integer2roman(1000) == "M"

    def test_INTEGER_2_ROMAN_converts_min_and_max_vals(self):
        assert self.roman.integer2roman(self.min_val) == "I"
        assert self.roman.integer2roman(self.max_val) == "MMMCMXCIX"

    def test_INTEGER_2_ROMAN_rejects_vals_out_of_min_and_max(self):
        below_min = 0
        above_max = 4000
        assert self.roman.integer2roman(below_min) == None
        assert self.roman.integer2roman(above_max) == None

    def test_IS_VALID_ROMAN_allows_max_four_times_xcm(self):
        assert self.roman.is_valid_roman("MMMCM")
        assert not self.roman.is_valid_roman("MMMMCM")
        assert self.roman.is_valid_roman("CCCXC")
        assert not self.roman.is_valid_roman("CCCXCC")
        assert self.roman.is_valid_roman("XXXIX")
        assert not self.roman.is_valid_roman("XXIXXX")

    def test_IS_VALID_ROMAN_allows_max_once_vld(self):
        assert self.roman.is_valid_roman("V")
        assert not self.roman.is_valid_roman("VV")
        assert self.roman.is_valid_roman("L")
        assert not self.roman.is_valid_roman("LL")
        assert self.roman.is_valid_roman("D")
        assert not self.roman.is_valid_roman("DD")

    def test_IS_VALID_ROMAN_allows_max_three_times_i(self):
        assert self.roman.is_valid_roman("III")
        assert not self.roman.is_valid_roman("IXIII")

    def test_IS_VALID_ROMAN_allows_mixed_casing(self):
        assert self.roman.is_valid_roman("MmMxXxiii")

    def test_IS_VALID_ROMAN_allows_only_ivxlcdm(self):
        assert self.roman.is_valid_roman("MMMDCCCLXXXVIII")
        assert not self.roman.is_valid_roman("ABCDEFGH")

    def test_IS_VALID_ROMAN_ignores_lateral_whitespaces(self):
        assert self.roman.is_valid_roman("\n MMMXXXIII \n")

    def test_IS_VALID_ROMAN_rejects_empty_string(self):
        assert not self.roman.is_valid_roman("")

    def test_IS_VALID_ROMAN_rejects_middle_whitespaces(self):
        assert not self.roman.is_valid_roman("M \n M")

    def test_ROMAN_2_INTEGER_converts_all_possible_cases(self):
        for integer in range(self.min_val, self.max_val + 1):
            roman = self.roman.integer2roman(integer)
            actual = self.roman.roman2integer(roman)
            assert actual == integer
