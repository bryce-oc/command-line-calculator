from calc import *
from sys import argv

## TODO: add in command line interface

def main():
	preciseMode = True
	if "-p" in argv or "--precise" in argv:
		preciseMode = True
	elif "-i" in argv or "--imprecise" in argv:
		preciseMode = False

	if preciseMode:
		print("Running in precise mode. Nonintegers will be truncated.")
	else:
		print("Running in imprecise mode. Nonintegers will not be \
truncated, and all values will be stored as floats.")

	calcStr = input("> ")
	while calcStr.strip() != "":
		print(calculateExpressionSafe(calcStr, preciseMode))
		calcStr = input("> ")

if __name__ == '__main__':
	main()