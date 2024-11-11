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
    return G

# Пример использования:
k = 4
n = 7
d = 4
G = create_generator_matrix(k, n, d)
print("Генераторная матрица G в систематическом виде:")
print(G)
