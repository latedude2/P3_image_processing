import treys
from treys import Evaluator
from treys import Card
from treys import Deck

# needed for the strength of each card to define later
cardValue = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cardSuit = ["h", "d", "s", "c"]

"""
INFORMATION ABOUT COMBINATIONS:

    Number of Distinct Hand Values:
    Straight Flush   10 
    Four of a Kind   156      [(13 choose 2) * (2 choose 1)]
    Full Houses      156      [(13 choose 2) * (2 choose 1)]
    Flush            1277     [(13 choose 5) - 10 straight flushes]
    Straight         10 
    Three of a Kind  858      [(13 choose 3) * (3 choose 1)]
    Two Pair         858      [(13 choose 3) * (3 choose 2)]
    One Pair         2860     [(13 choose 4) * (4 choose 1)]
    High Card      + 1277     [(13 choose 5) - 10 straights]
    -------------------------
    TOTAL            7462
    Here we create a lookup table which maps:
        5 card hand's unique prime product => rank in range [1, 7462]
    Examples:
    * Royal flush (best hand possible)          => 1
    * 7-5-4-3-2 unsuited (worst hand possible)  => 7462

"""

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
    i = 0  # used for searching
    if firstValue != secondValue:  # if both card values are not the same, following code is done

        for value in cardValue:  # checks through each element in the cardValue list, which is defined at the start
            if value == firstValue:
                firstValueIndex = i + 1
            else:
                if value == secondValue:
                    secondValueIndex = i + 1
                else:
                    i += 1
            # if values are already taken, compare them, compute the string and return it
            if firstValueIndex != 100 and secondValueIndex != 100:
                # value is:
                # all possible combinations - multiplication of two card strengths and 9
                # 8 is for accounting to the same value cards, which are also possible, such as 8CJD and 8SJC (they're the same strength)
                value = firstValueIndex * secondValueIndex * 8
                value = 7642 - value
                stringToSend = str("9 " + str(firstCard) + str(secondCard) + " " + str(value))
                return str(stringToSend)

    # if both cards are the same, there is a pair and another code is done
    if firstValue == secondValue:
        valueIndexes = firstValueIndex, secondValueIndex = (100, 100)
        for value in cardValue:
            if value == firstValue:
                firstValueIndex = i
                secondValueIndex = i
                # value is:
                # all possible combinations - ranks of the high cards - multiplication of two card strengths and 9
                # 9 is for accounting to the same value pairs, which are also possible, such as ASAD and AHAC (they're the same strength)
                value = 7642 - 1277 - (firstValueIndex * secondValueIndex * 17)
                stringToSend = str("8 " + str(firstCard) + str(secondCard) + " " + str(value))
                return str(stringToSend)
            else:
                i += 1


def evaluateCards(boardCards, handCards):
    # decrypt the two hand cards sent from the client + board cards
    n = 2
    str(boardCards).lower()
    boardCardsSplit = [(boardCards[i:i + n]) for i in range(0, len(boardCards), n)]


    str(handCards).lower()
    handCardsSplit = [(handCards[i:i + n]) for i in range(0, len(handCards), n)]

    handCardsSplit[0] = handCardsSplit[0][1] + handCardsSplit[0][0]
    handCardsSplit[1] = handCardsSplit[1][1] + handCardsSplit[1][0]

    hand = [
        Card.new(str(handCardsSplit[0].capitalize())),
        Card.new(str(handCardsSplit[1].capitalize()))
    ]
    board = []
    i = 0
    if len(list(boardCardsSplit)) == 3:
        board = [
            Card.new(str(boardCardsSplit[0].capitalize())),
            Card.new(str(boardCardsSplit[1].capitalize())),
            Card.new(str(boardCardsSplit[2].capitalize()))
        ]
    else:
        if len(list(boardCardsSplit)) == 4:
            board = [
                Card.new(str(boardCardsSplit[0].capitalize())),
                Card.new(str(boardCardsSplit[1].capitalize())),
                Card.new(str(boardCardsSplit[2].capitalize())),
                Card.new(str(boardCardsSplit[3].capitalize()))
            ]
        else:
            if len(list(boardCardsSplit)) == 5:
                board = [
                    Card.new(str(boardCardsSplit[0].capitalize())),
                    Card.new(str(boardCardsSplit[1].capitalize())),
                    Card.new(str(boardCardsSplit[2].capitalize())),
                    Card.new(str(boardCardsSplit[3].capitalize())),
                    Card.new(str(boardCardsSplit[4].capitalize()))
                ]

    deck = Deck()
    print(Card.print_pretty_cards(board + hand))

    evaluator = Evaluator()
    bestScore = evaluator.evaluate(board, hand)
    handType = evaluator.get_rank_class(bestScore)

    print("Player 1 hand rank = %d (%s)\n" % (bestScore, evaluator.class_to_string(handType)))

    if(len(board) == 5):
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
    else:
        best6Board = board
        best6Hand = hand

    print(Card.print_pretty_cards(best6Board + best6Hand))

    if(len(board) == 4):
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

    else:
        best5Board = best6Board
        best5Hand = best6Hand

    print(Card.print_pretty_cards(best5Board + best5Hand))

    card1 = convertCardToString(best5Board.__getitem__(0))
    card2 = convertCardToString(best5Board.__getitem__(1))
    card3 = convertCardToString(best5Board.__getitem__(2))
    card4 = convertCardToString(best5Hand.__getitem__(0))
    card5 = convertCardToString(best5Hand.__getitem__(1))

    handString = card1 + card2 + card3 + card4 + card5
    print("Hand string:  " + handString)

    stringToSend = str(handType) + " " + handString + " " + str(bestScore)

    print("String to send:  " + stringToSend)

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
