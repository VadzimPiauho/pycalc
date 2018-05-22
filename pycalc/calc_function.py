from .parse_epression import operators, list_functions


def calc(data_out):
    stack = []
    count_list = []
    for token in data_out:
        if token in operators:  # если приходящий элемент - оператор,
            if token not in list_functions:
                if token == "-u" or token == "+u":
                    stack.append(operators[token][1](stack.pop()))
                elif token == "^":
                    y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                    stack.append(operators[token][1](x, y))
                else:
                    y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                    stack.append(operators[token][1](x, y))
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
    return stack[0]  # результат вычисления - единственный элемент в стеке
