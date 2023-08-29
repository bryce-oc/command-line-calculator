def calculateExpressionSafe(calcStr):
	if checkValid(calcStr):
		return calculateExpression(calcStr)
	else:
		return "Expression invalid."

def checkValid(calcStr):
	# TODO: implement checking
	return True

def calculateExpression(calcStr):
	# following BIMDAS ordering, parse bracketed expressions first
	currCalcStr = calcStr[:]
	while "(" in currCalcStr:
		startIndex = 0
		endIndex = 0
		i = 0
		while i < len(calcStr):
			if currCalcStr[i] == "(":
				startIndex = i
			elif currCalcStr[i] == ")":
				endIndex = i
				break
			i += 1
		insideBrackets = currCalcStr[startIndex + 1:endIndex]
		bracketsResult = calculateDebracketedExpression(insideBrackets)
		currCalcStr = currCalcStr[:startIndex] + bracketsResult + currCalcStr[endIndex + 1:]

	# now that brackets are removed, parse remaining expression
	currCalcStr = calculateDebracketedExpression(currCalcStr)
	if len(currCalcStr) > 0:
		if currCalcStr[0] == "n":
			return "-" + currCalcStr[1:]
			
	return currCalcStr

def calculateDebracketedExpression(calcStr):
	currCalcStr = calcStr[:]

	# following BIMDAS ordering, without brackets:

	# indices
	powerIndex = currCalcStr.find("^")
	while powerIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, powerIndex)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:powerIndex])
		nextNum = convertStrToNum(currCalcStr[powerIndex + 1:nextNumEndIndex + 1])
		calculatedExpression = prevNum ** nextNum
		currCalcStr = currCalcStr[:prevNumStartIndex] + convertNumToStr(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		powerIndex = currCalcStr.find("^")

	# multiplication and division
	multDivIndex = getEarliestOperator(currCalcStr, "*", "/")

	while multDivIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, multDivIndex)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:multDivIndex])
		nextNum = convertStrToNum(currCalcStr[multDivIndex + 1:nextNumEndIndex + 1])

		if currCalcStr[multDivIndex] == "*": 
			calculatedExpression = prevNum * nextNum
		else:
			calculatedExpression = prevNum // nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + convertNumToStr(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		multDivIndex = getEarliestOperator(currCalcStr, "*", "/")

	# addition and subtraction
	addSubIndex = getEarliestOperator(currCalcStr, "+", "-")

	while addSubIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, addSubIndex)
		prevNum = convertStrToNum(currCalcStr[prevNumStartIndex:addSubIndex])
		nextNum = convertStrToNum(currCalcStr[addSubIndex + 1:nextNumEndIndex + 1])

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

def getPrevAndNextNumIndices(calcStr, operatorIndex):
	prevNumStartIndex = operatorIndex - 1
	foundStart = False
	while prevNumStartIndex >= 0 and not foundStart:
		if not (calcStr[prevNumStartIndex].isnumeric() or calcStr[prevNumStartIndex] == "." or calcStr[prevNumStartIndex] == "n"):
			foundStart = True
		else:
			prevNumStartIndex -= 1
	prevNumStartIndex += 1

	nextNumEndIndex = operatorIndex + 1
	foundEnd = False
	while nextNumEndIndex < len(calcStr) and not foundEnd:
		if not (calcStr[nextNumEndIndex].isnumeric() or calcStr[nextNumEndIndex] == "." or calcStr[nextNumEndIndex] == "n"):
			foundEnd = True
		else:
			nextNumEndIndex += 1
	nextNumEndIndex -= 1

	return (prevNumStartIndex, nextNumEndIndex)

def convertNumToStr(num):
	if num >= 0:
		return str(num)
	else:
		return "n" + str(num * (-1))

def convertStrToNum(string):
	if string[0] == "n":
		return int(string[1:]) * (-1)
	else:
		return int(string)