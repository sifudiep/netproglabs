import queue, math

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data
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
    for i in range(len(probDistribution)):
        if (probDistribution[i] != 0):
            pq.put(Node(prio=probDistribution[i], data=i))


    while (pq.qsize() > 1):
        left, right = pq.get(), pq.get()
        internalNode = Node(prio=(left.prio + right.prio), data=(left, right))
        pq.put(internalNode)

    # return the root of pq
    return pq.get()

def getAverageCodewordLength(node, binary):
    if (type(node.data) == int):
        return node.prio * len(binary) 
    else:
        right = getAverageCodewordLength(node.data[1], f"{binary}1")
        left = getAverageCodewordLength(node.data[0], f"{binary}0")
        return left + right


def fillDictWithHuffmanTreeValues(node, binary):
    global g_dict
    if (type(node.data) == int):
        g_dict[node.data] = {
            "ascii" : f"{chr(node.data)}" if (int(node.data) >= 32 and int(node.data) <= 127) else "",
            "binary" : binary,
            "binaryLength" : len(binary),
            "idealCodewordLength" :  round(math.log(1/node.prio, 2),2)
        } 
    else:
        #right path
        fillDictWithHuffmanTreeValues(node.data[1], f"{binary}1")
        #left path
        fillDictWithHuffmanTreeValues(node.data[0], f"{binary}0")

def printDict():
    global g_dict

    for i in range(0,255):
        if i in g_dict:
            noExtraSpaces = f"byte={i} <{g_dict[i]['ascii']}> {g_dict[i]['binary']}   len={g_dict[i]['binaryLength']} log(1/p)={g_dict[i]['idealCodewordLength']}"
            addedSpaces = (65 - len(noExtraSpaces)) * " "
            extraSpaces = f"byte={i} <{g_dict[i]['ascii']}> {g_dict[i]['binary']} {addedSpaces} len={g_dict[i]['binaryLength']} log(1/p)={g_dict[i]['idealCodewordLength']}"
            print(extraSpaces)
            
g_dict = {}

huffmanTreeRoot = createHuffmanTree()
print(getAverageCodewordLength(huffmanTreeRoot, ""))
fillDictWithHuffmanTreeValues(huffmanTreeRoot, "")
printDict()