import numpy as np
from itertools import combinations

def encode_message(message, G):
    codeword = np.dot(message, G) % 2
    return codeword

def decode_codeword(codeword, H, G, k, n):
    # Вычисляем синдром
    syndrome = np.dot(codeword, H.T) % 2
    # Если синдром равен нулевому вектору, ошибок нет
    if np.sum(syndrome) == 0:
        return codeword[:G.shape[0]], syndrome, codeword, np.zeros_like(codeword)

    invertible_submatrices = find_all_invertible_submatrices(G, k, n)
    inverse_submatrices = create_inverse_submatrices(G, invertible_submatrices)
    result_matrices = multiply_inverse_matrices_with_G(G, inverse_submatrices)
    coded_words = get_codewords(codeword, invertible_submatrices, result_matrices)
    error_vector = find_error_vector(codeword, coded_words)

    # Проверка количества единиц в векторе ошибок
    if np.sum(error_vector) > 1:
        raise ValueError("Однозначное декодирование невозможно.")

    corrected_word = correct_codeword(codeword, error_vector)
    syndrome2 = np.dot(corrected_word, H.T) % 2
    # Проверяем синдром
    if np.any(syndrome2 != 0):
        raise ValueError("Слово содержит слишком много ошибок, декодирование невозможно.")
    # Возвращаем исправленное сообщение (первые k бит), синдром и исправленное кодовое слово
    return corrected_word[:G.shape[0]], syndrome, corrected_word, error_vector


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
            try:
                # Проверяем обратимость подматрицы с помощью функции mod2_inv
                mod2_inv(submatrix)
                best_submatrix = submatrix
                best_submatrix_cols = cols
                min_overlap = overlap
            except ValueError:
                continue  # Если подматрица необратима, пропускаем её и продолжаем

        if best_submatrix is None:
            raise ValueError("Не удалось найти достаточно подматриц для покрытия всех столбцов.")

        invertible_submatrices.append(list(best_submatrix_cols))
        used_cols.update(best_submatrix_cols)

    return invertible_submatrices

def mod2_inv(matrix):
    n = matrix.shape[0]
    identity = np.eye(n, dtype=int)
    augmented = np.hstack((matrix, identity))

    for i in range(n):
        if augmented[i, i] == 0:
            for j in range(i + 1, n):
                if augmented[j, i] == 1:
                    augmented[[i, j]] = augmented[[j, i]]
                    break

        if augmented[i, i] == 0:
            raise ValueError("Матрица необратима в поле GF(2).")

        for j in range(n):
            if i != j and augmented[j, i] == 1:
                augmented[j] = (augmented[j] + augmented[i]) % 2

    inverse_matrix = augmented[:, n:]
    return inverse_matrix


# Получение обратных матриц
def create_inverse_submatrices(G, invertible_submatrices):

    inverse_submatrices = []

    for cols in invertible_submatrices:
        submatrix = G[:, cols]
        inverse_submatrix = mod2_inv(submatrix)
        inverse_submatrices.append(inverse_submatrix)

    return inverse_submatrices

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

def find_error_vector(codeword, coded_words):
    min_weight = np.inf
    error_vector = None

    for word in coded_words:
        difference = (codeword - word) % 2
        weight = np.sum(difference)
        if weight < min_weight:
            min_weight = weight
            error_vector = difference

    return error_vector

def correct_codeword(codeword, error_vector):
    corrected_word = (codeword - error_vector) % 2
    return corrected_word

def detectRightWord(codeword, coded_words):
    weights_array = {}
    for c in range(len(coded_words)):
        difference = np.array((codeword - coded_words[c]) % 2)
        print(f'Разность между кодовым словом и с{c} {codeword} - {coded_words[c]} = {difference}')
        weight = findHammingWeight(difference)
        print(f"W(h) для {c} = {weight}")
        weights_array[weight] = coded_words[c]

    min_weight = min(weights_array.keys())
    decoded_word = weights_array[min_weight]
    return decoded_word

#Нахождение веса хэммингаа
def findHammingWeight(word):
    int_word = word.astype(int)
    return np.sum(int_word)















