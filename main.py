from calc import *

## TODO: add in command line interface

def main():
	calcStr = input("> ")
	while calcStr != "":
		print(calculateExpressionSafe(calcStr))
		calcStr = input("> ")

if __name__ == '__main__':
	main()