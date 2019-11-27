import treys
from treys import Evaluator
from treys import Card
from treys import Deck

def decryptHand(string):
    # string sent should look like "h8s9"
    card = []
    card.append(string[1] + string[0]) # separate two cards and place them in needed positions
    card.append(string[3] + string[2])

    # makes the needed string to send
    stringToSend = evaluateHandCards(string[1].capitalize(), string[3].capitalize(), card[0], card[1])
    return stringToSend

# makes the needed string that should be sent
# suits are not needed, so only values of them sent (firstValue and secondValue)
# also both cards are sent as strings to me the combined string later
def evaluateHandCards(firstValue, secondValue, firstCard, secondCard):
    # firstValueIndex is the placement of the card's value according to the strength
    valueIndexes = firstValueIndex, secondValueIndex = (100, 100) #random can be given, so it could be seen if it's changed when searching
    i = 0 # used for searching
    if firstValue != secondValue:  # if both card values are not the same, following code is done

        for value in cardValue:  # checks through each element in the cardValue list, which is defined at the start
            if value == firstValue:
                firstValueIndex = i + 1
            if value == secondValue:
                secondValueIndex = i + 1

            # if values are already taken, compare them, compute the string and return it
            if firstValueIndex != 100 and secondValueIndex != 100:
                value = 7642 - (firstValueIndex * secondValueIndex)
                stringToSend = str("0 " + str(firstCard) + str(secondCard) + " " + str(value))
                return str(stringToSend)

    # if both cards are the same, there is a pair and another code is done
    if firstValue == secondValue:
        valueIndexes = firstValueIndex, secondValueIndex = (100, 100)
        for value in cardValue:
            if value == firstValue:
                firstValueIndex = i
                secondValueIndex = i
                # value = all possible combinations - rank of the strongest high card rank - mulitplication of two card strengths
                value = 7642 - 182 - (firstValueIndex * secondValueIndex)
                stringToSend = str("1 " + str(firstCard) + str(secondCard) + " " + str(value))
                return str(stringToSend)


def evaluateCards():
    deck = Deck()

    #For debugging
    board = deck.draw(5)
    hand = deck.draw(2)

    print(Card.print_pretty_cards(board + hand))

    evaluator = Evaluator()
    bestScore = evaluator.evaluate(board, hand)
    handType = evaluator.get_rank_class(bestScore)

    print("Player 1 hand rank = %d (%s)\n" % (bestScore, evaluator.class_to_string(handType)))


    for i in range(len(board) + len(hand)):
        # Make copy of hand and board
        tempHand = []
        tempBoard = []
        for j in range(len(hand)):
            tempHand.append(hand[j])
        for j in range(len(board)):
            tempBoard.append(board[j])

        #First try removing one of the hand cards
        if(i < 2):
            tempHand.pop(i)
            tempHand.append(board[0])
            tempBoard.pop(0)
        #Now we try removing board cards
        else:
            tempBoard.pop(i - 2)

        #Find the score
        score = evaluator.evaluate(tempBoard, tempHand)
        #If score is same as before, these cards have the best hand
        if(score == bestScore):
            # Make copy of best hand and board
            best6Hand = []
            best6Board = []
            for j in range(len(tempHand)):
                best6Hand.append(tempHand[j])
            for j in range(len(tempBoard)):
                best6Board.append(tempBoard[j])
            break

    print(Card.print_pretty_cards(best6Board + best6Hand))
    #we repeat the process to have the best 5 cards
    for i in range(len(best6Board) + len(best6Hand)):
        #Make copy of hand and board
        tempHand = []
        tempBoard = []
        for j in range(len(best6Hand)):
            tempHand.append(best6Hand[j])
        for j in range(len(best6Board)):
            tempBoard.append(best6Board[j])

        if (i < 2):
            tempHand.pop(i)
            tempHand.append(best6Board[0])
            tempBoard.pop(0)
        else:
            tempBoard.pop(i - 2)
        score = evaluator.evaluate(tempBoard, tempHand)
        if (score == bestScore):
            # Make copy of best hand and board
            best5Hand = []
            best5Board = []
            for j in range(len(tempHand)):
                best5Hand.append(tempHand[j])
            for j in range(len(tempBoard)):
                best5Board.append(tempBoard[j])
            break

    print(Card.print_pretty_cards(best5Board + best5Hand))

    card1 = convertCardToString(best5Board.__getitem__(0))
    card2 = convertCardToString(best5Board.__getitem__(1))
    card3 = convertCardToString(best5Board.__getitem__(2))
    card4 = convertCardToString(best5Board.__getitem__(0))
    card5 = convertCardToString(best5Board.__getitem__(1))

    handString = card1 + card2 + card3 + card4 + card5
    print(handString)

    stringToSend = str(handType) + " " + handString + " " + str(bestScore)

    return stringToSend

def convertCardToString(card):
    intSuit = Card.get_suit_int(card)  # Spade = 1, heart = 2, diamond = 4, club = 8
    intRank = Card.get_rank_int(card)  # 2 = 0, 3 = 1, 4 = 2, 5 = 3, 6 = 4, 7 = 5, 8 = 6,... J = 9, ... A = 12

    cardString = ""
    if (intRank < 8):
        cardString = str(intRank + 2)
    elif(intRank == 8):
        cardString = "T"
    elif (intRank == 9):
        cardString = "J"
    elif (intRank == 10):
        cardString = "Q"
    elif (intRank == 11):
        cardString = "K"
    elif (intRank == 12):
        cardString = "A"
    else:
        raise Exception('intRank should not exceed 12. The value of intRank was: {}'.format(intRank))

    if(intSuit == 1):
        cardString = cardString + "s"
    elif(intSuit == 2):
        cardString = cardString + "h"
    elif (intSuit == 4):
        cardString = cardString + "d"
    elif (intSuit == 8):
        cardString = cardString + "c"
    else:
        raise Exception('intSuit bad. The value of intSuit was: {}'.format(intSuit))

    return cardString
