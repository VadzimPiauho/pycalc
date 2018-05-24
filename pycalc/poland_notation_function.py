from .parse_epression import operators


def poland_notation(expression_parse):
    stack_operator = []  # стек операторов
    data_out = []
    for i in expression_parse:  # преобразуем выражение после парсинга по алгоритму обратной польской записи
        if i in operators:
            while stack_operator and stack_operator[-1] != "(" and operators[i][0] <= operators[stack_operator[-1]][0]:
                x = stack_operator.pop()
                if x == "^" and i == "^":  # решение проблемы приоритетов если 5^-1
                    stack_operator.append(i)
                    break
                elif (i == "+u" or i == "-u") and x == "^":
                    stack_operator.append(x)
                    break
                else:
                    data_out.append(x)
            stack_operator.append(i)
        elif i == ")":  # если ")" выдаем из стека операторов все элементы по не "("
            while stack_operator:
                x = stack_operator.pop()
                if x not in "(":
                    data_out.append(x)
                else:
                    break
        elif i == "(":
            stack_operator.append(i)  # если элемент - открывающая скобка, просто положим её в стек
        elif i == ",":
            while stack_operator and stack_operator[-1] != "(":
                data_out.append(stack_operator.pop())
        else:
            data_out.append(i)  # если элемент - число, отправим его сразу на выход

    while stack_operator:
        data_out.append(stack_operator.pop())
    return data_out
