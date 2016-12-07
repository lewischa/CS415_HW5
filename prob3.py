import random
import heapq

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


def Huffman(freqSet):

    n = len(freqSet)
    H = []
    G = {}

    for i in range(1,n+1):
        heapq.heappush(H,i)
    
    for k in range(n+1,2*n - 1):
        i = heapq.heappop(H)
        j = heapq.heappop(H)
        G[k] = {i ,j}
        freqSet.append(freqSet[i] + freqSet[j])
        heapq.heappush(H,k)

    return (H,G,freqSet)

def findFrequency(bitString,setSize):

    c_set = ""
    val = 0
    table = {}
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

    return table
        
