# python -m unittest tests.py

# pip install coverage
# coverage run -m unittest tests.py
# coverage report
# coverage html


import unittest
from main import test


class CalcTest(unittest.TestCase):
    def test_unary(self):
        # Unary operators
        test_list = [
            ("-13", -13),
            ("6-(-13)", 19),
            ("1-- -1", 0),
            ("1---1", 0),
            ("1 -  1", 0),
            ("-+---+-1", -1), ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_operation(self):
        # Operation priority
        test_list = [
            ("1+2*2", 5),
            ("1+(2+32)3", 103),
            ("10*(2+1)", 30),
            ("10^(2+1)", 1000),
            ("100/3^2", 11.11111111111111),
            ("100/3%2^2", 1.3333333333333357),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_functions(self):
        # Functions and constants
        test_list = [
            ("pi+e", 5.859874482048838),
            ("log(e)", 1.0),
            ("sin(pi/2)", 1.0),
            ("log10(100)", 2.0),
            ("sin(pi/2)1116", 1116.0),
            ("2*sin(pi/2)", 2.0),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_associative(self):
        # Associative
        test_list = [
            ("102%12%7", 6),
            ("100/4/3", 8.333333333333334),
            ("2^3^4", 2417851639229258349412352),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_comparison(self):
        # Comparison operators
        test_list = [
            ("1+23==1+23", True),
            ("e^5>=e^5+1", False),
            ("1+24/3+1!=1+24/3+2", True),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_common(self):
        # Common tests
        test_list = [
            ("(100)", 100),
            ("666", 666),
            ("10(2+1)", 30),
            ("(2+1)10+1", 31),
            ("(2+1)10", 30),
            ("-.1", -0.1),
            ("1/3", 0.3333333333333333),
            ("1.0/3.0", 0.3333333333333333),
            (".1*2.0^56.0", 7205759403792794.0),
            ("e^34", 583461742527453.9),
            ("(2.0^(pi/pi+e/e+2.0^0.0))", 8.0),
            ("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)", 2.0),
            ("sin(pi/2^1) + log(1*4+2^2+1, 3^2)", 2.0),
            ("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53/10) + -5", 10.3),
            ("log10(.4* -5/ -0.1-10)", 1.0),
            ("- -abs(-53/10) + -5", 0.2999999999999998),
            ("- -abs(-53/10)", 5.3),
            ("2*-1", -2),
            ("10*e^0", 10.0),
            ("2.0^(2.0^2.0*2.0^2.0)", 65536.0),
            ("(2.0^2.0*2.0^2.0)", 16),
            ("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))", 0.76638122986603),
            ("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))) \
            --cos(1.0)--cos(0.0)^3.0)", 0.5361064001012783),
            ("--cos(1.0)--cos(0.0)^3.0", 1.5403023058681398),
            ("cos(sin(sin(34.0-2.0^2.0)))", 0.6712189482597033),
            ("-sin(cos(log10(43.0)))", 0.06259017093637237),
            ("-cos(-sin(-3.0*5.0))", -0.7959095686227995),
            ("-cos(-sin(3.0))", -0.9900590857598653),
            ("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0))))", -0.5581746423992129),
            ("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))))",
             -0.8274124603473457),
            ("cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))", 1.4277017012821114),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_my(self):
        # My cases
        test_list = [
            ("2+ +2", 4),
            ("2>=2", True),
            ("2  < + 2", False),
            ("2  < ++ ++ 2", False),
            ("-2", -2),
            ("3-2", 1),
            ("(-3)", -3),
            ("((-4))", -4),
            ("-((5))", -5),
            ("(-(6))", -6),
            ("-2+1+1", 0),
            ("-2-1", -3),
            ("-2*1", -2),
            ("2*-1", -2),
            ("5^-1", 0.2),
            ("5^-1-1", -0.8),
            ("5^-1*2", 0.4),
            ("-53/10", -5.3),
            ("+abs(-53/10)", 5.3),
            ("-(2)+1+1", 0),
            ("(-2)+1+1", 0),
            ("-(2+1+1)", -4),
            ("3+2+2", 7),
            ("2*(1+1)", 4),
            ("pow(2,2)", 4),
            ("pow(2,pow(2,1))", 4),
            ("pow(2,-(2))", 0.25),
            ("pow(2,(-2))", 0.25),
            ("2*-2", -4),
            ("2+2*-2", -2),
            ("2^2^3", 256),
            ("2-2-3", -3),
            ("5/-1*2", -10),
            ("5/-1", -5),
            ("5^-1/2", 0.1),
            ("-5^-1-1", -1.2),
            ("5^-(1)", 0.2),
            ("5^-(.1)", 0.8513399225207846),
            ("5^-.1", 0.8513399225207846),
            ("5^(-1)", 0.2),
            ("5^(1)", 5),
            ("2/5^(-(1))", 10),
            ("2/5^(-1)", 10),
            ("--2+2++-+-2", 6),
            ("-5^2", -25),
            ("round(2*2*2+2,2)", 10),
            ("-5^-1", -0.2),
            ("2/-5^-1", -10.0),
            ("round(2^2,2)", 4),
            ("round(2^2)", 4),
            ("-(-2)", 2),
            ("round(1>=1)", 1),
            ("-(2+1+(-2))", -1),
            ("round((2/3)^213,round(1+114+332.2/4))", 3.1085783725131357e-38),
            ("round((2/3)^213,round(1+114+332.2/4))/5^-1-1", -1.0),
            ("round(1/3,2)", 0.33),
            ("sin(1/3)", 0.3271946967961522),
            ("2+sin(1/3)", 2.3271946967961523),
            ("-sin(2)^2", -0.826821810431806),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])

    def test_error(self):
        # Error cases
        test_list = [
            # ("",),
            # ("+",),
            # ("1-",),
            # ("1 2",),
            # ("ee",),
            # ("123e",),
            # ("==7",),
            # ("1 * * 2",),
            # ("1 + 2(3 * 4))",),
            # ("((1+2)",),
            # ("1 + 1 2 3 4 5 6 ",),
            # ("log100(100)",),
            # ("------",),
            # ("5 > = 6",),
            # ("5 / / 6",),
            # ("6 < = 6",),
            # ("6 * * 6",),
            # ("(((((",),
        ]
        for counter, EXPRESSION in enumerate(test_list):
            self.assertEqual(test(EXPRESSION[0]), EXPRESSION[1])


if __name__ == '__main__':
    unittest.main()
