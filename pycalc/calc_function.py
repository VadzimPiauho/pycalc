def calc(DATA_OUT):
    stack = []
    count_list = []
    for token in DATA_OUT:
        if token in OPERATORS:  # если приходящий элемент - оператор,
            if token not in LIST_FUNCTION:
                if token == "-u" or token == "+u":
                    stack.append(OPERATORS[token][1](stack.pop()))
                elif token == "^":
                    y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                    stack.append(OPERATORS[token][1](x, y))
                else:
                    y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                    stack.append(OPERATORS[token][1](x, y))
            else:
                while stack:
                    x = stack.pop()
                    if x == "]" or x == ",":
                        continue
                    elif x == "[":
                        count_list.reverse()
                        stack.append(OPERATORS[token][1](*count_list))
                        count_list.clear()
                        break
                    else:
                        count_list.append(x)
        else:
            stack.append(token)
    return stack[0]  # результат вычисления - единственный элемент в стеке


return calc(DATA_OUT)