from .roman import Roman

# create integer2roman then make a for loop with all possible values [1, 4000)


class TestRoman:
    roman = Roman()
    min_val = 1
    max_val = 3999

    def test_IS_VALID_ROMAN_allows_ivxlcdm(self):
        assert self.roman.is_valid_roman("MMMDCCCLXXXVIII")

    def test_IS_VALID_ROMAN_ROMAN_allows_mixed_casing(self):
        assert self.roman.is_valid_roman("MmMxXxiii")

    def test_IS_VALID_ROMAN_ROMAN_ignores_peripheral_whites(self):
        assert self.roman.is_valid_roman("\n MMMXXXIII \n")

    def test_IS_VALID_ROMAN_ROMAN_does_not_allow_middle_whites(self):
        assert not self.roman.is_valid_roman("M \n M")

    def test_IS_VALID_ROMAN_does_not_allow_empty_string(self):
        assert not self.roman.is_valid_roman("")

    def test_IS_VALID_ROMAN_vld_appear_max_once(self):
        assert self.roman.is_valid_roman("V")
        assert not self.roman.is_valid_roman("VV")
        assert self.roman.is_valid_roman("L")
        assert not self.roman.is_valid_roman("LL")
        assert self.roman.is_valid_roman("D")
        assert not self.roman.is_valid_roman("DD")

    def test_IS_VALID_ROMAN_xcm_appear_max_four_times(self):
        assert self.roman.is_valid_roman("MMMCM")
        assert not self.roman.is_valid_roman("MMMMCM")
        assert self.roman.is_valid_roman("CCCXC")
        assert not self.roman.is_valid_roman("CCCXCC")
        assert self.roman.is_valid_roman("XXXIX")
        assert not self.roman.is_valid_roman("XXIXXX")

    def test_IS_VALID_ROMAN_i_appears_max_three_times(self):
        assert self.roman.is_valid_roman("III")
        assert not self.roman.is_valid_roman("IXIII")

    def test_IS_VALID_ROMAN_first_nucleus(self):
        assert self.roman.is_valid_roman("CCC")
        assert self.roman.is_valid_roman("MCCC")
        assert self.roman.is_valid_roman("MMCCC")
        assert self.roman.is_valid_roman("MMMCCC")
        assert self.roman.is_valid_roman("CM")
        assert not self.roman.is_valid_roman("CCM")

    def test_INTEGER2ROMAN_min_max_val(self):
        assert self.roman.integer2roman(self.min_val) == "I"
        assert self.roman.integer2roman(self.max_val) == "MMMCMXCIX"

    def test_INTEGER2ROMAN_out_of_min_max_val(self):
        below_min = 0
        above_max = 4000
        assert self.roman.integer2roman(below_min) == None
        assert self.roman.integer2roman(below_min) == None

    def test_INTEGER2ROMAN_ivxlcdm(self):
        assert self.roman.integer2roman(1) == "I"
        assert self.roman.integer2roman(5) == "V"
        assert self.roman.integer2roman(10) == "X"
        assert self.roman.integer2roman(50) == "L"
        assert self.roman.integer2roman(100) == "C"
        assert self.roman.integer2roman(500) == "D"
        assert self.roman.integer2roman(1000) == "M"

    def test_ROMAN2INTEGER_all_cases(self):
        for i in range(self.min_val, self.max_val + 1):
            roman = self.roman.integer2roman(i)
            print("Roman: " + roman)
            actual = self.roman.roman2integer(roman)
            print("Actual: " + str(actual))
            assert actual == i
