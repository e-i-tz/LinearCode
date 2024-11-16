from EncodeAndDecode import encode_message, find_all_invertible_submatrices, find_all_invertible_submatrices, \
    create_inverse_submatrices, multiply_inverse_matrices_with_G, get_codewords, find_error_vector, correct_codeword, \
    decode_codeword
from InputParametrs import get_code_parameters, validate_code_parameters, input_message, input_codeword
from GeneratorAndCheckMatrix import create_generator_matrix, create_parity_check_matrix

def main():
    # Получение параметров кода от пользователя
    n, k, d = get_code_parameters()

    # Проверка параметров кода
    try:
        if validate_code_parameters(n, k, d):
            print("Параметры кода удовлетворяют всем границам.")
    except ValueError as e:
        print(e)
        return

    # Создание генераторной и проверочной матриц
    G, A = create_generator_matrix(k, n, d)
    H = create_parity_check_matrix(A)

    print("Генераторная матрица G в систематическом виде:")
    print(G)
    print("Проверочная матрица H:")
    print(H)
    print("Построенный код может исправить одну ошибку.")

    while True:
        print("\nВыберите действие:")
        print("1. Закодировать сообщение")
        print("2. Декодировать кодовое слово")
        print("3. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            message = input_message(k)
            codeword = encode_message(message, G)
            print("Исходное сообщение:", message)
            print("Кодовое слово:", codeword)

        elif choice == '2':
            codeword = input_codeword(n)
            try:
                decoded_word, syndrome, corrected_word, error_vector = decode_codeword(codeword, H, G, k, n)
                print("Вектор ошибок:", error_vector)
                print("Исправленное слово:", corrected_word)
                print("Декодированное слово:", decoded_word)
                print("Синдром:", syndrome)
            except ValueError as e:
                print(e)

        elif choice == '3':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
