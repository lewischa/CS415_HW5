'''
	CS415 Homework 5
	Problems 1-3

	Jeremy Olsen
	Carlos Downie
	Chad Lewis
'''

import random
import heapq
from heapq import heappush, heappop, heapify



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




'''   PROBLEM 3 CODE - BEGIN   '''

#Performs a test suite of different compression settings and prints out
#a table of the resulting compression values.
def performSetTests():
    P_values = [50, 60, 70, 80, 90]
    Lengths = [1000, 100000]
    Set_bits = [2, 4, 6, 8, 10]

    performTests(P_values,Lengths,Set_bits)

#Performs shorter simplified test of 100000 length strings
#with 0-bit probabilities ranging from 50-90%
#A set size of 5-bits is used because testing has shown
#that to be a sweet spot for best compression of 100000 length strings
def finalTests():
    P_values = [50, 60, 70, 80, 90]
    performTests(P_values,[100000],[5])

#Length: number of bits the string contains
#Zero_prob: The probability of a bit being 0. (0-100)
def makeBinaryString(length,zero_prob):

    random.seed()
    bit_string = ""
    num = 0
    zero_prob /= 100

    for i in range(0,length):
        num = random.random()

        if num <= zero_prob:
            bit_string += "0"
        else:
            bit_string += "1"
    
    return bit_string

#Compresses a binary string using Huffman encoding
#Returns a compressed binary string (with encoding table
#also encoded)
def compress(string,setSize):
    E = encode(freqList(string,setSize))

    Output = compressEncoding(E)
    
    c_set = ""
    code = ""
    while len(string) > setSize:
        c_set = string[0:setSize]
        string = string[setSize:]

        code = getCode(c_set,E)
        Output += code

    code = getCode(string,E)
    Output += code

    return Output

#Takes a compressed binary string and decompresses it
def uncompress(string):

    code = ""
    value = ""
    output = ""

    #Read out the encoding table
    E = decodeEncoding(string)

    string = E[1]#Get remaining compressed file

    while len(string) > 0:
        code += string[0]
        string = string[1:]

        value = getValue(code,E[0])
        
        if value is not None:
            output += value
            code = ""

    return output

#Takes the frequency list and creates a Huffman encoding list
def encode(freqList):
    heap = freqList
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

#Converts an encoding entry to binary for decoding later
def compressNode(entry):

    value = entry[0]
    code = entry[1]
    encoded = ""
    
    while len(value) > 0:
        if value[0] == "0":
            encoded += "0"
        else:
            encoded += "10"
        value = value[1:]

    encoded += "110"

    while len(code) > 0:
        if code[0] == "0":
            encoded += "0"
        else:
            encoded += "10"
        code = code[1:]

    return encoded

#Converts encoded entries
def compressEncoding(encoding):

    encoded = ""

    for entry in encoding:
        encoded += compressNode(entry) + "110"

    return encoded + "1110"

#Reads in a string and outputs and entry
def decodeEntry(encoded):

    value = ""
    while len(encoded) > 0:
        if encoded[0] == "0":
            value += "0"
            encoded = encoded[1:]
        elif encoded[0] == "1":
            if encoded[1] == "0":
                value += "1"
                encoded = encoded[2:]
            else:
                encoded = encoded[3:]
                break

    return (value, encoded)

#Creates an encoding tree based on the encoded string
def decodeEncoding(encoding):

    encoded = []
    entry = []
    value = ""
    code = ""

    while len(encoding) > 0:

        #End of header reached
        if encoding[0:4] == "1110":
            encoding = encoding[4:]
            break
        
        entry = decodeEntry(encoding)
        value = entry[0]
        encoding = entry[1]
        
        entry = decodeEntry(encoding)
        code = entry[0]
        encoding = entry[1]
        
        encoded.append([value,code])
        
    return (encoded, encoding)

#Takes a string and find's it's associated code
def getCode(string,encoding):

    for code in encoding:
        if string == code[0]:
            return code[1]

    return "String not found in encoding tree!"

#Takes a code and finds it's associated string
def getValue(code,encoding):
    for val in encoding:
        if code == val[1]:
            return val[0]

    return None

#Takes a binary string and splits it into sets
#then counts each set's frequency.
#Returns the frequency list
def freqList(bitString,setSize):

    c_set = ""
    val = 0
    table = {}
    freq = []
    while len(bitString) > setSize:
        c_set = bitString[0:setSize]
        bitString = bitString[setSize:]
        val = table.get(c_set)
        if val != None:
            table[c_set] = val + 1
        else:
            table[c_set] = 1

    val = table.get(bitString)
    if val != None:
        table[bitString] = table.get(bitString) + 1
    else:
        table[bitString] = 1

    for key in table:        
        freq.append([table[key],[key,'']])

    return freq
        

#Performs compression of a random binary string and returns the
#compression ratio.
#length: The length of the binary string
#zeros: The percentage of zeros (0-100) in the binary string
#set_size: The number of bits per set when performing compression
def compareCompression(string, set_size):
    C = compress(string, set_size)
    L = len(S)
    LC = len(C)
    R = LC/L

    return "Set size: {0} bits; Original string length: {1}; Compressed length: {2}; Ratio: {3}".format(set_size,L,LC,R)


#Perform repeated tests using specified settings
def performTests(P_values,Lengths,Set_bits):
    
    print("Compression Variables and Results:\n")
    
    for L in Lengths:

        print("----Test results on binary string of length: {0}----\n".format(L)) 

        for S in Set_bits:
            print("\nSet bit length: {0}".format(S))
            print("0-bit Percentage | Compression Ratio\n")
            
            for P in P_values:

                binS = makeBinaryString(L,P)
                C = compress(binS,S)
                D = uncompress(C)
                # comp = (len(binS)/len(C))
                comp = (len(C)/len(D))

                print("{:13d}%   |  {:9f}  ".format(P,comp))

    print("End of test results.\n")

'''   PROBLEM 3 CODE - END   '''



# Print the user's options
def printOptions():
	print("   Options")
	print("1. Problem 1")
	print("2. Problem 3\n")

# Get user option input
def getOption():
	option = input("Enter 1, 2, or 3 (-1 to quit): ")
	while (option != '1') and (option != '2') and (option != '-1'):
		option = input("Please enter only 1 or 2 (-1 to quit): ")
	return option

# Run option based on user input
def runOption(op):
	if op == '1':
		problem_1()
	elif op == '2':
		finalTests()
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