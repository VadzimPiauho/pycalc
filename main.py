import argparse

from pycalc.calc_function import calc
from pycalc.parse_epression import list_module, operators, static_value, replace_plus_minus, parse_expression, \
    list_functions
from pycalc.poland_notation_function import poland_notation

parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

parser.add_argument('EXPRESSION', action="store", type=str, help="expression string to evaluate")
parser.add_argument('-m', '--use-modules', nargs='+', action="store", dest="MODULE", type=str,
                    help="additional modules to use")

args = parser.parse_args()

if args.MODULE:
    list_module = ["math"] + args.MODULE

for modname in list_module:
    modules = __import__(modname)
    for key in modules.__dict__:
        if callable(modules.__dict__[key]):
            operators[key] = (7, getattr(modules, key))
            list_functions.append(key)
        else:
            static_value[key] = getattr(modules, key)


def test(expression):
    exp = expression.replace(" ", "")
    # print(exp)
    exp = replace_plus_minus(exp)
    # print(exp)
    exp = parse_expression(exp)
    # print(exp)
    exp = poland_notation(exp)
    # print(exp)
    exp = calc(exp)
    # print(exp)
    # print("===================================")
    return exp


if __name__ == '__main__':
    EXPRESSION = args.EXPRESSION.replace(" ", "")
    EXPRESSION = replace_plus_minus(EXPRESSION)
    EXPRESSION = parse_expression(EXPRESSION)
    # print(EXPRESSION)
    EXPRESSION = poland_notation(EXPRESSION)
    # print(EXPRESSION)
    EXPRESSION = calc(EXPRESSION)
    print(EXPRESSION)
