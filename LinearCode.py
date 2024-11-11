from InputParametrs import get_code_parameters, validate_code_parameters
from GeneratorAndCheckMatrix import create_generator_matrix, create_parity_check_matrix

n, k, d = get_code_parameters()

try:
    if validate_code_parameters(n, k, d):
        print("Параметры кода удовлетворяют всем границам.")
except ValueError as e:
    print(e)

G, A = create_generator_matrix(k, n, d)
H = create_parity_check_matrix(A)

print("Генераторная матрица G в систематическом виде:")
print(G)
print("Проверочная матрица H:")
print(H)