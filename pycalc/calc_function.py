from pycalc.parse_epression import operators, list_functions
from pycalc.exception import MyException


def calc(data_out):
    """
    Function of result calculation
    :param data_out: modified expression for the reverse polish notation
    :return: counting result
    """
    stack = []
    count_list = []
    for token in data_out:
        if token in operators:  # если приходящий элемент - оператор,
            if token not in list_functions:
                try:
                    if token == "-u" or token == "+u":
                        stack.append(operators[token][1](stack.pop()))
                    elif token == "^":
                        y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                        stack.append(operators[token][1](x, y))
                    else:
                        y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                        stack.append(operators[token][1](x, y))
                except IndexError:
                    raise MyException("Error calculation")
            else:
                while stack:
                    x = stack.pop()
                    if x == "]" or x == ",":
                        continue
                    elif x == "[":
                        count_list.reverse()
                        stack.append(operators[token][1](*count_list))
                        count_list.clear()
                        break
                    else:
                        count_list.append(x)
        else:
            stack.append(token)
    if len(stack) >= 2:
        raise MyException("Error calculation")
    return stack[0]  # результат вычисления - единственный элемент в стеке
