''' This is my first module. It determines whether a given number is prime or not.
    It can also gives you the nearest prime number from given number.'''

def is_prime(num):
	for n in range(2, num // 2):
		if num % n is 0:
			return False
	return True

def nearest_prime(num):
	'''If given number is prime it returns itself otherwise calculates from top and bottom. '''
	if isprime(num):
		return num
	up = down = num
	while True:
		down = down - 1
		if isprime(down):
			return down
		up = up + 1
		if isprime(up):
			return up
