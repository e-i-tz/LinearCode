from EncodeAndDecode import encode_message, find_all_invertible_submatrices, find_all_invertible_submatrices
from InputParametrs import get_code_parameters, validate_code_parameters, input_message
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

#print("Исходное сообщение:", message)
#print("Кодовое слово:", codeword)
#print("Построенный код может исправить одну ошибку")
#print("Проверочная матрица H:")
print("Генераторная матрица G в систематическом виде:")
print(G)
#print("Проверочная матрица H:")
#print(H)

invertible_submatrices = find_all_invertible_submatrices(G, k, n)
print("Индексы столбцов, образующих обратимые подматрицы:", invertible_submatrices)
for idx, cols in enumerate(invertible_submatrices):
    print(f"Подматрица {idx + 1}:")
    print(G[:, cols])
