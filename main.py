import random
import string
import csv
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

def newGame():  # Function
    inFile = True
    gameID = ""
    while inFile:
        f = open("games.csv", "r")
        gameID = "".join(random.choice(string.ascii_uppercase) for _ in range(4))
        if gameID in f.read():
            inFile = True
            f.close()
        else:
            inFile = False
            f.close()
            with open("games.csv", "a") as f:
                f.write(gameID + ",")
            with open(gameID + ".csv", "a") as f, open("game.csv", "r") as f2:
                for line in f2:
                    f.write(line)
            f.close()
            f2.close()
    return gameID

def getPiece(location, gameID):  # Function
    file = location[:1]
    rank = location[1:]
    f = open(gameID + ".csv", "r")
    line = ""
    for _ in range(9-int(rank)):
        line = f.readline()
    lineItems = line.split(",")
    f.close()
    return lineItems[int(letters.index(file))]

def isSquareValid(square):  # Function
    if square[:1] in letters and 1 <= int(square[1:]) <= 8:
        return True
    return False

def isCoordinateValid(coordinate):  # Function
    if 1 <= coordinate[0] <= 8 and 1 <= coordinate[1] <= 8:
        return True
    return False

def encodeSquare(square):  # Function
    return int(letters.index(square[:1])) + 1, int(square[1:])

def decodeCoordinate(coordinate):  # Function
    return letters[coordinate[0]-1] + str(coordinate[1])

def isHorVerBlocked(startPieceCoordinate, checkBlockSquareCoordinate, gameID):  # Function
    x1 = startPieceCoordinate[0]
    y1 = startPieceCoordinate[1]
    x2 = checkBlockSquareCoordinate[0]
    y2 = checkBlockSquareCoordinate[1]
    if y1 == y2:  # Horizontal
        if x2 - x1 > 0:  # East
            for i in range(x2 - x1 - 1):
                coordinate = (x2 - i - 1, startPieceCoordinate[1])
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
        else:  # West
            for i in range(x1 - x2 - 1):
                coordinate = (x2 + i + 1, startPieceCoordinate[1])
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
    else:  # Vertical
        if y2 - y1 > 0:  # North
            for i in range(y2 - y1 - 1):
                coordinate = (startPieceCoordinate[0], y2 - i - 1)
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
        else:  # South
            for i in range(y1 - y2 - 1):
                coordinate = (startPieceCoordinate[0], y2 + i + 1)
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
    return False

def isDiagonalBlocked(startPieceCoordinate, checkBlockSquareCoordinate, gameID):  # Function
    x1 = startPieceCoordinate[0]
    y1 = startPieceCoordinate[1]
    x2 = checkBlockSquareCoordinate[0]
    y2 = checkBlockSquareCoordinate[1]
    if y2 - y1 > 0:  # North
        if x2 - x1 > 0:  # East
            for i in range(x2 - x1 - 1):
                coordinate = ((x2 - i - 1), (y2 - i - 1))
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
        else:  # West
            for i in range(x1 - x2 - 1):
                coordinate = ((x2 + i + 1), (y2 - i - 1))
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
    else:  # South
        if x2 - x1 > 0:  # East
            for i in range(x2 - x1 - 1):
                coordinate = ((x2 - i - 1), (y2 + i + 1))
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True
        else:  # West
            for i in range(x1 - x2 - 1):
                coordinate = ((x2 + i + 1), (y2 + i + 1))
                if getPiece(decodeCoordinate(coordinate), gameID) != "  ":
                    return True

def getVisibleSquares(pieceType, coordinate, gameID):  # Function
    playerTurn = checkTurn(gameID)
    pieceSquare = decodeCoordinate(coordinate)
    if pieceType == " ":
        return
    x = coordinate[0]
    y = coordinate[1]
    if playerTurn == "W":
        pawnVisibleCoordinates = [(x-1, y+1), (x, y+1), (x+1, y+1)]
    else:
        pawnVisibleCoordinates = [(x-1, y-1), (x, y-1), (x+1, y-1)]
    rookVisibleCoordinates = []
    for i in range(1, 8):
        rookVisibleCoordinates.append((x, y+i))
        rookVisibleCoordinates.append((x, y-i))
        rookVisibleCoordinates.append((x+i, y))
        rookVisibleCoordinates.append((x-i, y))
    knightVisibleCoordinates = [(x+1, y+2), (x+2, y+1), (x+2, y-1), (x+1, y-2),
                                (x-1, y-2), (x-2, y-1), (x-2, y+1), (x-1, y+2)]
    bishopVisibleCoordinates = []
    for i in range(1, 8):
        bishopVisibleCoordinates.append((x+i, y+i))
        bishopVisibleCoordinates.append((x+i, y-i))
        bishopVisibleCoordinates.append((x-i, y+i))
        bishopVisibleCoordinates.append((x-i, y-i))
    kingVisibleCoordinates = [(x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1),
                              (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
    pieceVisibleCoordinates = []
    match pieceType:
        case "P":
            pieceVisibleCoordinates = pawnVisibleCoordinates
            if coordinate[1] == 2:
                pieceVisibleCoordinates.append((x, y+2))
            elif coordinate[1] == 7:
                pieceVisibleCoordinates.append((x, y-2))
        case "R":
            pieceVisibleCoordinates = rookVisibleCoordinates
        case "N":
            pieceVisibleCoordinates = knightVisibleCoordinates
        case "B":
            pieceVisibleCoordinates = bishopVisibleCoordinates
        case "K":
            pieceVisibleCoordinates = kingVisibleCoordinates
        case _:
            pass
    visibleSquares = []
    visibleSquaresHorVer = []
    visibleSquaresDiagonal = []
    if pieceType == "Q":
        for i in range(len(rookVisibleCoordinates)):
            square = rookVisibleCoordinates[i]
            if isCoordinateValid(square):
                square = decodeCoordinate(square)
                if getPiece(square, gameID)[:1] != getPiece(pieceSquare, gameID)[:1]:
                    visibleSquaresHorVer.append(square)
        for i in range(len(bishopVisibleCoordinates)):
            square = bishopVisibleCoordinates[i]
            if isCoordinateValid(square):
                square = decodeCoordinate(square)
                if getPiece(square, gameID)[:1] != getPiece(pieceSquare, gameID)[:1]:
                    visibleSquaresDiagonal.append(square)
    else:
        for i in range(len(pieceVisibleCoordinates)):
            square = pieceVisibleCoordinates[i]
            if isCoordinateValid(square):
                square = decodeCoordinate(square)
                if getPiece(square, gameID)[:1] != getPiece(pieceSquare, gameID)[:1]:
                    visibleSquares.append(square)
    match pieceType:
        case "R":
            for i in reversed(range(len(visibleSquares))):
                if isHorVerBlocked(encodeSquare(pieceSquare), encodeSquare(visibleSquares[i]), gameID):
                    visibleSquares.remove(visibleSquares[i])
        case "B":
            for i in reversed(range(len(visibleSquares))):
                if isDiagonalBlocked(encodeSquare(pieceSquare), encodeSquare(visibleSquares[i]), gameID):
                    visibleSquares.remove(visibleSquares[i])
        case "Q":
            for i in reversed(range(len(visibleSquaresHorVer))):
                if isHorVerBlocked(encodeSquare(pieceSquare), encodeSquare(visibleSquaresHorVer[i]), gameID):
                    visibleSquaresHorVer.pop()
                else:
                    visibleSquares.append(visibleSquaresHorVer[i])
                    visibleSquaresHorVer.pop()
            for i in reversed(range(len(visibleSquaresDiagonal))):
                if isHorVerBlocked(encodeSquare(pieceSquare), encodeSquare(visibleSquaresDiagonal[i]), gameID):
                    visibleSquaresDiagonal.pop()
                else:
                    visibleSquares.append(visibleSquaresDiagonal[i])
                    visibleSquaresDiagonal.pop()
        case _:
            pass
    return visibleSquares

def movePiece(startSquare, endSquare, gameID):  # Procedure
    playerTurn = checkTurn(gameID)
    with open(gameID + ".csv", newline="") as f:
        data = list(csv.reader(f))
    piece = getPiece(startSquare, gameID)
    startRank = 8-int(startSquare[1:])
    startFile = letters.index(startSquare[:1])
    endRank = 8-int(endSquare[1:])
    endFile = letters.index(endSquare[:1])
    # En Passant Start
    if data[endRank][endFile][1:] == "E" and piece[1:] == "P":
        if playerTurn == "W":
            data[endRank+1][endFile] = "  "
        else:
            data[endRank-1][endFile] = "  "
    if piece[1:] == "P":
        if (startRank == 1 and endRank == 3) or (startRank == 6 and endRank == 4):
            if playerTurn == "W":
                data[endRank+1][endFile] = "WE"
                data[9][0] = startSquare[:1] + str(int(startSquare[1:]) + 1)
            else:
                data[endRank-1][endFile] = "BE"
                data[10][0] = startSquare[:1] + str(int(startSquare[1:]) - 1)
        elif endRank == 0 or endRank == 7:
            pass
    # En Passant End
    data[startRank][startFile] = "  "
    data[endRank][endFile] = piece
    with open(gameID + ".csv", "w", newline="") as f:
        csv.writer(f).writerows(data)

def findKing(colour, gameID):  # Function
    pieceToFind = colour + "K"
    f = open(gameID + ".csv", "r")
    for y in reversed(range(1, 9)):
        line = f.readline()
        lineItems = line.split(",")
        for x in range(8):
            piece = lineItems[x]
            if piece == pieceToFind:
                return decodeCoordinate((x + 1, y))
    return False

def isInCheck(colour, gameID, checkSquare):  # Function
    if colour == "W":
        oppositeColour = "B"
    else:
        oppositeColour = "W"
    kingSquare = findKing(colour, gameID)
    horizontalView = getVisibleSquares("R", encodeSquare(checkSquare), gameID)
    for x in horizontalView:
        xPiece = getPiece(x, gameID)
        if xPiece == oppositeColour + "R" or xPiece == oppositeColour + "Q":
            return True
    diagonalView = getVisibleSquares("B", encodeSquare(checkSquare), gameID)
    for x in diagonalView:
        xPiece = getPiece(x, gameID)
        if xPiece == oppositeColour + "B" or xPiece == oppositeColour + "Q":
            return True
    knightView = getVisibleSquares("N", encodeSquare(checkSquare), gameID)
    for x in knightView:
        xPiece = getPiece(x, gameID)
        if xPiece == oppositeColour + "N":
            return True
    return False

def isCheckmate():  # Function
    inMate = False
    winner = None
    return inMate, winner

def isMoveLegal(startSquare, endSquare, gameID):  # Function
    playerTurn = checkTurn(gameID)
    startSquarePiece = getPiece(startSquare, gameID)
    endSquarePiece = getPiece(endSquare, gameID)
    if startSquarePiece[:1] == playerTurn:  # Checks if the piece to move is the correct colour
        if endSquarePiece[:1] != playerTurn:  # Checks if piece on end square isn't that players
            if endSquarePiece[1:] != "K":  # Checks if piece on end square is a king
                if endSquare in getVisibleSquares(startSquarePiece[1:], encodeSquare(startSquare), gameID):  # Checks if the square wanted to move to is in the list
                    # Pawn Start
                    if startSquarePiece[1:] == "P":  # Checks if piece is pawn
                        if startSquare[:1] == endSquare[:1]:  # Checks if the end square is on the same file as the start square
                            if endSquarePiece.strip():  # Checks if the end square has a piece
                                return False
                            else:
                                return True
                        else:
                            if endSquarePiece.strip():  # Checks if the end square has a piece
                                return True
                            else:
                                return False
                    # Pawn End
                    else:
                        return True
    return False

def getScore(colour, gameID):  # Function
    score = 0
    f = open(gameID + ".csv", "r")
    for _ in range(8):
        lineRead = f.readline()
        lineItems = lineRead.split(",")
        for x in range(8):
            if lineItems[x][:1] == colour:
                match lineItems[x][1:]:
                    case "P":
                        score += 1
                    case "R":
                        score += 5
                    case "N":
                        score += 3
                    case "B":
                        score += 3
                    case "Q":
                        score += 9
                    case _:
                        pass
    f.close()
    return score

def convertPieceToUnicode(piece):
    if piece == "  ":
        return "  "
    unicode = ""
    if piece[:1] == "W":
        match piece[1:]:
            case "P":
                unicode = u"\u2659"
            case "R":
                unicode = u"\u2656"
            case "N":
                unicode = u"\u2658"
            case "B":
                unicode = u"\u2657"
            case "Q":
                unicode = u"\u2655"
            case "K":
                unicode = u"\u2654"
    else:
        match piece[1:]:
            case "P":
                unicode = u"\u265F"
            case "R":
                unicode = u"\u265C"
            case "N":
                unicode = u"\u265E"
            case "B":
                unicode = u"\u265D"
            case "Q":
                unicode = u"\u265B"
            case "K":
                unicode = u"\u265A"
    return unicode + " "

def displayBoardA1(gameID):  # Procedure
    f = open(gameID + ".csv", "r")
    print("--|----|----|----|----|----|----|----|----|")
    for x in reversed(range(8)):
        lineRead = f.readline()
        lineItems = lineRead.split(",")
        line = ""
        for y in range(8):
            if lineItems[y][1:] == "E":
                lineItems[y] = "  "
            line += (" | " + convertPieceToUnicode(lineItems[y]))
        print(str(x+1) + line + " |")
        print("--|----|----|----|----|----|----|----|----|")
    line = ""
    for x in range(8):
        line += ("  | " + str(letters[x]))
    print(line + "  |")
    f.close()

def displayBoardH8(gameID):  # Procedure
    f = open(gameID + ".csv", "r")
    lines = ["" for _ in range(8)]
    for x in reversed(range(8)):
        lineRead = f.readline()
        lines[x] = lineRead
    print("--|----|----|----|----|----|----|----|----|")
    for x in range(8):
        lineItems = lines[x].split(",")
        line = ""
        for y in reversed(range(8)):
            if lineItems[y][1:] == "E":
                lineItems[y] = "  "
            line += (" | " + convertPieceToUnicode(lineItems[y]))
        print(str(x+1) + line + " |")
        print("--|----|----|----|----|----|----|----|----|")
    line = ""
    for x in reversed(range(8)):
        line += ("  | " + str(letters[x]))
    print(line + "  |")
    f.close()

def makeMove(playerTurn, gameID):  # Procedure
    if playerTurn == "W":
        print("White to move.")
    elif playerTurn == "B":
        print("Black to move.")
    while True:
        startSquare = input("Enter the square of the piece you want to move. > ").upper().strip()
        while not(isSquareValid(startSquare)):
            print("Invalid square.")
            startSquare = input("Enter the square of the piece you want to move. > ").upper().strip()
        endSquare = input("Enter the square you want to move to. > ").upper().strip()
        while not(isSquareValid(endSquare)):
            print("Invalid square.")
            endSquare = input("Enter the square you want to move to. > ").upper().strip()
        if not(isMoveLegal(startSquare, endSquare, gameID)):
            print("Illegal move.")
        else:
            break
    movePiece(startSquare, endSquare, gameID)
    with open(gameID + ".csv", newline="") as f:
        data = list(csv.reader(f))
    if playerTurn == "W":
        data[8][0] = "B"
    elif playerTurn == "B":
        data[8][0] = "W"
    with open(gameID + ".csv", "w", newline="") as f:
        csv.writer(f).writerows(data)

def checkTurn(gameID):  # Function
    with open(gameID + ".csv", newline="") as f:
        data = list(csv.reader(f))
    return data[8][0]

def turn(gameID):  # Procedure
    playerTurn = checkTurn(gameID)
    if playerTurn == "W":
        displayBoardA1(gameID)
        makeMove("W", gameID)
    elif playerTurn == "B":
        displayBoardH8(gameID)
        makeMove("B", gameID)

def game(gameID):  # Procedure
    while True:
        turn(gameID)
        mate = isCheckmate()
        if mate[0]:
            break
    if mate[1] == "W":
        print("Black is in checkmate, White wins!")
    else:
        print("White is in checkmate, Black wins!")

def gameSelect():  # Function
    option = input("Start a new game [N] or load an existing game [L]. > ").lower()
    while not (option == "n" or option == "l"):
        print("Please enter 'N' or 'L'.")
        option = input("Start a new game [N] or load an existing game [L]. > ").lower()
    return option

def loadGame():  # Function
    with open("games.csv", "r") as f:
        file = f.read()
    inputID = input("Please enter the 4 letter ID of the game. > ").upper()
    if not(inputID in file):
        print("This game does not exist.")
        return False, inputID
    return True, inputID

if __name__ == "__main__":
    while True:
        selection = gameSelect()
        if selection == "n":
            newGameID = newGame()
            print("Game ID: " + newGameID)
            game(newGameID)
            break
        elif selection == "l":
            loadGameID = loadGame()
            if loadGameID[0]:
                print("Game ID: " + loadGameID[1])
                game(loadGameID[1])
                break
