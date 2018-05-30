import argparse

from pycalc.calc_function import calc
from pycalc.parse_epression import list_module, operators, static_value, parse_expression, list_functions
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
    """
    Function of testing the program
    :param expression: Expression for testing
    :return: result of expression
    """
    exp = parse_expression(expression)
    exp = poland_notation(exp)
    exp = calc(exp)
    return exp


if __name__ == '__main__':
    EXPRESSION = parse_expression(args.EXPRESSION)
    EXPRESSION = poland_notation(EXPRESSION)
    EXPRESSION = calc(EXPRESSION)
    print(EXPRESSION)
