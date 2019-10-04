import card


class Deck:
    def __init__(self, symbols, cardsPerSymbol):
        self.symbols = symbols
        self.cardsPerSymbol = cardsPerSymbol

        for x in symbols:
            for y in cardsPerSymbol:
                card.Card(x, y)
