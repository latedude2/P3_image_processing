import socket   #library for socket networking
import treys
from treys import Evaluator
from treys import Card

# needed for the strength of each card to define later
cardValue = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cardSuit = ["h", "d", "s", "c"]

connected = True # for the server to know, when the connection is on and when off to wait for a new connection


def main():
    # Web cam should be connected here
    while True: # for more connection to be added after others end
        HOST = "192.168.43.18"   # Also known as IP
        PORT = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
        print('Socket created')
        try:
            s.bind((HOST, PORT))        # Assing IP to socket, no other program can use this port now
        except socket.error as err:
            print('Bind failed. Error Code : ' .format(err))
        s.listen(100)        # How many connections do we take in, set to 100 for testing
        print("Socket Listening")
        conn, addr = s.accept()         # Accept connection from client
        print("connection accepted")
        connected = True
        i = 0       # Used for testing
        stringToSend = "nothing"
        while(connected):
            # try-finally block needed, because if it's not there, when connection is cut, the error is thrown
            # to be able not to crash and then try to connect to someone else, we jump out to finally
            try:
                i = i + 1   # Used for testing
                # OpenCV stuff should be done here
                # Card Evaluation should be done here
                data = conn.recv(1024)  # Receive message from client
                string = data.decode(encoding='UTF-8') #decode the image from bytes to string
                if (len(string) == 4):
                    stringToSend = decryptHand(string) # making the string that should be sent
                    conn.send(bytes(str(stringToSend) + "\r\n", 'UTF-8'))  # Send message to client
            finally:
                connected = False

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
    if firstValue != secondValue: # if both card values are not the same, following code is done

        for value in cardValue: # checks through each element in the cardValue list, which is defined at the start
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

# decrypt the two hand cards sent from the client + board cards
# ---------------- NOT WORKING, JUST AS AN EXAMPLE ------------------
def evaluateCards(board, hand):
    hand = [
        Card.new("Qs"),
        Card.new("8c")
    ]
    board = [
        Card.new("Ks"),
        Card.new("Ad"),
        Card.new("Jc"),
        Card.new("5d"),
        Card.new("7s"),
    ]

    Card.print_pretty_cards(board + hand)

    evaluator = Evaluator()
    score = evaluator.evaluate(board, hand)
    handType = evaluator.get_rank_class(score)

    print("Player 1 hand rank = %d (%s)\n" % (score, evaluator.class_to_string(handType)))

if __name__ == '__main__':
    main()