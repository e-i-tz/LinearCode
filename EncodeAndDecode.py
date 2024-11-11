import numpy as np
from itertools import combinations

def encode_message(message, G):
    codeword = np.dot(message, G) % 2
    return codeword

def decode_codeword(codeword, H):
    # Вычисляем синдром
    syndrome = np.dot(H, codeword.T) % 2
    # Если синдром равен нулевому вектору, ошибок нет
    if np.all(syndrome == 0):
        return codeword[:H.shape[0]], syndrome
    # Проверяем вес синдрома
    if np.sum(syndrome) > 1:
        raise ValueError("Слово содержит слишком много ошибок, декодирование невозможно.")
    # Возвращаем исправленное сообщение (первые k бит) и синдром
    return codeword[:H.shape[0]], syndrome


def find_all_invertible_submatrices(G, k, n):

    all_cols = list(range(n))
    used_cols = set()
    invertible_submatrices = []

    while len(used_cols) < n:
        best_submatrix = None
        best_submatrix_cols = None
        min_overlap = float('inf')

        for cols in combinations(all_cols, k):
            overlap = sum(col in used_cols for col in cols)
            if overlap >= min_overlap:
                continue

            submatrix = G[:, cols]
            if np.linalg.matrix_rank(submatrix) == k:
                best_submatrix = submatrix
                best_submatrix_cols = cols
                min_overlap = overlap

        if best_submatrix is None:
            raise ValueError("Не удалось найти достаточно подматриц для покрытия всех столбцов.")

        invertible_submatrices.append(list(best_submatrix_cols))
        used_cols.update(best_submatrix_cols)

    return invertible_submatrices











