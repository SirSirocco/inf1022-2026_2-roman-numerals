from .roman import Roman

# create integer2roman then make a for loop with all possible values [1, 4000)

class TestRoman:
    roman = Roman()

    def test_IS_VALID_allows_ivxlcdm(self):
        assert self.roman.is_valid("MMMDCCCLXXXVIII")

    def test_IS_VALID_allows_mixed_casing(self):
        assert self.roman.is_valid("MmMxXxiii")

    def test_IS_VALID_ignores_peripheral_whites(self):
        assert self.roman.is_valid("\n MMMXXXIII \n")

    def test_IS_VALID_does_not_allow_middle_whites(self):
        assert not self.roman.is_valid("M \n M")

    def test_IS_VALID_does_not_allow_empty_string(self):
        assert not self.roman.is_valid("")

    def test_IS_VALID_vld_appear_max_once(self):
        assert self.roman.is_valid("V")
        assert not self.roman.is_valid("VV")
        assert self.roman.is_valid("L")
        assert not self.roman.is_valid("LL")
        assert self.roman.is_valid("D")
        assert not self.roman.is_valid("DD")

    def test_IS_VALID_xcm_appear_max_four_times(self):
        assert self.roman.is_valid("MMMCM")
        assert not self.roman.is_valid("MMMMCM")
        assert self.roman.is_valid("CCCXC")
        assert not self.roman.is_valid("CCCXCC")
        assert self.roman.is_valid("XXXIX")
        assert not self.roman.is_valid("XXIXXX")

    def test_IS_VALID_i_appears_max_three_times(self):
        assert self.roman.is_valid("III")
        assert not self.roman.is_valid("IXIII")

    def test_IS_VALID_first_nucleus(self):
        assert self.roman.is_valid("CCC")
        assert self.roman.is_valid("MCCC")
        assert self.roman.is_valid("MMCCC")
        assert self.roman.is_valid("MMMCCC")
        assert self.roman.is_valid("CM")
        assert not self.roman.is_valid("CCM")
    