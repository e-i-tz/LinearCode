import numpy as np
from itertools import combinations

# Создает генераторную матрицу G размером k x n в систематическом виде [I | A].
def create_generator_matrix(k, n, d):
    # Строит I, генерирует A и проверяет линейную независимость строк в получившейся G, повторяя процесс при необходимости.
    I = np.eye(k, dtype=int)
    while True:
        # Генерируем случайную бинарную матрицу A размером k x (n-k)
        A = np.random.randint(0, 2, (k, n - k))
        # Конкатенируем I и A, чтобы получить генераторную матрицу G
        G = np.hstack((I, A))
        # Проверяем, что строки матрицы G линейно независимы
        if np.linalg.matrix_rank(G) == k:
            H = create_parity_check_matrix(A)
            d_H = find_minimum_distance(H)
            if d_H == d:
                break
    return G, A


def create_parity_check_matrix(A):
    I = np.eye(A.shape[1], dtype=int)
    A = A.T
    H = np.hstack((A, I))
    return H


def find_minimum_distance(H):
    n = H.shape[1]
    for d in range(2, n + 1):
        for cols in combinations(range(n), d):
            submatrix = H[:, cols]
            if np.linalg.matrix_rank(submatrix) < d:
                return d
    return n + 1  # Если все столбцы линейно независимы








