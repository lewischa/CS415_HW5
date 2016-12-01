'''
	CS415 Homework 5
	Problems 1-3

	Jeremy Olsen
	Carlos Downie
	Chad Lewis
'''

'''   PROBLEM 1 CODE - BEGIN   '''
# Create empty dictionary 'knapsack' and return it
def initializeEmptyKnapsack():
	knapsack = {}
	for i in range(1,11):
		newDict = {}
		newDict["weight"] = 0
		newDict["profit"] = 0
		knapsack[i] = newDict
	return knapsack

# Populate knapsack with data from HW5 prompt (in 'knapsack.txt')
def parseKnapsackFile(sack):
	lines = []
	with open( "knapsack.txt", "r" ) as file:
		for line in file:
			lines.append(line.strip('\n').split(' '))
	for line in lines:
		for i in range(len(line)):
			line[i] = eval(line[i])
	for each in lines:
		sack[each[0]]["weight"] = each[1]
		sack[each[0]]["profit"] = each[2]
	return sack

# Initialize the hash table (all 0's)
def initializeTable():
	k = []
	for i in range(11):
		new = []
		for w in range(76):
			new.append(0)
		k.append(new)
	return k

# Fill hash table and return maximum profit
def fillKnapsack(table, sack):
	for i in range(1, 11):
		for w in range(1, 76):
			itemWeight = sack[i]["weight"]
			profit = sack[i]["profit"]
			if itemWeight > w:
				table[i][w] = table[i - 1][w]
			else:
				table[i][w] = max(table[i - 1][w], table[i -1][w - itemWeight] + profit)
	return table[10][75]

# Top-level handler for problem 1
	# Get knapsack data
	# Initialize hash table
	# Fill hash table, print profit
def problem_1():
	print("KNAPSACK PROBLEM - DYNAMIC PROGRAMMING")
	knapsack = parseKnapsackFile( initializeEmptyKnapsack() )
	dynamicTable = initializeTable()
	result = fillKnapsack(dynamicTable, knapsack)
	print("The maximum profit for a knapsack of weight 75 is: {}\n".format(result))


'''   PROBLEM 1 CODE - END   '''






# Print the user's options
def printOptions():
	print("   Options")
	print("1. Problem 1")
	print("2. Problem 2")
	print("3. Problem 3\n")

# Get user option input
def getOption():
	option = input("Enter 1, 2, or 3 (-1 to quit): ")
	while (option != '1') and (option != '2') and (option != '3') and (option != '-1'):
		option = input("Please enter only 1, 2, or 3 (-1 to quit): ")
	return option

# Run option based on user input
def runOption(op):
	if op == '1':
		problem_1()
	elif op == '2':
		print("No code for Problem 2 yet.\n")
	elif op == '3':
		print("No code for Problem 3 yet.\n")
	elif op == '-1':
		print("All done. Exiting . . .")
		exit()
	else:
		print("Option not recognized.")

def main():
	print("****   Homework 5   ****\n")
	printOptions()
	while True:
		runOption( getOption() )
		printOptions()



if __name__ == "__main__":
	main()