import numpy as np

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
            # Подсчитываем минимальный вес строки в G, получая минимальный вес кода и сравнивая его с d
            min_weight = np.min(np.sum(G, axis=1))
            if min_weight == d:
                break
    return G, A


def create_parity_check_matrix(A):
    I = np.eye(A.shape[1], dtype=int)
    A = A.T
    H = np.hstack((A, I))
    return H







