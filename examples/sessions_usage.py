# WARNING
# Install the module before run this file.

import sys
import casket

def main():
	name = input("Insert your name: ")
	password = input("Insert your master password: ")
	email = input("Insert your email: ")
	try:
		session = casket.new_session(name, password, email)
	except casket.unable_to_open_session_exception:
		a = input("Oh oh. Seems like this session name already exist. \n Do you want to load it? (yes/no): ")
		if a == 'yes':
			session = casket.load_session(name, password)
		else:
			exit()
	account = casket.account(input("Insert an account name: "), input("Insert the password: "), input("Insert the email: "))
	print(casket.crypto.list_algorithms())
	algo = input("Insert the algorithm you wanna use for this account (none for default): ")
	if algo == '':
		session.new_account(account)
	else:
		session.new_account(account, algo)
	print("Well! You added your first acount.")
	print(session.accounts)
	print("These are your data encrypted.")
	print(session.decrypt_accounts())
	print("These are your data unencrypted. Casket store safely the encrypted data in the casket folder.")

if __name__ == '__main__':
	sys.exit(main())


