import argparse
from pycalc.parse_epression import list_module, operators, static_value, replace_plus_minus, parse_expression
from pycalc.poland_notation_function import poland_notation
from pycalc.calc_function import calc

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
        else:
            static_value[key] = getattr(modules, key)


EXPRESSION = args.EXPRESSION.replace(" ", "")
EXPRESSION = replace_plus_minus(EXPRESSION)
EXPRESSION = parse_expression(EXPRESSION)
print(EXPRESSION)
EXPRESSION = poland_notation(EXPRESSION)
print(EXPRESSION)
EXPRESSION = calc(EXPRESSION)
print(EXPRESSION)


