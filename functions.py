# Файл с рекурсивными функциями
def print_to_n(n):
    #Вывести число от 1 до n
    if n < 1:
        return
    print_to_n(n - 1)
    print(n)


def print_reversed(n):
    #Вывести число от n до 1
    if n < 1:
        return
    print(n)
    print_reversed(n - 1)


def has_divider_smaller_than(n, i):
    #Получает true, если n после деления равно больше 1
    print(n, i)
    if i <= 1:
        return False
    else:
        if n % i == 0:
            return True
        else:
            return has_divider_smaller_than(n, i - 1)


def is_prime(n):
    #Взвращает значение, если n - простое число
    return not has_divider_smaller_than(n, int(n / 2))


def get_factorial(n):
    #Получить факториал n
    if (n <= 1):
        return n
    else:
        return n * (get_factorial(n - 1))


def exp_n_x(n, x):
    #Создание показательной функции, где n называется основанием степени, а x — показателем степени.
    if (n <= 1):
        return x
    else:
        return exp_n_x(n - 1, x) + (x ** n / get_factorial(n))


def play_hanoi(hanoi, n, src, dest, temp):
    """
    Функция с логикой Ханойских башен
    :параметр hanoi: объект hanoi
    :параметр n: счётчик дисков с исходной башни
    :параметр src: исходная башня
    :параметр dest: башня назначения
    :параметр temp: временная башня
    """
    if n == 1:
        hanoi.move(src, dest)
        return
    play_hanoi(hanoi, n - 1, src, temp, dest)
    hanoi.move(src, dest)
    play_hanoi(hanoi, n - 1, temp, dest, src)


def permutations(head, tail='', printed=[]):
    #Вывод перестановок строки
    if len(head) == 0 and tail not in printed:
        print(tail)
        printed.append(tail)
    else:
        for i in range(len(head)):
            permutations(head[0:i] + head[i + 1:], tail + head[i], printed)


def print_sequences(char_list, n, ret=[]):
    #Вывести все последовательности char-список с длинной n
    if (len(ret) == n):
        print("".join(ret))
    else:
        for item in char_list:
            new_list = ret[:]
            new_list.append(item)
            print_sequences(char_list, n, new_list)


def print_no_repetition_sequences(char_list, n):
    #Возвращает char-список последовательностей без повторов
    for i in range(len(char_list)):
        if (len(char_list) == n):
            permutations("".join(char_list))
        else:
            new_list = char_list[:]
            new_list.pop(i)
            print_no_repetition_sequences(new_list, n)


def parentheses(n, count_open=0, count_close=0, item_str="", ret=[]):
    #Возвращает все круглые скобки с длинной n
    if count_close == int(n):
        ret.append(item_str)
    else:
        if count_open == int(n):
            parentheses(n, count_open, count_close + 1, item_str + ")")
        else:
            if count_open == count_close:
                parentheses(n, count_open + 1, count_close, item_str + "(")
            else:
                parentheses(n, count_open + 1, count_close, item_str + "(")
                parentheses(n, count_open, count_close + 1, item_str + ")")
    return ret


def up_and_right(n, k, current=(0, 0), ret=''):
    #Выводит все пути от n до k
    if current == (n, k):
        print(ret)
    if current[0] <= n:
        up_and_right(n, k, (current[0] + 1, current[1]), ret + "r")
    if current[1] <= k:
        up_and_right(n, k, (current[0], current[1] + 1), ret + "u")


def flood_fill(image, start):
    #
    """
    Функция обновляет изображение посредсвтом алгоритма Flood-fill
    :параметр image: матрица
    :параметр start: начальная точка (кортеж)
    """
    image[start[0]][start[1]] = '*'
    if start[0] > 0 and image[start[0] - 1][start[1]] == '.':
        flood_fill(image, (start[0] - 1, start[1]))
    if start[0] < (len(image) - 1) and image[start[0] + 1][start[1]] == '.':
        flood_fill(image, (start[0] + 1, start[1]))
    if start[1] > 0 and image[start[0]][start[1] - 1] == '.':
        flood_fill(image, (start[0], start[1] - 1))
    if start[1] < len(image[0]) - 1 and image[start[0]][start[1] + 1] == '.':
        flood_fill(image, (start[0], start[1] + 1))


if __name__ == '__main__':
    print_no_repetition_sequences(['a', 'b'], 2)
