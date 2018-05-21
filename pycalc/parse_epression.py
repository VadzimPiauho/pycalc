list_module = ["math"]
list_functions = ["abs", "pow", "round"]  # лист имеющихся функций в выражении
static_value = {}
EXPRESSION_PARSE = []  # выражение после парсинга
operators = {
    '!': (None, None),
    '=': (None, None),
    'abs': (7, abs),  # done
    'pow': (7, pow),  # done
    'round': (7, round),  # done
    '^': (6, lambda x, y: x ** y),  # done
    '-u': (5, lambda x, y=0: y - x),  # done
    '+u': (5, lambda x: x),  # done
    '*': (4, lambda x, y: x * y),  # done
    '/': (4, lambda x, y: x / y),  # done
    '//': (4, lambda x, y: x // y),  # done
    '%': (4, lambda x, y: x % y),  # done
    '+': (3, lambda x, y: x + y),  # done
    '-': (3, lambda x, y: x - y),  # done
    '!=': (2, lambda x, y: x != y),  # done
    '==': (2, lambda x, y: x == y),  # done
    '<': (1, lambda x, y: x < y),  # done
    '<=': (1, lambda x, y: x <= y),  # done
    '>': (1, lambda x, y: x > y),  # done
    '>=': (1, lambda x, y: x >= y),  # done
}


def replace_plus_minus(expression):
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


def check_int_float(number):
    tmp = float(number)
    if tmp.is_integer():
        EXPRESSION_PARSE.append(int(tmp))
    else:
        EXPRESSION_PARSE.append(float(number))


def parse_expression(expression):
    number = ''
    func = ''
    oper = ''
    bracket_stack = []
    for ind, val in enumerate(expression):
        if val in '1234567890.':  # если символ - цифра, то собираем число
            if func:
                tmp = func + val
                if any(tmp in s for s in list_functions):
                    func = func + val
                    continue
                else:
                    number += val
            else:
                number += val
        elif number:  # если символ не цифра, то выдаём собранное число и начинаем собирать заново
            if EXPRESSION_PARSE and EXPRESSION_PARSE[-1] == ")":
                # если цифра не первая в выражении и и последный символ
                # в выражении закрывающаяся скобка , то ставим знак умножения и выдаем цифру
                EXPRESSION_PARSE.append("*")
                check_int_float(number)
            elif val == "(":  # если после цифры скобка, то выдаем цифру и ставим знак умножения
                check_int_float(number)
                EXPRESSION_PARSE.append("*")
            else:  # просто выдаем цифру
                check_int_float(number)
            number = ''
        if val in 'abcdefghijklmnopqrstuvwxyz':  # если символ - ,буква, то собираем слово
            func += val
        elif func:  # если символ не буква, то выдаём собранное слово и начинаем собирать заново
            if func in static_value:
                EXPRESSION_PARSE.append(static_value[func])
            else:
                EXPRESSION_PARSE.append(str(func))  # выдаем слово в итоговое выражение
                EXPRESSION_PARSE.append("[")  # открываем скобку для аргументов функции
                bracket_stack.append("[")  # добавляем скобку в стек скобок
            func = ''
        if val in operators:  # если символ - оператор или скобка или запятая, то собираем оператор
            # если символ + или -, стоит в начале строки либо
            # после "(,^<>!=/*", либо собираемый оператор не равен 0 и состоит из символов "(,^<>!=/*"
            if (val == "+" or val == "-") and (len(EXPRESSION_PARSE) == 0 or (
                    str(EXPRESSION_PARSE[-1]) in "(,^<>!=/*" or (len(oper) != 0 and oper in "(,^<>!=/*"))):
                val += 'u'  # это унарный минус
                # если до унарного минуса собирался какой
                # либо оператор из operators выдаем его в итоговое выражение и обнуляем
                if oper and oper in operators:
                    EXPRESSION_PARSE.append(oper)
                    oper = ''
                EXPRESSION_PARSE.append(val)  # добавляем в итоговое выражение унарный минус
            else:
                oper += val
        elif oper:  # если символ не оператор, то выдаём собранный оператор и начинаем собирать заново
            if oper in operators:
                EXPRESSION_PARSE.append(oper)
                oper = ''
        if val in "(),":  # если символ "(),"
            if val == "(":
                bracket_stack.append(val)  # добавляем в стек скобок
                EXPRESSION_PARSE.append(val)  # добавляем в итоговое выражение
            elif val == ")":
                while bracket_stack:  # проверяем стек скобок
                    x = bracket_stack.pop()
                    if x == "(":  # если в стеке скобок "("
                        EXPRESSION_PARSE.append(val)  # добавляем в итоговое выражение ")
                    elif x == "[":
                        EXPRESSION_PARSE.append("]")
                        break
            else:
                EXPRESSION_PARSE.append(val)
    if number:  # если в конце строки есть число, выдаём его
        if EXPRESSION_PARSE and (EXPRESSION_PARSE[-1] == ")" or EXPRESSION_PARSE[-1] == "]"):
            # если перед полследним числом ")" или "ъ",
            # то ставим умножение и выдаем число, иначе просто выдаем число
            EXPRESSION_PARSE.append("*")
            check_int_float(number)
        else:
            check_int_float(number)
    elif func:
        if func in static_value:
            EXPRESSION_PARSE.append(static_value[func])
    return EXPRESSION_PARSE
