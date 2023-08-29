from calc import *

## TODO: add in command line interface

def main():
	calcStr = "0"
	while calcStr != "":
		calcStr = input("> ")
		print(calculateExpressionSafe(calcStr))

if __name__ == '__main__':
	main()