# WARNING
# Install the module before run this file.

import sys
import casket


def main():

	length = int(input("Insert lentgh of yout password (minimum 8): "))

	if length < 8:
		raise Exception('Invalid parameter.')

	special_characters = bool(input("The password must have special characters? (True/False): "))

	if not special_characters in [True, False]:
		raise Exception('Invalid parameter.')

	upper_letters = bool(input("The password must have upper letters? (True/False): "))

	if not upper_letters in [True, False]:
		raise Exception('Invalid parameter.')

	lower_letters = bool(input("The password must have lower letters? (True/False): "))

	if not lower_letters in [True, False]:
		raise Exception('Invalid parameter.')

	digits = bool(input("The password must have numbers? (True/False): "))

	if not digits in [True, False]:
		raise Exception('Invalid parameter.')

	password = casket.generate_password(length, special_characters,
				upper_letters, lower_letters, digits)

	print("Your password is \'%s\'" % (password))

	if casket.verify_security_password(password):
		print("\'verify_security_password()\' returned \'True\'")
	else:
		print("\'verify_security_password()\' returned \'False\'")

if __name__ == '__main__':
	sys.exit(main())


