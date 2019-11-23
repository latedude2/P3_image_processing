import treys
from treys import Evaluator
from treys import Card

def evaluateCards(board, hand):
    board = [
        Card.new('Ah'),
        Card.new('Kd'),
        Card.new('Jc')
    ]
    hand = [
        Card.new('Qs'),
        Card.new('Qh')
    ]
    Card.print_pretty_cards(board + hand)

    evaluator = Evaluator()
    score = evaluator.evaluate(board, hand)
    handType = evaluator.get_rank_class(score)

    print("Player 1 hand rank = %d (%s)\n" % (score, evaluator.class_to_string(handType)))