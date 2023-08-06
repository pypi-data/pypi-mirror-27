''' This is my first module. It determines whether a given number is prime or not.
    It can also gives you the nearest prime number from given number.
    Version 1.0.1 includes a game in which you can guess wheter a number is prime or not'''

from random import randint

def is_prime(num):
	'''Checks that given number is prime or not. Returns a boolean value.'''
	for n in range(2, num // 2):
		if num % n is 0:
			return False
	return True

def nearest_prime(num):
	'''If given number is prime it returns itself otherwise calculates from top and bottom. '''
	if is_prime(num):
		return num
	up = down = num
	while True:
		down = down - 1
		if is_prime(down):
			return down
		up = up + 1
		if is_prime(up):
			return up

def game(name):
	'''Gives user a random number from 1, 100 and asks whether it is prime or not.'''
	print("Guide: Please type 'y' for yes and 'n' for no.")
	num = randint(1,100)
	user_input = input('Hello ' + name + '! Is '+ str(num) + ' a prime number? (y/n)\n')
	if user_input == 'y':
		if is_prime(num):
			print('Yes ' + name +'! ' + str(num) + ' is a prime number. Congratulations you WON.')
		else:
			print('No ' + name +'! '  + str(num) + ' is not a prime number. You LOST.')
	elif user_input == 'n':
		if not is_prime(num):
			print('Yes ' + name +'! '  + str(num) + ' is not a prime number. Congratulations you WON.')
		else:
			print('No ' + name +'! '  + str(num) + ' is a prime number. You LOST.')
	else:
		print("Error: Please type 'y' for yes and 'n' for no.")




