from math import comb

def get_code_parameters():
    while True:
        try:
            n = int(input("Введите значение n (длина кода): "))
            k = int(input("Введите значение k (размер сообщения): "))
            d = int(input("Введите значение d (3 или 4, минимальное расстояние): "))
            if d not in [3, 4]:
                raise ValueError("Значение d должно быть 3 или 4.")
            break
        except ValueError as e:
            print(e)
            print("Попробуйте еще раз.")
    return n, k, d

def check_hamming_bound(n, k, d):
    left_side = 2 ** k
    right_side = 2 ** n / sum(comb(n, i) for i in range((d-1)//2))
    return left_side <= right_side

def check_vashamov_gilbert_bound(n, k, d):
    left_side = 2 ** k
    right_side = 2 ** n / sum(comb(n, i) for i in range(d-1))
    return left_side <= right_side

def check_singleton_bound(n, k, d):
    return k <= n - d + 1

def validate_code_parameters(n, k, d):
    if not check_hamming_bound(n, k, d):
        raise ValueError("Параметры кода не удовлетворяют границе Хэмминга.")
    if not check_singleton_bound(n, k, d):
        raise ValueError("Параметры кода не удовлетворяют границе Синглтона.")
    if not check_vashamov_gilbert_bound(n, k, d):
        raise ValueError("Параметры кода не удовлетворяют границе Варшамова-Гильберта.")
    return True




