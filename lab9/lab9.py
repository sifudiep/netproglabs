import math, random, zlib

def partOne():
    txt = ""

    with open('exempeltext.txt', 'r') as extxt:
        for line in extxt:
            txt += line

    print(len(txt))

    byteArr = bytearray(txt, 'utf-8')

    print(len(byteArr))

    # Q : How many symbols does the string contain? How many bytes does the byte-array contain? Explain differences.
    # A : The string contains 29091 symbols and byteArr contains 30491 bytes.
    #     The reason byteArr contains those extra symbols is because it is encoded in UTF-8 and it contains the swedish symbols "ÄÅÖ",
    #     the swedish symbols take up more bytes(3 bytes) than regular ASCII symbols(1 byte) which results in it containing more bytes than the string has symbols. 

def makeHisto(byteArr):
    histogram = [0] * 256

    for byte in byteArr:
        histogram[int(byte)] += 1

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

def entropi(prob):
    total = 0
    for num in prob:
        if (num != 0):
            total += num*math.log(1/num, 2)

    return total

def partTwo():
    txt = ""

    with open('exempeltext.txt', 'r') as extxt:
        for line in extxt:
            txt += line

    print(len(txt))

    byteArr = bytearray(txt, 'utf-8')

    prob = makeProb(makeHisto(byteArr))
    bitsPerChar = entropi(prob)
    print((bitsPerChar * len(txt)) / 8)
    print(f"entropi : {bitsPerChar}")
    
    # Q : Down to how many bytes should it be possible to compress the byte-array byteArr if we treat it as a memory-free source 
    # (i.e.,we do not exploit statistical redundancy) but use an optimal encoding?

    # bitsPerChar = 4.594840697056228
    # Since length of txt is 29091, then total bits = 4.594840697056228 * 29091 = 133668.51071806275
    # 1 byte = 8 bit, which means 133668 bits = 16709 bytes (rounded up)
    # A : Should be possible to compress byteArr down to 16709 bytes!

def partThreeAndFour():
    txt = ""

    with open('exempeltext.txt', 'r') as extxt:
        for line in extxt:
            txt += line

    print(len(txt))

    byteArr = bytearray(txt, 'utf-8')
    theCopy = byteArr[0:-1]

    random.shuffle(theCopy)

    theCopyZip = zlib.compress(theCopy)

    # Q : How long is code measured in bits?
    # A : 19818 * 8 = 158 544 bits
    # Q : How many source symbols does theCopy contain?
    # A : len(txt) = 29091 symbols
    # Q : bits/symbol = 158 544 / 290 91 = 5,45 bits/symbol

    byteArrZip = zlib.compress(byteArr)
    print(len(byteArrZip))

    # Q : Repeat the above with the unshuffled byte-array byteArr. Down to how many bit/symbol can the zip-algorithm compress this array?
    # 128 48 bytes = 128 48 * 8 bits = 102 784 bits
    # A : 102 784 / 29091 = 3,53 bits / symbol

    # Q : Now you have three different numbers of bits/symbol: (a) the data source’s entropy, (b) the zlib-encoding of theCopy, and (c)the zlib-encoding of byteArr. 
    # Which one is the smallest number? Which one is the highest number? Explain why!
    # a) 4.6 bits / symbol, b) 5,45 bits / symbol, c) 3,53 bits / symbol
    # A : b) has the highest number, meaning it is the one that is the worst compressed one. 
    # Whilst c) has the lowest number, meaning it is the best compressed one. 
    # c) is lower than a) which suggests that c) is making use of source memory. 
    # Since a) should have the smallest theoretical value if no source memory exploitation is involved. 


def partFive():
    t1 = """I hope this lab never ends because
    it is so incredibly thrilling!"""
    t10 = t1*10

    t1ByteArr = bytearray(t1, 'utf-8')
    t10ByteArr = bytearray(t10, 'utf-8')

    t1Zip = zlib.compress(t1ByteArr)
    t10Zip = zlib.compress(t10ByteArr)

    # Q : Down to how many bytes can zlib compress the first and second string, respectively?
    # A : t1Zip - 70 bytes and t10Zip - 79 bytes

    # Q : The string t10 contains 10 times more symbols than t1, but is also its zip-code ten times longer than t1’s? Explain why/why not
    # A : The zip-code is not ten times larger since both t10 contains the same words that t1 has. Meaning it can encode the words instead of characters, 
    # since the words are repeating you don't need to allocate many more bytes than you'd use in t1.

partFive()