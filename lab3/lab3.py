import random

class Card:
    def __init__(self, suit, value):
        assert 1 <= suit <= 4 and 1 <= value <= 13
        self._suit = suit
        self._value = value

    def getValue(self):
        return int(self._value)

    def getSuit(self):
        return int(self._suit)

    def __str__(self):
        description = ""
        if (self._value == 1):
            description += "Ace"
        elif (self._value == 2):
            description += "Two"
        elif (self._value == 3):
            description += "Three"
        elif (self._value == 4):
            description += "Four"
        elif (self._value == 5):
            description += "Five"
        elif (self._value == 6):
            description += "Six"
        elif (self._value == 7):
            description += "Seven"
        elif (self._value == 8):
            description += "Eight"
        elif (self._value == 9):
            description += "Nine"
        elif (self._value == 10):
            description += "Ten"
        elif (self._value == 11):
            description += "Jack"
        elif (self._value == 12):
            description += "Queen"
        elif (self._value == 13):
            description += "King"

        if (self._suit == 1):
            description += " of Hearts"
        if (self._suit == 2):
            description += " of Diamonds"
        if (self._suit == 3):
            description += " of Clubs"
        if (self._suit == 4):
            description += " of Spades"
        return description
        
class CardDeck:
    def __init__(self):
        self.reset()
        
    def shuffle(self):
        random.shuffle(self._deck)
    def getCard(self):
        return self._deck.pop(0)
    def size(self):
        return len(self._deck)
    def reset(self):
        self._deck = []
        for num in range(1,14):
            for color in range(1,5):
                self._deck.append(Card(color, num))

deck = CardDeck()
deck.shuffle()

while deck.size() > 0:
    card = deck.getCard()
    print("Card {} has value {}".format(card, card.getValue()))

