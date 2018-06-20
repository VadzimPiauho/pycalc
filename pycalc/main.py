#!/usr/bin/env python3
import argparse

from pycalc.calc_function import calc
from pycalc.exception import MyException
from pycalc.import_module import imp_module
from pycalc.parse_epression import parse_expression, list_module
from pycalc.poland_notation_function import poland_notation


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
    Function of expression calculation
    :param expression: entrance expression
    :return: counting result
    """

    exception = parse_expression(expression)
    return calc(poland_notation(exception))


def _main():
    """
    Main Function
    """
    try:
        args = _parse_args()
        if args.MODULE:
            list_module.extend(args.MODULE)
        imp_module()
        print(main(args.EXPRESSION))
    except (MyException, ImportError) as e:
        print(e.message)
    except Exception as e:
        raise MyException("{}".format(e))


if __name__ == '__main__':
    _main()
