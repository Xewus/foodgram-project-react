import pytest
from backend.core.validators import OneOfTwoValidator, MinLenValidator, hex_color_validator
from django.core.exceptions import ValidationError

correct_words = ('Алёша', 'Artur')
invalid_words = ('Алёшаtur', 'Иван 3', 'Ro.Bot')
too_short_words = ('', '1', '22')


@pytest.mark.validators
@pytest.mark.parametrize('word', correct_words)
def test_one_of_two_correct(word):
    assert OneOfTwoValidator()(word) is None


@pytest.mark.validators
@pytest.mark.parametrize('word', invalid_words)
def test_one_of_two_invalid(word):
    pytest.raises(ValidationError, OneOfTwoValidator(), word)


@pytest.mark.validators
@pytest.mark.parametrize('word', correct_words)
def test_min_len_correct(word):
    assert MinLenValidator(3)(word) is None


@pytest.mark.validators
@pytest.mark.parametrize('word', too_short_words)
def test_min_len_invalid(word):
    pytest.raises(ValidationError, MinLenValidator(3), word)


@pytest.mark.validators
def test_color_correct():
    assert hex_color_validator('123') == '#112233'
    assert hex_color_validator('aBc') == '#AABBCC'
    assert hex_color_validator('0a2B3c') == '#0A2B3C'

######################################################################
invalid_colors = ('1', '12', '1234', '1234567', 'a', '12g', '12a12af')


@pytest.mark.validators
@pytest.mark.parametrize('color', invalid_colors)
def test_color_invalid(color):
    pytest.raises(ValidationError, hex_color_validator, color)
