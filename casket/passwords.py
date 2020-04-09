# -*- coding: utf-8 -*-
# Casket python module
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
passwords.py

Set of functions for elaborate passwords, generate randomic ones
and check the security level.
"""

import random
import string

MINIMUM_LENGTH = 8
SPECIALS_CHARACTERS_ARR = '!\"\'\\#$%&()*+,-./:;<=>?@[]^_` {|}~'
NUMBERS_ARR = string.digits
LOWER_LETTERS_ARR = string.ascii_lowercase
UPPER_LETTERS_ARR = string.ascii_uppercase


def _compare(list_1, list_2):
    result = False
    for _ in list_1:
        for __ in list_2:
            if _ == __:
                return True
    return result


def has_special_characters(value):
    return _compare(value, SPECIALS_CHARACTERS_ARR)


def has_upper_and_lower(value):
    return not value.isupper() and not value.islower()


def has_minimum_length(value):
    return len(value) >= MINIMUM_LENGTH


def is_alphanumeric(value):
    return _compare(value, NUMBERS_ARR)


def verify_security_password(password, security_grade=4):
    """Verify if the given password match the security requirements
       according with the passed security grade.
    Args:
        password (str):       The password to check.
        security_grade (int): Grade of security that the password
                              must have for the function to return True.
                              Accepted grades:
                               - 0: Every passwords accepted.
                               - 1: Only minimum length check.
                               - 0: Check if is alphanumeric.
                               - 0: Check if contain both lower and upper characters.
                               - 0: Check if contain special characters.
    Returns: (bool)
    """
    if not password.isistance('string'):
        raise Exception()

    if security_grade not in [0, 1, 2, 3, 4]:
        raise Exception()

    checkers_arr = [
        has_minimum_length,
        is_alphanumeric,
        has_upper_and_lower,
        has_special_characters]

    flag = True
    for _ in range(security_grade):
        if not checkers_arr[_](password):
            flag = False

    return flag


def generate_password(length=MINIMUM_LENGTH*2, special_characters=True,
                      upper_letters=True, lower_letters=True, digits=True):
    """generate and return randomic password according to passed
       optional parameters.
    Args:
            length (int):              The length the returned password will have.
            special_characters (bool): If the password must have special characters.
            upper_letters (bool):      If the password must have upper letters.
            lower_letters (bool):      If the password must have lower letters.
            digits (bool):             If the password must have numbers.

    Returns: (str)
    """
    if length < MINIMUM_LENGTH:
        raise Exception()

    def mix(value):
        value = [_ for _ in value]
        for i, j in enumerate(value):
            rand = random.randint(0, len(value))
            value.pop(i)
            value.insert(rand, j)
        return ''.join(string)

    arr_chars = []
    cnt = 0

    if special_characters:
        arr_chars.append(SPECIALS_CHARACTERS_ARR)
        cnt += 1
    if upper_letters:
        arr_chars.append(UPPER_LETTERS_ARR)
        cnt += 1
    if lower_letters:
        arr_chars.append(LOWER_LETTERS_ARR)
        cnt += 1
    if digits:
        arr_chars.append(NUMBERS_ARR)
        cnt += 1

    pswd = ''
    for _ in range(cnt):
        pswd += random.choice(arr_chars[_])
    for _ in range(length - cnt):
        pswd += random.choice(random.choice(arr_chars))

    return mix(pswd)
