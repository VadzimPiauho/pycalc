import math

static_value = {}
list_functions = ["abs", "pow", "round"]  # лист имеющихся функций в выражении
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
for key in math.__dict__:
    if callable(math.__dict__[key]):
        operators[key] = (7, getattr(math, key))
        list_functions.append(key)
    else:
        static_value[key] = getattr(math, key)


def test_func(EXPRESSION, operators):
    DATA_OUT = []
    STACK_OPERATOR = []  # стек операторов
    EXPRESSION_PARSE = []  # выражение после парсинга

    def replace_plus_minus(EXPRESSION):
        dic = {"--": "+", "+-": "-", "-+": "-", "++": "+"}
        old_len = len(EXPRESSION)
        while True:
            for i, j in dic.items():
                EXPRESSION = EXPRESSION.replace(i, j)
            new_len = len(EXPRESSION)
            if new_len == old_len:
                break
            else:
                old_len = new_len
        return EXPRESSION

    # EXPRESSION = EXPRESSION.replace(" ", "")

    # EXPRESSION = replace_plus_minus(EXPRESSION)

    def check_int_float(number):
        tmp = float(number)
        if tmp.is_integer():
            EXPRESSION_PARSE.append(int(tmp))
        else:
            EXPRESSION_PARSE.append(float(number))

    def parse_expression(EXPRESSION):
        number = ''
        func = ''
        oper = ''
        bracket_stack = []
        for ind, val in enumerate(EXPRESSION):
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
                    oper = replace_plus_minus(oper)
            elif oper:  # если символ не оператор, то выдаём собранный оператор и начинаем собирать заново
                if oper in operators:
                    if EXPRESSION_PARSE and EXPRESSION_PARSE[-1] == "-u" or EXPRESSION_PARSE[-1] == "+u":
                        oper += 'u'
                        x = EXPRESSION_PARSE.pop()
                        if x == oper == "+u":
                            EXPRESSION_PARSE.append(oper)
                        elif x == oper == "-u":
                            EXPRESSION_PARSE.append("+u")
                        elif (x == "-u" and oper == "+u") or (x == "+u" and oper == "-u"):
                            EXPRESSION_PARSE.append("-u")
                    else:
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
                            if len(bracket_stack):
                                x = bracket_stack.pop()
                                if x == "(":
                                    bracket_stack.append(x)
                                    break
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

    parse_expression(EXPRESSION)  # функция парсинга входного выражения по элементам

    for i in EXPRESSION_PARSE:  # преобразуем выражение после парсинга по алгоритму обратной польской записи
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

    def calc(DATA_OUT):
        stack = []
        count_list = []
        for token in DATA_OUT:
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

    return calc(DATA_OUT)


if __name__ == '__main__':
    MASS_EXPRESSION = [
        # # Unary operators
        # ("-13", -13),
        # ("6-(-13)", 19),
        # ("1-- -1", 0),
        # ("1---1", 0),
        # ("1 -  1", 0),
        # ("-+---+-1", -1),
        # # Operation priority
        # ("1+2*2", 5),
        # ("1+(2+32)3", 103),
        # ("10*(2+1)", 30),
        # ("10^(2+1)", 1000),
        # ("100/3^2", 11.11111111111111),
        # ("100/3%2^2", 1.3333333333333357),
        # # Functions and constants
        # ("pi+e", 5.859874482048838),
        # ("log(e)", 1.0),
        # ("sin(pi/2)", 1.0),
        # ("log10(100)", 2.0),
        # ("sin(pi/2)1116", 1116.0),
        # ("2*sin(pi/2)", 2.0),
        # # Associative
        # ("102%12%7", 6),
        # ("100/4/3", 8.333333333333334),
        # ("2^3^4", 2417851639229258349412352),
        # # Comparison operators
        # ("1+23==1+23", True),
        # ("e^5>=e^5+1", False),
        # ("1+24/3+1!=1+24/3+2", True),
        # # Common tests
        # ("(100)", 100),
        # ("666", 666),
        # ("10(2+1)", 30),
        # ("(2+1)10+1", 31),
        # ("(2+1)10", 30),
        # ("-.1", -0.1),
        # ("1/3", 0.3333333333333333),
        # ("1.0/3.0", 0.3333333333333333),
        # (".1*2.0^56.0", 7205759403792794.0),
        # ("e^34", 583461742527453.9),
        # ("(2.0^(pi/pi+e/e+2.0^0.0))", 8.0),
        # ("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)", 2.0),
        # ("sin(pi/2^1) + log(1*4+2^2+1, 3^2)", 2.0),
        # ("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53/10) + -5", 10.3),
        # ("log10(.4* -5/ -0.1-10)", 1.0),
        # ("- -abs(-53/10) + -5", 0.2999999999999998),
        # ("- -abs(-53/10)", 5.3),
        # ("2*-1", -2),
        # ("10*e^0", 10.0),
        # ("2.0^(2.0^2.0*2.0^2.0)", 65536.0),
        # ("(2.0^2.0*2.0^2.0)", 16),
        # ("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))", 0.76638122986603),
        # (
        #     "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)",
        #     0.5361064001012783),
        # ("--cos(1.0)--cos(0.0)^3.0", 1.5403023058681398),
        # ("cos(sin(sin(34.0-2.0^2.0)))", 0.6712189482597033),
        # ("-sin(cos(log10(43.0)))", 0.06259017093637237),
        # ("-cos(-sin(-3.0*5.0))", -0.7959095686227995),
        # ("-cos(-sin(3.0))", -0.9900590857598653),
        # ("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0))))", -0.5581746423992129),
        # ("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))))",
        #  -0.8274124603473457),
        # ("cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))", 1.4277017012821114),
        # # My cases
        # ("-2", -2),
        # ("3-2", 1),
        # ("(-3)", -3),
        # ("((-4))", -4),
        # ("-((5))", -5),
        # ("(-(6))", -6),
        # ("-2+1+1", 0),
        # ("-2-1", -3),
        # ("-2*1", -2),
        # ("2*-1", -2),
        # ("5^-1", 0.2),
        # ("5^-1-1", -0.8),
        # ("5^-1*2", 0.4),
        # ("-53/10", -5.3),
        # ("+abs(-53/10)", 5.3),
        # ("-(2)+1+1", 0),
        # ("(-2)+1+1", 0),
        # ("-(2+1+1)", -4),
        # ("3+2+2", 7),
        # ("2*(1+1)", 4),
        # ("pow(2,2)", 4),
        # ("pow(2,pow(2,1))", 4),
        # ("pow(2,-(2))", 0.25),
        # ("pow(2,(-2))", 0.25),
        # ("2*-2", -4),
        # ("2+2*-2", -2),
        # ("2^2^3", 256),
        # ("2-2-3", -3),
        # ("5/-1*2", -10),
        # ("5/-1", -5),
        # ("5^-1/2", 0.1),
        # ("-5^-1-1", -1.2),
        # ("5^-(1)", 0.2),
        # ("5^-(.1)", 0.8513399225207846),
        # ("5^-.1", 0.8513399225207846),
        # ("5^(-1)", 0.2),
        # ("5^(1)", 5),
        # ("2/5^(-(1))", 10),
        # ("2/5^(-1)", 10),
        # ("--2+2++-+-2", 6),
        # ("-5^2", -25),
        # ("round(2*2*2+2,2)", 10),
        # ("-5^-1", -0.2),
        # ("2/-5^-1", -10.0),
        # ("round(2^2,2)", 4),
        # ("round(2^2)", 4),
        # ("-(-2)", 2),
        # ("round(1>=1)", 1),
        # ("-(2+1+(-2))", -1),
        # ("round((2/3)^213,round(1+114+332.2/4))", 3.1085783725131357e-38),
        # ("round((2/3)^213,round(1+114+332.2/4))/5^-1-1", -1.0),
        # ("round(1/3,2)", 0.33),
        # ("sin(1/3)", 0.3271946967961522),
        # ("2+sin(1/3)", 2.3271946967961523),
        # ("-sin(2)^2", -0.826821810431806),

        # Error cases
        # *""
        #  * "+"
        #  * "1-"
        #  * "1 2"
        #  * "ee"
        #  * "123e"
        #  * "==7"
        #  * "1 * * 2"
        #  * "1 + 2(3 * 4))"
        #  * "((1+2)"
        #  * "1 + 1 2 3 4 5 6 "
        #  * "log100(100)"
        #  * "------"
        #  * "5 > = 6"
        #  * "5 / / 6"
        #  * "6 < = 6"
        #  * "6 * * 6"
        #  * "((((("
        # # My cases
        # ("-2", -2),
        # ("3-2", 1),
        # ("(-3)", -3),
        # ("((-4))", -4),
        # ("-((5))", -5),
        # ("(-(6))", -6),
        # ("-2+1+1", 0),
        # ("-2-1", -3),
        # ("-2*1", -2),
        # ("2*-1", -2),
        # ("5^-1", 0.2),
        # ("5^-1-1", -0.8),
        # ("5^-1*2", 0.4),
        # ("-53/10", -5.3),
        # ("+abs(-53/10)", 5.3),
        # ("-(2)+1+1", 0),
        # ("(-2)+1+1", 0),
        # ("-(2+1+1)", -4),
        # ("3+2+2", 7),
        # ("2*(1+1)", 4),
        # ("pow(2,2)", 4),
        # ("pow(2,pow(2,1))", 4),
        # ("pow(2,-(2))", 0.25),
        # ("pow(2,(-2))", 0.25),
        # ("2*-2", -4),
        # ("2+2*-2", -2),
        # ("2^2^3", 256),
        # ("2-2-3", -3),
        # ("5/-1*2", -10),
        # ("5/-1", -5),
        # ("5^-1/2", 0.1),
        # ("-5^-1-1", -1.2),
        # ("5^-(1)", 0.2),
        # ("5^-(.1)", 0.8513399225207846),
        # ("5^-.1", 0.8513399225207846),
        # ("5^(-1)", 0.2),
        # ("5^(1)", 5),
        # ("2/5^(-(1))", 10),
        # ("2/5^(-1)", 10),
        # ("--2+2++-+-2", 6),
        # ("-5^2", -25),
        # ("round(2*2*2+2,2)", 10),
        # ("-5^-1", -0.2),
        # ("2/-5^-1", -10.0),
        # ("round(2^2,2)", 4),
        # ("round(2^2)", 4),
        # ("-(-2)", 2),
        # ("round(1>=1)", 1),
        # ("-(2+1+(-2))", -1),
        # ("round((2/3)^213,round(1+114+332.2/4))", 3.1085783725131357e-38),
        # ("round((2/3)^213,round(1+114+332.2/4))/5^-1-1", -1.0),
        # ("round((2/3))", 1),
        # ("round(1/3,2)", 0.33),
        # ("sin(1/3)", 0.3271946967961522),
        # ("2+sin(1/3)", 2.3271946967961523),
        # ("-sin(2)^2", -0.826821810431806),
    ]
    for counter, EXPRESSION in enumerate(MASS_EXPRESSION):
        res = test_func(EXPRESSION[0], operators)
        if res == EXPRESSION[1]:
            print("{}\t\t{}".format("Done", EXPRESSION[0]))
        else:
            print("{}\t\t{}".format("False", EXPRESSION[0]))
