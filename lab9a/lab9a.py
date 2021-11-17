import queue

def printAndPop(pq):
    while (pq.qsize() > 0):
        print(pq.get())


def test1():
    print("running test 1")

    pq = queue.PriorityQueue()
    # pq.put( (4.0, 10) )
    # pq.put( (2.0, 8) )
    # pq.put( (5.0, 2) )
    # pq.put( (1.5, 8) )
    # pq.put( (4.0, 8) )
    # pq.put( (1.0, 8) )


    # pq.put( (3.0, (1,2)) )

    # Explain why it crashes now, but did not before:
    # pq.put( (2.0, (1,2)) )
    # The code above crashes the program since 2.0 is already inside the priority queue, meaning the priority queue has to check which of the two 2.0s has the higher priority.
    # since the first one has the integer 8 and the second one has a tuple, they cannot be compared. 

    pq.put(Node(4.0, 10))
    pq.put(Node(2.0, 8))
    pq.put(Node(5.0, 2))
    pq.put(Node(1.5, 8))
    pq.put(Node(4.0, 8))
    pq.put(Node(1.0, 8))
    pq.put(Node(3.0, (1,2)))

    printAndPop(pq)

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data
    def __lt__(self, other):
        return self.prio<other.prio
    def __str__(self):
        return f"({self.prio}, {self.data})"


test1()