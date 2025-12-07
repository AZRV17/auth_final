import pytest
from utils.password_generator import generate_password


@pytest.mark.parametrize(
    'length, expected',
    [
        (8, 8),
        (10, 10),
        (3, 3)
    ]
)
def test_generate_password_length_int_success(length, expected):
    assert len(generate_password(length)) == expected


def test_generate_password_length_nan_success():
    expected = 8

    result = len(generate_password())

    assert expected == result


def test_generate_password_contains_letters_and_digits_success():
    password = generate_password(20)

    has_letter = any(ch.isalpha() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)

    assert has_letter and has_digit
