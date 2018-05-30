list_module = ["math"]
list_functions = ["abs", "pow", "round"]  # лист имеющихся функций в выражении
static_value = {}
operators = {
    '!': (None, None),
    '=': (None, None),
    'abs': (7, abs),
    'pow': (7, pow),
    'round': (7, round),
    '^': (6, lambda x, y: x ** y),
    '-u': (5, lambda x, y=0: y - x),
    '+u': (5, lambda x: x),
    '*': (4, lambda x, y: x * y),
    '/': (4, lambda x, y: x / y),
    '//': (4, lambda x, y: x // y),
    '%': (4, lambda x, y: x % y),
    '+': (3, lambda x, y: x + y),
    '-': (3, lambda x, y: x - y),
    '!=': (2, lambda x, y: x != y),
    '==': (2, lambda x, y: x == y),
    '<': (1, lambda x, y: x < y),
    '<=': (1, lambda x, y: x <= y),
    '>': (1, lambda x, y: x > y),
    '>=': (1, lambda x, y: x >= y),
}


def replace_plus_minus(expression):
    """
    Function of removing spaces from an expression
    :param expression: Input expression
    :return: expression without spaces
    """
    dic = {"--": "+", "+-": "-", "-+": "-", "++": "+"}
    old_len = len(expression)
    while True:
        for i, j in dic.items():
            expression = expression.replace(i, j)
        new_len = len(expression)
        if new_len == old_len:
            break
        else:
            old_len = new_len
    return expression


def check_int_float(number, expression_parse):
    """
    Function for checking the type of a number
    :param number: Input expression
    :param expression_parse: list of separated expression
    """
    tmp = float(number)
    if tmp.is_integer():
        expression_parse.append(int(tmp))
    else:
        expression_parse.append(float(number))


def parse_expression(expression):
    """
    Function of dividing expression by numbers, functions and operations
    :param expression: Input expression
    :return: separated expression
    """
    number = ''
    func = ''
    operator = ''
    bracket_stack = []
    expression_parse = []  # выражение после парсинга

    for ind, val in enumerate(expression):
        if val in " ":
            continue
        elif val in '1234567890.':  # если символ - цифра, то собираем число
            if func:
                tmp = func + val
                if any(tmp in s for s in list_functions):
                    func = func + val
                    continue
                # else:
                #     number += val
            else:
                number += val
        elif number:  # если символ не цифра, то выдаём собранное число и начинаем собирать заново
            if expression_parse and expression_parse[-1] == ")":
                # если цифра не первая в выражении и и последный символ
                # в выражении закрывающаяся скобка , то ставим знак умножения и выдаем цифру
                expression_parse.append("*")
                check_int_float(number, expression_parse)
            elif val == "(":  # если после цифры скобка, то выдаем цифру и ставим знак умножения
                check_int_float(number, expression_parse)
                expression_parse.append("*")
            else:  # просто выдаем цифру
                check_int_float(number, expression_parse)
            number = ''
        if val in 'abcdefghijklmnopqrstuvwxyz':  # если символ - ,буква, то собираем слово
            func += val
        elif func:  # если символ не буква, то выдаём собранное слово и начинаем собирать заново
            if func in static_value:
                expression_parse.append(static_value[func])
            else:
                expression_parse.append(str(func))  # выдаем слово в итоговое выражение
                expression_parse.append("[")  # открываем скобку для аргументов функции
                bracket_stack.append("[")  # добавляем скобку в стек скобок
            func = ''
        if val in operators:  # если символ - оператор или скобка или запятая, то собираем оператор
            # если символ + или -, стоит в начале строки либо
            # после "(,^<>!=/*", либо собираемый оператор не равен 0 и состоит из символов "(,^<>!=/*"
            if (val == "+" or val == "-") and (len(expression_parse) == 0 or (
                    str(expression_parse[-1]) in "(,^<>!=/*" or (len(operator) != 0 and operator in "(,^<>!=/*"))):
                val += 'u'  # это унарный минус
                # если до унарного минуса собирался какой
                # либо оператор из operators выдаем его в итоговое выражение и обнуляем
                if operator and operator in operators:
                    expression_parse.append(operator)
                    operator = ''
                expression_parse.append(val)  # добавляем в итоговое выражение унарный минус
            else:
                operator += val
                operator = replace_plus_minus(operator)
        elif operator:  # если символ не оператор, то выдаём собранный оператор и начинаем собирать заново
            if operator in operators:
                if expression_parse and expression_parse[-1] == "-u" or expression_parse[-1] == "+u":
                    operator += 'u'
                    x = expression_parse.pop()
                    if x == operator == "+u":
                        expression_parse.append(operator)
                    elif x == operator == "-u":
                        expression_parse.append("+u")
                    elif (x == "-u" and operator == "+u") or (x == "+u" and operator == "-u"):
                        expression_parse.append("-u")
                else:
                    expression_parse.append(operator)
                operator = ''
        if val in "(),":  # если символ "(),"
            if val == "(":
                bracket_stack.append(val)  # добавляем в стек скобок
                expression_parse.append(val)  # добавляем в итоговое выражение
            elif val == ")":
                while bracket_stack:  # проверяем стек скобок
                    x = bracket_stack.pop()
                    if x == "(":  # если в стеке скобок "("
                        expression_parse.append(val)  # добавляем в итоговое выражение ")
                        if len(bracket_stack):
                            x = bracket_stack.pop()
                            if x == "(":
                                bracket_stack.append(x)
                                break
                            elif x == "[":
                                expression_parse.append("]")
                                break
            else:
                expression_parse.append(val)
    if number:  # если в конце строки есть число, выдаём его
        if expression_parse and (expression_parse[-1] == ")" or expression_parse[-1] == "]"):
            # если перед полследним числом ")" или "ъ",
            # то ставим умножение и выдаем число, иначе просто выдаем число
            expression_parse.append("*")
            check_int_float(number, expression_parse)
        else:
            check_int_float(number, expression_parse)
    elif func:
        if func in static_value:
            expression_parse.append(static_value[func])
    return expression_parse
