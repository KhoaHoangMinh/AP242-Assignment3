import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_7(self):
        input = ["INSERT x number"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, 107))

    def test_8(self):
        input = ["INSERT x string", "INSERT x number"]
        expected = ["Redeclared: INSERT x number"]
        self.assertTrue(TestUtils.check(input, expected, 108))

    def test_9(self):
        input = ["INSERT y number", "ASSIGN y 42"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 109))

    def test_10(self):
        input = ["INSERT y string", "ASSIGN y 42"]
        expected = ["TypeMismatch: ASSIGN y 42"]
        self.assertTrue(TestUtils.check(input, expected, 110))

    def test_11(self):
        input = ["INSERT _x number"]
        expected = ["Invalid: INSERT _x number"]
        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_12(self):
        input = ["INSERT z number", "ASSIGN z 'str'"]
        expected = ["TypeMismatch: ASSIGN z 'str'"]
        self.assertTrue(TestUtils.check(input, expected, 112))

    def test_13(self):
        input = ["INSERT z string", "ASSIGN z 'str'"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = ["INSERT z string", "ASSIGN z 123"]
        expected = ["TypeMismatch: ASSIGN z 123"]
        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = ["INSERT x number", "ASSIGN y 1"]
        expected = ["Undeclared: ASSIGN y 1"]
        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = ["ASSIGN x 1"]
        expected = ["Undeclared: ASSIGN x 1"]
        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = ["INSERT x number", "BEGIN", "INSERT x string"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "ASSIGN x 5"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = ["INSERT x number", "BEGIN", "INSERT x string", "ASSIGN x 5"]
        expected = ["TypeMismatch: ASSIGN x 5"]
        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = ["INSERT x number", "BEGIN", "INSERT x string", "ASSIGN x 'hi'"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = ["INSERT x number", "LOOKUP y"]
        expected = ["Undeclared: LOOKUP y"]
        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = ["LOOKUP x"]
        expected = ["Undeclared: LOOKUP x"]
        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_23(self):
        input = ["INSERT x number", "PRINT"]
        expected = ["success", "x//0"]
        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_24(self):
        input = ["INSERT x number", "INSERT y string", "PRINT"]
        expected = ["success", "success", "x//0 y//0"]
        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_25(self):
        input = ["INSERT x number", "INSERT y string", "RPRINT"]
        expected = ["success", "success", "y//0 x//0"]
        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_26(self):
        input = ["INSERT x number", "BEGIN", "INSERT y string", "PRINT"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = ["INSERT x number", "BEGIN", "INSERT y string", "RPRINT"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 127))

    def test_28(self):
        input = ["BEGIN", "END"]
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = ["END"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = ["BEGIN"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = ["BEGIN", "BEGIN"]
        expected = ["UnclosedBlock: 2"]
        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = ["BEGIN", "END", "END"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = ["INSERT x number", "ASSIGN x 1", "ASSIGN x 2"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = ["INSERT x string", "ASSIGN x 'a'", "ASSIGN x 'b'"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = ["INSERT x number", "ASSIGN x 1", "ASSIGN x 'b'"]
        expected = ["TypeMismatch: ASSIGN x 'b'"]
        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = ["INSERT x string", "ASSIGN x 'a'", "ASSIGN x 2"]
        expected = ["TypeMismatch: ASSIGN x 2"]
        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = ["INSERT x number", "INSERT y number", "ASSIGN x y"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = ["INSERT x string", "INSERT y string", "ASSIGN x y"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 138))

    def test_39(self):
        input = ["INSERT x number", "INSERT y string", "ASSIGN x y"]
        expected = ["TypeMismatch: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = ["INSERT x string", "INSERT y number", "ASSIGN x y"]
        expected = ["TypeMismatch: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = ["INSERT x number", "ASSIGN x y"]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = ["INSERT x string", "ASSIGN x y"]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = ["INSERT x number", "INSERT y number", "ASSIGN y x"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = ["INSERT x string", "INSERT y string", "ASSIGN y x"]
        expected = ["success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = ["INSERT x number", "INSERT y string", "ASSIGN y x"]
        expected = ["TypeMismatch: ASSIGN y x"]
        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = ["INSERT x string", "INSERT y number", "ASSIGN y x"]
        expected = ["TypeMismatch: ASSIGN y x"]
        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = ["INSERT x number", "INSERT y number", "ASSIGN z x"]
        expected = ["Undeclared: ASSIGN z x"]
        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = ["INSERT x string", "INSERT y string", "ASSIGN z x"]
        expected = ["Undeclared: ASSIGN z x"]
        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = ["INSERT x number", "INSERT y string", "ASSIGN z x"]
        expected = ["Undeclared: ASSIGN z x"]
        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_50(self):
        input = ["INSERT x string", "INSERT y number", "ASSIGN z x"]
        expected = ["Undeclared: ASSIGN z x"]
        self.assertTrue(TestUtils.check(input, expected, 150))
