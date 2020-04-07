import random
import string


minimum_len = 8
specials = ' ð¶&|§"#ł«”.{“]€½;[¬_ŋ£/:ß@æ¢ŧ%=µđ³$(~¹»+²)?°¼*!←ø↓\\,^→-}ç`ñþħ`'
numbers = '0123456789'

def _compare(l1, l2):
	result = False
	for x in l1:
		for y in l2:
			if x == y:
				result = True
				return result                
	return result

def has_special_characters(string): 
	return _compare(string, specials)

def has_upper_and_lower(string):
	return not string.isupper() and not string.islower()

def has_minimum_length(string):
	return len(string) >= minimum_len

def is_alphanumeric(string):
	return _compare(string, numbers)

def verify_security_password(password, security_grade=4):
	
	if not type(password) == type(''):
		raise Exception()
		
	if not security_grade in [0,1,2,3,4]:
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

def generate_password(length=minimum_len*2):
	
	if length < minimum_len:
		raise Exception()

	if length % 4 == 0:
		div = int(length / 4)
		res = div
	else:
		div = int(length // 3)
		res = int(length % 3)

	def mix(string):
		string = [_ for _ in string]
		for i, j in enumerate(string):
			rand = random.randint(0,len(string))
			val = j
			string.pop(i)
			string.insert(rand, val)
		return ''.join(string)

	lower_letters = string.ascii_lowercase
	upper_letters = string.ascii_uppercase
	
	pswd = ''
	pswd += ''.join(random.choice(lower_letters) for i in range(div))
	pswd += ''.join(random.choice(upper_letters) for i in range(div))
	pswd += ''.join(random.choice(specials) for i in range(div))
	pswd += ''.join(random.choice(numbers) for i in range(res))

	return mix(pswd)

for _ in range(minimum_len, 180):
	p = generate_password(_)
	print(str(len(p)) + ": " + str(p))

print(generate_password())
