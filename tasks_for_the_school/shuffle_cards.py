import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])


class Deck:
    def __init__(self):
        self.suits = ['♥', '♦', '♣', '♠']
        self.ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return '\n'.join(f"{i}. {card.rank}{card.suit}" for i, card in enumerate(self.cards, 1))


if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    print("Перемешанная колода:")
    print(deck)