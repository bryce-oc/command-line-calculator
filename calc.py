from math import floor

def calculateExpressionSafe(calcStr, preciseMode=True):
	if checkValid(calcStr):
		return calculateExpression(calcStr, preciseMode)
	else:
		return "Expression invalid."

def checkValid(calcStr):
	# TODO: implement checking
	return True

def calculateExpression(calcStr, preciseMode):
	# following BIMDAS ordering, parse bracketed expressions first
	currCalcStr = calcStr[:]
	while "(" in currCalcStr:
		startIndex = -1
		endIndex = -1
		i = 0
		while i < len(currCalcStr) and endIndex == -1:
			if currCalcStr[i] == "(":
				startIndex = i
			elif currCalcStr[i] == ")":
				endIndex = i
			i += 1
		insideBrackets = currCalcStr[startIndex + 1:endIndex]
		bracketsResult = calculateDebracketedExpression(insideBrackets, preciseMode)
		#print(insideBrackets, "\t\t", bracketsResult)
		currCalcStr = currCalcStr[:startIndex] + bracketsResult + currCalcStr[endIndex + 1:]

	print("all brackets removed", flush=True)

	# now that brackets are removed, parse remaining expression
	currCalcStr = calculateDebracketedExpression(currCalcStr, preciseMode)
	if len(currCalcStr) > 0:
		if currCalcStr[0] == "n":
			return "-" + currCalcStr[1:]

	return currCalcStr

def calculateDebracketedExpression(calcStr, preciseMode):
	currCalcStr = calcStr[:]

	# following BIMDAS ordering, without brackets:

	# indices
	powerIndex = currCalcStr.find("^")
	while powerIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, powerIndex, preciseMode)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:powerIndex], preciseMode)
		nextNum = convertStrToNum(currCalcStr[powerIndex + 1:nextNumEndIndex + 1], preciseMode)
		
		if preciseMode:
			calculatedExpression = floor(prevNum ** nextNum)
		else:
			calculatedExpression = prevNum ** nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + convertNumToStr(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		powerIndex = currCalcStr.find("^")

	# multiplication and division
	multDivIndex = getEarliestOperator(currCalcStr, "*", "/")

	while multDivIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, multDivIndex, preciseMode)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:multDivIndex], preciseMode)
		nextNum = convertStrToNum(currCalcStr[multDivIndex + 1:nextNumEndIndex + 1], preciseMode)

		if currCalcStr[multDivIndex] == "*": 
			calculatedExpression = prevNum * nextNum
		else:
			if preciseMode:
				calculatedExpression = prevNum // nextNum
			else:
				calculatedExpression = prevNum / nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + convertNumToStr(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		multDivIndex = getEarliestOperator(currCalcStr, "*", "/")

	# addition and subtraction
	addSubIndex = getEarliestOperator(currCalcStr, "+", "-")

	while addSubIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, addSubIndex, preciseMode)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:addSubIndex], preciseMode)
		nextNum = convertStrToNum(currCalcStr[addSubIndex + 1:nextNumEndIndex + 1], preciseMode)

		if currCalcStr[addSubIndex] == "+": 
			calculatedExpression = prevNum + nextNum
		else:
			calculatedExpression = prevNum - nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + convertNumToStr(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		addSubIndex = getEarliestOperator(currCalcStr, "+", "-")

	return currCalcStr

'''
This function finds the earliest index of either of the two operators in the given string.
Returns -1 if neither operator is found in the string.
'''
def getEarliestOperator(calcStr, operator1, operator2):
	bothOpsIndex = -1
	op1Index = calcStr.find(operator1)
	op2Index = calcStr.find(operator2)
	if op1Index == -1:
		bothOpsIndex = op2Index
	elif op2Index == -1:
		bothOpsIndex = op1Index
	else:
		bothOpsIndex = min(op1Index, op2Index)

	return bothOpsIndex

def getPrevAndNextNumIndices(calcStr, operatorIndex, preciseMode):
	prevNumStartIndex = operatorIndex - 1
	foundStart = False
	while prevNumStartIndex >= 0 and not foundStart:
		if not (calcStr[prevNumStartIndex].isnumeric() or calcStr[prevNumStartIndex] == "n" or (calcStr[prevNumStartIndex] == "." and not preciseMode)):
			foundStart = True
		else:
			prevNumStartIndex -= 1
	prevNumStartIndex += 1

	nextNumEndIndex = operatorIndex + 1
	foundEnd = False
	while nextNumEndIndex < len(calcStr) and not foundEnd:
		if not (calcStr[nextNumEndIndex].isnumeric() or calcStr[nextNumEndIndex] == "n" or (calcStr[nextNumEndIndex] == "." and not preciseMode)):
			foundEnd = True
		else:
			nextNumEndIndex += 1
	nextNumEndIndex -= 1

	print(prevNumStartIndex, nextNumEndIndex)
	print(calcStr)
	print(calcStr[prevNumStartIndex:nextNumEndIndex+1])

	return (prevNumStartIndex, nextNumEndIndex)

def convertNumToStr(num):
	if num >= 0:
		return str(num)
	else:
		return "n" + str(num * (-1))

def convertStrToNum(string, preciseMode):
	if preciseMode:
		if string[0] == "n":
			return int(string[1:]) * (-1)
		else:
			return int(string)
	else:
		if string[0] == "n":
			return float(string[1:]) * (-1)
		else:
			return float(string) 