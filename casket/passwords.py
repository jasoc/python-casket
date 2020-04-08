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


minimum_len = 8
specials_characters_arr = '!\"\'\\#$%&()*+,-./:;<=>?@[]^_` {|}~'
numbers_arr = string.digits
lower_letters_arr = string.ascii_lowercase
upper_letters_arr = string.ascii_uppercase


def _compare(l1, l2):
    result = False
    for x in l1:
        for y in l2:
            if x == y:
                result = True
                return result
    return result


def has_special_characters(string):
    return _compare(string, specials_characters_arr)


def has_upper_and_lower(string):
    return not string.isupper() and not string.islower()


def has_minimum_length(string):
    return len(string) >= minimum_len


def is_alphanumeric(string):
    return _compare(string, numbers_arr)


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
    if not type(password) == type(''):
        raise Exception()

    if not security_grade in [0, 1, 2, 3, 4]:
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


def generate_password(length=minimum_len*2, special_characters=True,
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
	if length < minimum_len:
		raise Exception()

	def mix(string):
		string = [_ for _ in string]
		for i, j in enumerate(string):
			rand = random.randint(0, len(string))
			string.pop(i)
			string.insert(rand, j)
		return ''.join(string)
	
	arr_chars = []
	cnt = 0

	if special_characters:
		arr_chars.append(specials_characters_arr)
		cnt += 1
	if upper_letters:
		arr_chars.append(upper_letters_arr)
		cnt += 1
	if lower_letters:
		arr_chars.append(lower_letters_arr)
		cnt += 1
	if digits:
		arr_chars.append(numbers_arr)
		cnt += 1

	pswd = ''
	for _ in range(cnt):
		pswd += random.choice(arr_chars[_])
	for _ in range(length - cnt):
		pswd += random.choice(random.choice(arr_chars))

	return mix(pswd)
