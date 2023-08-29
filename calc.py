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
	return calculateDebracketedExpression(currCalcStr)

def calculateDebracketedExpression(calcStr):
	currCalcStr = calcStr[:]

	# following BIMDAS ordering, without brackets:

	# indices
	powerIndex = currCalcStr.find("^")
	while powerIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, powerIndex)
		prevNum = int(currCalcStr[prevNumStartIndex:powerIndex])
		nextNum = int(currCalcStr[powerIndex + 1:nextNumEndIndex + 1])
		calculatedExpression = prevNum ** nextNum
		currCalcStr = currCalcStr[:prevNumStartIndex] + str(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		powerIndex = currCalcStr.find("^")

	# multiplication and division
	multDivIndex = -1
	multIndex = currCalcStr.find("*")
	divIndex = currCalcStr.find("/")
	if multIndex == -1:
		multDivIndex = divIndex
	elif divIndex == -1:
		multDivIndex = multIndex
	else:
		multDivIndex = min(multIndex, divIndex)

	while multDivIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, multDivIndex)
		prevNum = int(currCalcStr[prevNumStartIndex:multDivIndex])
		nextNum = int(currCalcStr[multDivIndex + 1:nextNumEndIndex + 1])

		if currCalcStr[multDivIndex] == "*": 
			calculatedExpression = prevNum * nextNum
		else:
			calculatedExpression = prevNum // nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + str(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		multIndex = currCalcStr.find("*")
		divIndex = currCalcStr.find("/")
		if multIndex == -1:
			multDivIndex = divIndex
		elif divIndex == -1:
			multDivIndex = multIndex
		else:
			multDivIndex = min(multIndex, divIndex)

	# addition and subtraction
	addSubIndex = -1
	addIndex = currCalcStr.find("+")
	subIndex = currCalcStr.find("-")
	if addIndex == -1:
		addSubIndex = subIndex
	elif subIndex == -1:
		addSubIndex = addIndex
	else:
		addSubIndex = min(addIndex, subIndex)

	while addSubIndex != -1:
		prevNumStartIndex, nextNumEndIndex = getPrevAndNextNumIndices(currCalcStr, addSubIndex)
		prevNum = int(currCalcStr[prevNumStartIndex:addSubIndex])
		nextNum = int(currCalcStr[addSubIndex + 1:nextNumEndIndex + 1])

		if currCalcStr[addSubIndex] == "+": 
			calculatedExpression = prevNum + nextNum
		else:
			calculatedExpression = prevNum - nextNum

		currCalcStr = currCalcStr[:prevNumStartIndex] + str(calculatedExpression) + currCalcStr[nextNumEndIndex + 1:]

		addIndex = currCalcStr.find("+")
		subIndex = currCalcStr.find("-")
		if addIndex == -1:
			addSubIndex = subIndex
		elif subIndex == -1:
			addSubIndex = addIndex
		else:
			addSubIndex = min(addIndex, subIndex)

	return currCalcStr

def getPrevAndNextNumIndices(calcStr, operatorIndex):
	prevNumStartIndex = operatorIndex - 1
	while prevNumStartIndex >= 0:
		if not (calcStr[prevNumStartIndex].isnumeric() or calcStr[prevNumStartIndex] == "."):
			break

		prevNumStartIndex -= 1
	prevNumStartIndex += 1

	nextNumEndIndex = operatorIndex + 1
	while nextNumEndIndex < len(calcStr):
		if not (calcStr[nextNumEndIndex].isnumeric() or calcStr[nextNumEndIndex] == "."):
			break

		nextNumEndIndex += 1
	nextNumEndIndex -= 1

	return (prevNumStartIndex, nextNumEndIndex)