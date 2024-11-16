from EncodeAndDecode import encode_message, find_all_invertible_submatrices, find_all_invertible_submatrices, \
    create_inverse_submatrices, multiply_inverse_matrices_with_G, get_codewords
from InputParametrs import get_code_parameters, validate_code_parameters, input_message, input_codeword
from GeneratorAndCheckMatrix import create_generator_matrix, create_parity_check_matrix

n, k, d = get_code_parameters()

try:
    if validate_code_parameters(n, k, d):
        print("Параметры кода удовлетворяют всем границам.")
except ValueError as e:
    print(e)

G, A = create_generator_matrix(k, n, d)
H = create_parity_check_matrix(A)

message = input_message(k)
codeword = encode_message(message, G)

print("Исходное сообщение:", message)
print("Кодовое слово:", codeword)
#print("Построенный код может исправить одну ошибку")
print("Генераторная матрица G в систематическом виде:")
print(G)
print("Проверочная матрица H:")
print(H)

invertible_submatrices = find_all_invertible_submatrices(G, k, n)
print("Индексы столбцов, образующих обратимые подматрицы:", invertible_submatrices)
for idx, cols in enumerate(invertible_submatrices):
    print(f"Подматрица {idx + 1}:")
    print(G[:, cols])

# Создание и обращение подматриц
inverse_submatrices = create_inverse_submatrices(G, invertible_submatrices)

print("Обратные матрицы подматриц:")
for i, inverse_submatrix in enumerate(inverse_submatrices):
    print(f"Обратная матрица {i + 1}:")
    print(inverse_submatrix)

# Умножение обратных матриц на изначальную генераторную матрицу G
result_matrices = multiply_inverse_matrices_with_G(G, inverse_submatrices)

print("Результирующие матрицы:")
for i, result_matrix in enumerate(result_matrices):
    print(f"Результирующая матрица {i + 1}:")
    print(result_matrix)

a = input_codeword(n)

# Декодирование слова с помощью обратных и результирующих матриц
coded_words = get_codewords(a, invertible_submatrices, result_matrices)

for i, coded_word in enumerate(coded_words):
    print(f"Закодированное слово {i + 1}:")
    print(coded_word)
