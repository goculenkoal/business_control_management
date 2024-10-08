import secrets


def generate_code(length: int = 6) -> int:
    """Генерирует целочисленный проверочный код заданной длины.

    :param length: Длина проверочного кода (по умолчанию 6 символов)
    :return: Сгенерированный проверочный код в виде целого числа
    """
    # Максимальное значение для кода (например, для 6-значного кода - 999999)
    max_value = 10 ** length - 1
    min_value = 10 ** (length - 1)  # Минимальное значение (например, для 6-значного кода - 100000)

    # Генерация случайного кода в заданном диапазоне
    return secrets.randbelow(max_value - min_value + 1) + min_value
