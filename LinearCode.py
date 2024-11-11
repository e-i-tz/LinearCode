from InputParametrs import get_code_parameters, validate_code_parameters

n, k, d = get_code_parameters()

try:
    if validate_code_parameters(n, k, d):
        print("Параметры кода удовлетворяют всем границам.")
except ValueError as e:
    print(e)

