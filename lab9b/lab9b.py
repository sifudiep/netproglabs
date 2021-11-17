import queue, math

class Node:
    def __init__(self, prio, data, char):
        self.prio = prio
        self.data = data
        self.char = char
    def __lt__(self, other):
        return self.prio<other.prio
    def __str__(self):
        return f"({self.prio}, {self.data})"

def makeHisto(byteArr):
    histogram = [0] * 256

    for byte in byteArr:
        histogram[byte] += 1

    return histogram

def makeProb(histo):
    probDistrubution = [0] * 256
    total = 0
    for num in histo:
        total += num

    index = 0
    for num in histo:
        probDistrubution[index] = num / total
        index += 1

    return probDistrubution

def printAndPop(pq):
    while (pq.qsize() > 0):
        print(pq.get())

def createHuffmanTree():
    txt = ""
    with open('exempeltext.txt', 'r') as extxt:
        for line in extxt:
            txt += line
    byteArr = bytearray(txt, 'utf-8')

    probDistribution = makeProb(makeHisto(byteArr))

    pq = queue.PriorityQueue()
    counter = 0
    for i in range(len(probDistribution)):
        if (probDistribution[i] != 0):
            pq.put(Node(prio=probDistribution[i], data=counter, char=i))
            counter += 1

    while (pq.qsize() > 1):
        left, right = pq.get(), pq.get()
        internalNode = Node((left.prio + right.prio), (left, right), char=None)
        pq.put(internalNode)

    # return the root of pq
    return pq.get()

def getAverageCodewordLength(node):
    if (type(node.data) == int):
        # print(f"node.data: {node.data} , binary: {bin(node.data)[2:]}")
        return node.prio * len(str(bin(node.data)[2:])) 
    else:
        if (len(node.data) == 2):
            left = getAverageCodewordLength(node.data[0])
            right = getAverageCodewordLength(node.data[1])
            return left + right
        elif (len(node.data) == 1):
            return getAverageCodewordLength(node.data[0])

def fillDictWithHuffmanTreeValues(node):
    global g_dict
    if (type(node.data) == int):
        g_dict[node.char] = {
            "ascii" : f"{chr(node.char)}" if (int(node.char) >= 32 and int(node.char) <= 127) else "",
            "binary" : bin(node.char)[2:],
            "binaryLength" : len(str(bin(node.char)[2:])),
            "idealCodewordLength" :  math.log(1/node.prio, 2)
        } 
    else:
        if (len(node.data) == 2):
            #left path
            fillDictWithHuffmanTreeValues(node.data[0])
            #right path
            fillDictWithHuffmanTreeValues(node.data[1])
        elif (len(node.data) == 1):
            fillDictWithHuffmanTreeValues(node.data[0])

def printDict():
    global g_dict

    for i in range(0,255):
        if i in g_dict:
            print(f"byte={i} <{g_dict[i]['ascii']}> {g_dict[i]['binary']}   len={g_dict[i]['binaryLength']} log(1/p)={g_dict[i]['idealCodewordLength']}")

g_dict = {}

huffmanTreeRoot = createHuffmanTree()
print(getAverageCodewordLength(huffmanTreeRoot))
fillDictWithHuffmanTreeValues(huffmanTreeRoot)
printDict()