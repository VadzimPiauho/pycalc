import argparse

from import_module import imp_module
from pycalc.calc_function import calc
from pycalc.parse_epression import parse_expression, list_module
from pycalc.poland_notation_function import poland_notation
from exception import MyException


def _parse_args():
    """
    Function of parsing arguments
    """
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

    parser.add_argument('EXPRESSION', action="store", type=str, help="expression string to evaluate")
    parser.add_argument('-m', '--use-modules', nargs='+', action="store", dest="MODULE", type=str,
                        help="additional modules to use")

    return parser.parse_args()


def main(expression):
    """
    Function of converting an expression to a reverse polish notation
    :param expression: entrance expression
    :return: counting result
    """
    try:
        exception = parse_expression(expression)
        return calc(poland_notation(exception))
    except (MyException, ImportError) as e:
        raise MyException("{}".format(e))
    except Exception as e:
        raise MyException("{}".format(e))


def _main():
    args = _parse_args()
    if args.MODULE:
        list_module.extend(args.MODULE)
    imp_module()
    print(main(args.EXPRESSION))


if __name__ == '__main__':
    _main()
