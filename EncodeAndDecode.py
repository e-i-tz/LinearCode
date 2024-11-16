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

# Получение обратных матриц
def create_inverse_submatrices(G, invertible_submatrices):

    inverse_submatrices = []

    for cols in invertible_submatrices:
        submatrix = G[:, cols]
        inverse_submatrix = mod2_inv(submatrix)
        inverse_submatrices.append(inverse_submatrix)

    return inverse_submatrices

# Нахождение обратной матрицы над полем GF(2)
def mod2_inv(matrix):

    n = matrix.shape[0]
    identity = np.eye(n, dtype=int)
    augmented = np.hstack((matrix, identity))

    for i in range(n):
        # Находим строку с ненулевым элементом в текущем столбце
        if augmented[i, i] == 0:
            for j in range(i + 1, n):
                if augmented[j, i] == 1:
                    augmented[[i, j]] = augmented[[j, i]]
                    break

        # Если все элементы столбца равны нулю, матрица необратима
        if augmented[i, i] == 0:
            raise ValueError("Матрица необратима в поле GF(2).")

        # Приводим элемент на главной диагонали к 1 и обнуляем остальные элементы в этом столбце
        for j in range(n):
            if i != j and augmented[j, i] == 1:
                augmented[j] = (augmented[j] + augmented[i]) % 2

    inverse_matrix = augmented[:, n:]
    return inverse_matrix


def multiply_inverse_matrices_with_G(G, inverse_submatrices):

    result_matrices = []

    for inverse_submatrix in inverse_submatrices:
        result_matrix = np.dot(inverse_submatrix, G) % 2
        result_matrices.append(result_matrix)

    return result_matrices


def get_codewords(a, invertible_submatrices, result_matrices):
    coded_words = []
    for cols, result_matrix in zip(invertible_submatrices, result_matrices):
        # Составляем вектор a1, выбирая элементы на позициях из cols
        a1 = np.array([a[i] for i in cols])
        # Кодируем вектор a1 с помощью результирующей матрицы
        c1 = np.dot(a1, result_matrix) % 2
        coded_words.append(c1)

    return coded_words

def detectRightWord(codeword, coded_words):
    weights_array = {}
    for c in range(len(coded_words)):
        difference = np.array((codeword - coded_words[c]) % 2)
        weight = findHammingWeight(difference)
        weights_array[weight] = coded_words[c]

    min_weight = min(weights_array.keys())
    decoded_word = weights_array[min_weight]
    return decoded_word

#Нахождение веса хэммингаа
def findHammingWeight(word):
    int_word = word.astype(int)
    return np.sum(int_word)















