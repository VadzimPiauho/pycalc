from .parse_epression import operators

STACK_OPERATOR = []  # стек операторов
DATA_OUT = []


def poland_notation(expression_parse):
    for i in expression_parse:  # преобразуем выражение после парсинга по алгоритму обратной польской записи
        if i in operators:
            while STACK_OPERATOR and STACK_OPERATOR[-1] != "(" and operators[i][0] <= operators[STACK_OPERATOR[-1]][0]:
                x = STACK_OPERATOR.pop()
                # if (x == "+u" or x == "-u") and i in "+-*/":
                #     if len(STACK_OPERATOR) >= 1:
                #         DATA_OUT.append(x)
                #         #DATA_OUT.append(STACK_OPERATOR.pop())
                #     else:
                #         DATA_OUT.append(x)
                #         break
                # elif x == "+u" or x == "-u":
                #     STACK_OPERATOR.append(x)
                #     break
                if x == "^" and i == "^":  # решение проблемы приоритетов если 5^-1
                    STACK_OPERATOR.append(i)
                    break
                elif (i == "+u" or i == "-u") and x == "^":
                    STACK_OPERATOR.append(x)
                    break
                else:
                    DATA_OUT.append(x)
            STACK_OPERATOR.append(i)
        elif i == ")":  # если ")" выдаем из стека операторов все элементы по не "("
            while STACK_OPERATOR:
                x = STACK_OPERATOR.pop()
                if x not in "(":
                    DATA_OUT.append(x)
                else:
                    break
        elif i == "(":
            STACK_OPERATOR.append(i)  # если элемент - открывающая скобка, просто положим её в стек
        elif i == ",":
            while STACK_OPERATOR and STACK_OPERATOR[-1] != "(":
                DATA_OUT.append(STACK_OPERATOR.pop())
        else:
            DATA_OUT.append(i)  # если элемент - число, отправим его сразу на выход

    while STACK_OPERATOR:
        DATA_OUT.append(STACK_OPERATOR.pop())
    return DATA_OUT
