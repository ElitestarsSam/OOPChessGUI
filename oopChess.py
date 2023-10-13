# Chess pieces by Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499803

import copy
import customtkinter
import pickle
import random
import string
from tkinter import PhotoImage

from PIL import Image

games = []
gameIDs = []
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
customtkinter.set_appearance_mode("dark")


# customtkinter.set_default_color_theme("themes/Greengage.json")

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("1000x850")
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.title("Chess")
        self.iconbitmap("n-white.ico")

        self.menuFrame = customtkinter.CTkFrame(self)
        self.menuFrame.grid(row=0, column=1, sticky="new", padx=(4, 8), pady=(8, 4), columnspan=8)

        self.infoFrame = customtkinter.CTkFrame(self)
        self.infoFrame.grid(row=0, column=0, sticky="nsw", padx=(8, 4), pady=8, rowspan=9)

        self.toggleFrame = customtkinter.CTkFrame(self.infoFrame, fg_color=("gray75", "gray30"))
        self.toggleFrame.grid(column=0, row=0, sticky="ew", padx=8, pady=(8, 4))
        # self.toggleFrame.grid_columnconfigure(0, weight=1)

        # self.modeLabelLight = customtkinter.CTkLabel(self.toggleFrame, text="Light")
        # self.modeLabelLight.grid(column=0, row=0, padx=(8, 4), pady=(8, 4), sticky="ew")
        self.modeToggle = customtkinter.CTkSwitch(self.toggleFrame, text="     Light - Dark",
                                                  command=self.toggleAppearance)
        self.modeToggle.pack(anchor="center", padx=8, pady=(8, 4))
        self.modeToggle.toggle()
        # self.modeLabelLight = customtkinter.CTkLabel(self.toggleFrame, text="Dark")
        # self.modeLabelLight.grid(column=2, row=0, padx=(4, 8), pady=(8, 4), sticky="ew")

    def toggleAppearance(self):
        if self.modeToggle.get() == 1:
            customtkinter.set_appearance_mode("dark")
        elif self.modeToggle.get() == 0:
            customtkinter.set_appearance_mode("light")


class BoardGUI(GUI):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.menuFrame.grid_columnconfigure((0, 1, 2), weight=1)
        self.resignButton = customtkinter.CTkButton(self.menuFrame, text="Resign", font=("", 15))
        self.resignButton.grid(padx=8, pady=8, sticky="w", row=0, column=0)
        self.codeLabel = customtkinter.CTkLabel(self.menuFrame, fg_color=("gray75", "gray30"),
                                                text="Game Code: " + self.game.id,
                                                font=("", 15), corner_radius=6)
        self.codeLabel.grid(padx=8, pady=8, sticky="ew", row=0, column=1)
        self.drawButton = customtkinter.CTkButton(self.menuFrame, text="Offer Draw", font=("", 15))
        self.drawButton.grid(padx=8, pady=8, sticky="e", row=0, column=2)

        self.movesFrame = customtkinter.CTkScrollableFrame(self.infoFrame, fg_color=("gray75", "gray30"), height=200)
        self.movesFrame.grid(column=0, row=1, sticky="ew", padx=8, pady=(8, 4))

        self.movesFrameLabel = customtkinter.CTkLabel(self.movesFrame, fg_color=("#8c8c8c", "#696969"), corner_radius=6,
                                                      text="Moves", width=150)
        self.movesFrameLabel.pack(padx=8, pady=(8, 4), anchor="center")

        self.boardFrame = customtkinter.CTkFrame(self, fg_color=("#3b8ed0", "#1f6aa5"))
        self.boardFrame.grid(column=1, row=1, sticky="se", padx=(4, 8), pady=(4, 8), rowspan=8, columnspan=8)
        self.boardFrame.grid_columnconfigure((0, 9), weight=1)
        self.boardFrame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)
        self.boardFrame.grid_rowconfigure((0, 9), weight=1)
        self.boardFrame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)

        for x in range(1, 9):
            self.letterLabel0 = customtkinter.CTkLabel(self.boardFrame, text=letters[x - 1])
            self.letterLabel0.grid(column=x, row=0)
            self.letterLabel9 = customtkinter.CTkLabel(self.boardFrame, text=letters[x - 1])
            self.letterLabel9.grid(column=x, row=9)
            self.numberLabel0 = customtkinter.CTkLabel(self.boardFrame, text=str(9 - x), padx=12)
            self.numberLabel0.grid(column=0, row=x)
            self.numberLabel9 = customtkinter.CTkLabel(self.boardFrame, text=str(9 - x), padx=12)
            self.numberLabel9.grid(column=9, row=x)

        self.piecesFrame = PiecesFrame(self.boardFrame, self.movesFrame, self.game)
        self.piecesFrame.grid(column=1, row=1, sticky="nesw", padx=0, pady=0, rowspan=8, columnspan=8)


class Game:
    def __init__(self):
        self.testBoard = [['WR', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BR'],
                          ['WN', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BN'],
                          ['WB', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BB'],
                          ['WQ', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BQ'],
                          ['WK', '  ', 'WE', 'WP', 'BP', 'BE', '  ', 'BK'],
                          ['WB', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BB'],
                          ['WN', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BN'],
                          ['WR', 'WP', '  ', '  ', '  ', '  ', 'BP', 'BR']]
        self.board = [["WR", "WP", "  ", "  ", "  ", "  ", "BP", "BR"],
                      ["WN", "WP", "  ", "  ", "  ", "  ", "BP", "BN"],
                      ["WB", "WP", "  ", "  ", "  ", "  ", "BP", "BB"],
                      ["WQ", "WP", "  ", "  ", "  ", "  ", "BP", "BQ"],
                      ["WK", "WP", "  ", "  ", "  ", "  ", "BP", "BK"],
                      ["WB", "WP", "  ", "  ", "  ", "  ", "BP", "BB"],
                      ["WN", "WP", "  ", "  ", "  ", "  ", "BP", "BN"],
                      ["WR", "WP", "  ", "  ", "  ", "  ", "BP", "BR"]]
        self.turn = "W"
        while True:
            self.id = "".join(random.choice(string.ascii_uppercase) for _ in range(4))
            if not (self.id in gameIDs):
                break
        self.enPassant = [(), ()]

    def __str__(self):
        return self.board

    def isHorizontalOrVerticalBlocked(self, pieceLocation, checkBlockSquareLocation, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        # Extract coordinates for the starting and ending squares
        x1, y1 = pieceLocation
        x2, y2 = checkBlockSquareLocation
        # Check if the movement is horizontal (same rank) or vertical (same file)
        if y1 == y2:  # Horizontal movement
            # Determine the direction of movement (East or West)
            if x2 > x1:  # East
                for x in range(x1 + 1, x2):
                    location = (x, y1)
                    # Check if there's a piece blocking the path
                    if self.getPieceFromLocation(location, board) != "  ":
                        return True
            else:  # West
                for x in range(x2 + 1, x1):
                    location = (x, y1)
                    # Check if there's a piece blocking the path
                    if self.getPieceFromLocation(location, board) != "  ":
                        return True
        else:  # Vertical movement
            # Determine the direction of movement (North or South)
            if y2 > y1:  # North
                for y in range(y1 + 1, y2):
                    location = (x1, y)
                    # Check if there's a piece blocking the path
                    if self.getPieceFromLocation(location, board) != "  ":
                        return True
            else:  # South
                for y in range(y2 + 1, y1):
                    location = (x1, y)
                    # Check if there's a piece blocking the path
                    if self.getPieceFromLocation(location, board) != "  ":
                        return True
        # If no blocking piece is found, return False
        return False

    def isDiagonalBlocked(self, pieceLocation, checkBlockSquareLocation, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        # Extract coordinates for the starting and ending squares
        x1, y1 = pieceLocation
        x2, y2 = checkBlockSquareLocation
        # Calculate the horizontal and vertical distances between the squares
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # Determine the direction of diagonal movement (North-East, North-West, South-East, or South-West)
        directionX = 1 if x2 > x1 else -1
        directionY = 1 if y2 > y1 else -1
        # Check if the movement is diagonal and there are no blocking pieces
        if dx == dy:
            # Iterate over squares along the diagonal path
            for i in range(1, dx):
                x = x1 + i * directionX
                y = y1 + i * directionY
                location = (x, y)
                # Check if there's a piece blocking the path
                if self.getPieceFromLocation(location, board) != "  ":
                    return True
        # If no blocking piece is found, return False
        return False

    def getVisibleLocations(self, pieceType, location, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        if pieceType == " ":
            return
        x, y = location
        if self.turn == "W":
            pawnVisibleLocations = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        else:
            pawnVisibleLocations = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        rookVisibleLocations = []
        for i in range(1, 8):
            rookVisibleLocations.append((x, y + i))
            rookVisibleLocations.append((x, y - i))
            rookVisibleLocations.append((x + i, y))
            rookVisibleLocations.append((x - i, y))
        knightVisibleLocations = [(x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
                                  (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)]
        bishopVisibleLocations = []
        for i in range(1, 8):
            bishopVisibleLocations.append((x + i, y + i))
            bishopVisibleLocations.append((x + i, y - i))
            bishopVisibleLocations.append((x - i, y + i))
            bishopVisibleLocations.append((x - i, y - i))
        kingVisibleLocations = [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                                (x + 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        pieceVisibleLocations = []
        match pieceType:
            case "P":
                pieceVisibleLocations = pawnVisibleLocations
                if location[1] == 1:
                    pieceVisibleLocations.append((x, y + 2))
                elif location[1] == 6:
                    pieceVisibleLocations.append((x, y - 2))
            case "R":
                pieceVisibleLocations = rookVisibleLocations
            case "N":
                pieceVisibleLocations = knightVisibleLocations
            case "B":
                pieceVisibleLocations = bishopVisibleLocations
            case "K":
                pieceVisibleLocations = kingVisibleLocations
            case _:
                pass
        for i in pieceVisibleLocations:
            if not self.isLocationValid(i):
                pieceVisibleLocations.remove(i)
        visibleLocations = []
        visibleLocationsTemp = []
        visibleLocationsHorizontalOrVertical = []
        visibleLocationsDiagonal = []
        if pieceType == "Q":
            for i in rookVisibleLocations:
                if self.isLocationValid(i):
                    if self.getPieceFromLocation(i, board)[:1] != self.getPieceFromLocation(location,
                                                                                            board)[:1]:
                        visibleLocationsHorizontalOrVertical.append(i)
            for i in bishopVisibleLocations:
                if self.isLocationValid(i):
                    if self.getPieceFromLocation(i, board)[:1] != self.getPieceFromLocation(location,
                                                                                            board)[:1]:
                        visibleLocationsDiagonal.append(i)
        else:
            for i in pieceVisibleLocations:
                if self.isLocationValid(i):
                    if self.getPieceFromLocation(i, board)[:1] != self.getPieceFromLocation(location,
                                                                                            board)[:1]:
                        visibleLocationsTemp.append(i)
        match pieceType:
            case "R":
                if visibleLocationsHorizontalOrVertical:
                    for i in reversed(range(len(visibleLocationsTemp))):
                        if self.isHorizontalOrVerticalBlocked(location, visibleLocationsHorizontalOrVertical[i], board):
                            visibleLocationsHorizontalOrVertical.pop()
                        else:
                            visibleLocations.append(visibleLocationsHorizontalOrVertical[i])
                            visibleLocationsHorizontalOrVertical.pop()
            case "B":
                if visibleLocationsDiagonal:
                    for i in reversed(range(len(visibleLocationsTemp))):
                        if self.isDiagonalBlocked(location, visibleLocationsDiagonal[i], board):
                            visibleLocationsDiagonal.pop()
                        else:
                            visibleLocations.append(visibleLocationsDiagonal[i])
                            visibleLocationsDiagonal.pop()
            case "Q":
                for i in reversed(range(len(visibleLocationsHorizontalOrVertical))):
                    if self.isHorizontalOrVerticalBlocked(location, visibleLocationsHorizontalOrVertical[i], board):
                        visibleLocationsHorizontalOrVertical.pop()
                    else:
                        visibleLocations.append(visibleLocationsHorizontalOrVertical[i])
                        visibleLocationsHorizontalOrVertical.pop()
                for i in reversed(range(len(visibleLocationsDiagonal))):
                    if self.isDiagonalBlocked(location, visibleLocationsDiagonal[i], board):
                        visibleLocationsDiagonal.pop()
                    else:
                        visibleLocations.append(visibleLocationsDiagonal[i])
                        visibleLocationsDiagonal.pop()
            case _:
                visibleLocations = visibleLocationsTemp
        return visibleLocations

    def findWhiteKing(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        self.getLocationsFromPieceType("WK", board)
        return self.getLocationsFromPieceType("WK", board)[0]

    def findBlackKing(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return self.getLocationsFromPieceType("BK", board)[0]

    def isInCheck(self, colour, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        if colour == "W":
            kingLocation = self.findWhiteKing(board)
            oppositeColour = "B"
        else:
            kingLocation = self.findBlackKing(board)
            oppositeColour = "W"
        horizontalView = self.getVisibleLocations("R", kingLocation, board)
        for location in horizontalView:
            piece = self.getPieceFromLocation(location, board)
            if piece in [oppositeColour + "R", oppositeColour + "Q", oppositeColour + "K"]:
                return True
        diagonalView = self.getVisibleLocations("B", kingLocation, board)
        for location in diagonalView:
            piece = self.getPieceFromLocation(location, board)
            if piece in [oppositeColour + "B", oppositeColour + "Q", oppositeColour + "K"]:
                return True
        knightView = self.getVisibleLocations("N", kingLocation, board)
        for location in knightView:
            piece = self.getPieceFromLocation(location, board)
            if piece == oppositeColour + "N":
                return True
        return False

    def isCheckmate(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        colour = self.turn

    def isWhiteInCheck(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return self.isInCheck(board, "W")

    def isBlackInCheck(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return self.isInCheck(board, "B")

    def getPieceLocations(self, colour, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        locations = []
        for x in range(8):
            for y in range(8):
                if board[x][y][:1] == colour:
                    locations.append((x, y))
        return locations

    def getAllMoves(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        moves = []
        colour = self.turn
        for location in self.getPieceLocations(colour, board):
            piece = self.getPieceFromLocation(location, board)
            for x in self.getVisibleLocations(piece[1:], location, board):
                if self.getPieceFromLocation(x, board)[:1] != colour:
                    moves.append(self.getSquareFromLocation(location) + self.getSquareFromLocation(x))
        return moves

    def getLegalMoves(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        legalMoves = []
        for move in self.getAllMoves(board):
            if self.isMoveLegal(move, board):
                legalMoves.append(move)
        return legalMoves

    def isMoveLegal(self, move, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        startSquareLocation = self.getLocationFromSquare(move[:2])
        endSquareLocation = self.getLocationFromSquare(move[2:])
        startPiece = self.getPieceFromLocation(startSquareLocation, board)
        endPiece = self.getPieceFromLocation(endSquareLocation, board)
        playerTurn = self.turn
        # Checks if the piece to move is the correct colour
        if startPiece[:1] == playerTurn:
            # Checks if piece on end square isn't that players
            if endPiece[:1] != playerTurn:
                # Checks if piece on end square is a king
                if endPiece[1:] != "K":
                    # Checks if the square wanted to move to is in the list
                    if endSquareLocation in self.getVisibleLocations(startPiece[1:], startSquareLocation, board):
                        # Checks if move puts the player in check
                        if not self.doesMovePutInCheck(move, board):
                            # Pawn Start
                            # Checks if piece is pawn
                            if startPiece[1:] == "P":
                                # Checks if the end square is on the same file as the start square
                                if startSquareLocation[0] == endSquareLocation[0]:
                                    # Checks if the end square has a piece
                                    if endPiece.strip():
                                        return False
                                    else:
                                        return True
                                else:
                                    # Checks if the end square has a piece
                                    if endPiece.strip():
                                        return True
                                    else:
                                        return False
                            # Pawn End
                            else:
                                return True
        return False

    def doesMovePutInCheck(self, move, mainBoard=None):
        if mainBoard is None:
            mainBoard = copy.deepcopy(self.board)
        if self.isInCheck(self.turn, self.getBoardFromPieceMove(move, mainBoard)):
            return True
        return False

    def movePiece(self, move, promotionPiece="P", mainBoard=None):
        if mainBoard is None:
            mainBoard = self.board
        mainBoard = self.getBoardFromPieceMove(move, promotionPiece, mainBoard)
        return mainBoard

    def oppositeTurn(self):
        if self.turn == "W":
            self.turn = "B"
        else:
            self.turn = "W"

    def getBoardFromPieceMove(self, move, promotionPiece="P", mainBoard=None):
        if mainBoard is None:
            mainBoard = self.board
        tempBoard = copy.deepcopy(mainBoard)
        playerTurn = self.turn
        startSquareLocation = self.getLocationFromSquare(move[:2])
        endSquareLocation = self.getLocationFromSquare(move[2:])
        piece = self.getPieceFromLocation(startSquareLocation, tempBoard)
        startFile, startRank = startSquareLocation
        endFile, endRank = endSquareLocation
        # En Passant Start
        if tempBoard[endFile][endRank][1:] == "E" and piece[1:] == "P":
            if playerTurn == "W":
                tempBoard[endFile][endRank - 1] = "  "
            else:
                tempBoard[endFile][endRank + 1] = "  "
        if playerTurn == "W":
            if self.enPassant[0]:
                tempBoard[self.enPassant[0][0]][self.enPassant[0][1]] = "  "
                self.enPassant[0] = ()
        else:
            if self.enPassant[1]:
                tempBoard[self.enPassant[1][0]][self.enPassant[1][1]] = "  "
                self.enPassant[1] = ()
        if piece[1:] == "P":
            if (startRank == 1 and endRank == 3) or (startRank == 6 and endRank == 4):
                if playerTurn == "W":
                    tempBoard[endFile][endRank - 1] = "WE"
                    (self.enPassant[0]) = (startFile, startRank + 1)
                else:
                    tempBoard[endFile][endRank + 1] = "BE"
                    (self.enPassant[1]) = (startFile, startRank - 1)
            elif (endRank == 0 and playerTurn == "B") or (endRank == 7 and playerTurn == "W"):
                piece = piece[:1] + promotionPiece
        # En Passant End
        tempBoard[startFile][startRank] = "  "
        tempBoard[endFile][endRank] = piece
        return tempBoard

    def getLocationsFromPieceType(self, piece, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        squares = []
        for x in range(8):
            for y in range(8):
                if board[x][y] == piece:
                    squares.append((x, y))
        return squares

    def getScore(self, colour, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        score = 0
        for x in range(8):
            for y in range(8):
                if board[x][y][:1] == colour:
                    match board[x][y][1:]:
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
        return score

    def getWhiteScore(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return self.getScore("W", board)

    def getBlackScore(self, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return self.getScore("B", board)

    def getPieceFromLocation(self, location, board=None):
        if board is None:
            board = copy.deepcopy(self.board)
        return board[location[0]][location[1]]

    @staticmethod
    def getLocationFromSquare(square):
        return letters.index(square[:1]), int(square[1:]) - 1

    @staticmethod
    def getSquareFromLocation(location):
        return letters[location[0]] + str(location[1] + 1)

    @staticmethod
    def isLocationValid(location):
        if 0 <= location[0] <= 7 and 0 <= location[1] <= 7:
            return True
        return False


class SquareButtonLight(customtkinter.CTkButton):
    def __init__(self, master, location):
        super().__init__(master)
        self.location = location
        self.configure(fg_color="#f0d9b5", width=98, height=98, text="", corner_radius=0, hover=False)


class SquareButtonDark(customtkinter.CTkButton):
    def __init__(self, master, location):
        super().__init__(master)
        self.location = location
        self.configure(fg_color="#b58863", width=98, height=98, text="", corner_radius=0, hover=False)


class PiecesFrame(customtkinter.CTkFrame):
    def __init__(self, master, movesFrame, game):
        super().__init__(master)
        self.configure(fg_color=("#8c8c8c", "#696969"), width=784, height=784)
        self.activatedFirst = ()
        self.activatedSecond = ()
        self.board = game.board
        self.game = game
        self.movesFrame = movesFrame
        self.buttons = [[[] for _ in range(8)] for _ in range(8)]
        self.createButtons()

    def buttonCommand(self, location):
        isFirstEmpty = not bool(self.activatedFirst)
        if location == self.activatedFirst:
            self.changeColour(self.activatedFirst)
            self.activatedFirst = ()
        elif isFirstEmpty:
            self.activatedFirst = location
            self.changeColour(self.activatedFirst)
        else:
            self.activatedSecond = location
            move = self.game.getSquareFromLocation(self.activatedFirst) + self.game.getSquareFromLocation(
                self.activatedSecond)
            if not self.game.isMoveLegal(move, self.board):
                self.changeColour(self.activatedFirst)
                self.activatedFirst = ()
                self.activatedSecond = ()
            else:
                self.board = self.game.movePiece(move, mainBoard=self.board)
                self.changeColour(self.activatedFirst)
                self.updateButton(self.activatedFirst)
                self.updateButton(self.activatedSecond)
                try:
                    self.updateButton((self.activatedSecond[0], self.activatedSecond[1] - 1))
                except IndexError:
                    pass
                try:
                    self.updateButton((self.activatedSecond[0], self.activatedSecond[1] + 1))
                except IndexError:
                    pass
                self.activatedFirst = ()
                self.activatedSecond = ()
                moveLabel = customtkinter.CTkLabel(self.movesFrame, text=move)
                moveLabel.pack(padx=8, pady=0, anchor="w")
                self.game.oppositeTurn()

    def changeColour(self, location):
        x, y = location
        button = self.buttons[x][y]
        colour = button.cget("fg_color")
        if colour == "#f0d9b5":
            button.configure(fg_color="#f8ec74")
        elif colour == "#b58863":
            button.configure(fg_color="#e0c44c")
        elif colour == "#f8ec74":
            button.configure(fg_color="#f0d9b5")
        elif colour == "#e0c44c":
            button.configure(fg_color="#b58863")

    def getPieceImageFromLocation(self, location, board=None):
        if board is None:
            board = self.board
        piece = self.getPieceFromLocation(location, board)
        if piece[1:] in [" ", "E"]:
            return ""
        if piece[:1] == "W":
            imagePath = piece[1:].lower() + "-white.png"
        else:
            imagePath = piece[1:].lower() + "-black.png"
        return customtkinter.CTkImage(light_image=Image.open("pieces/" + imagePath),
                                      dark_image=Image.open("pieces/" + imagePath),
                                      size=(90, 90))

    def getPieceFromLocation(self, location, board=None):
        if board is None:
            board = self.board
        return board[location[0]][location[1]]

    def updateButton(self, location):
        x, y = location
        button = self.buttons[x][y]
        try:
            button.configure(image=self.getPieceImageFromLocation(location, self.board))
            button.grid(column=x, row=7 - y)
        except ValueError:
            pass

    def createButtons(self):
        (self.buttons[0][0]) = SquareButtonDark(self, (0, 0))
        (self.buttons[0][0]).configure(command=lambda: self.buttonCommand((self.buttons[0][0]).location))
        try:
            (self.buttons[0][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 0), self.board))
        except ValueError:
            pass
        (self.buttons[0][0]).grid(column=0, row=7)

        (self.buttons[1][0]) = SquareButtonLight(self, (1, 0))
        (self.buttons[1][0]).configure(command=lambda: self.buttonCommand((self.buttons[1][0]).location))
        try:
            (self.buttons[1][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 0), self.board))
        except ValueError:
            pass
        (self.buttons[1][0]).grid(column=1, row=7)

        (self.buttons[2][0]) = SquareButtonDark(self, (2, 0))
        (self.buttons[2][0]).configure(command=lambda: self.buttonCommand((self.buttons[2][0]).location))
        try:
            (self.buttons[2][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 0), self.board))
        except ValueError:
            pass
        (self.buttons[2][0]).grid(column=2, row=7)

        (self.buttons[3][0]) = SquareButtonLight(self, (3, 0))
        (self.buttons[3][0]).configure(command=lambda: self.buttonCommand((self.buttons[3][0]).location))
        try:
            (self.buttons[3][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 0), self.board))
        except ValueError:
            pass
        (self.buttons[3][0]).grid(column=3, row=7)

        (self.buttons[4][0]) = SquareButtonDark(self, (4, 0))
        (self.buttons[4][0]).configure(command=lambda: self.buttonCommand((self.buttons[4][0]).location))
        try:
            (self.buttons[4][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 0), self.board))
        except ValueError:
            pass
        (self.buttons[4][0]).grid(column=4, row=7)

        (self.buttons[5][0]) = SquareButtonLight(self, (5, 0))
        (self.buttons[5][0]).configure(command=lambda: self.buttonCommand((self.buttons[5][0]).location))
        try:
            (self.buttons[5][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 0), self.board))
        except ValueError:
            pass
        (self.buttons[5][0]).grid(column=5, row=7)

        (self.buttons[6][0]) = SquareButtonDark(self, (6, 0))
        (self.buttons[6][0]).configure(command=lambda: self.buttonCommand((self.buttons[6][0]).location))
        try:
            (self.buttons[6][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 0), self.board))
        except ValueError:
            pass
        (self.buttons[6][0]).grid(column=6, row=7)

        (self.buttons[7][0]) = SquareButtonLight(self, (7, 0))
        (self.buttons[7][0]).configure(command=lambda: self.buttonCommand((self.buttons[7][0]).location))
        try:
            (self.buttons[7][0]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 0), self.board))
        except ValueError:
            pass
        (self.buttons[7][0]).grid(column=7, row=7)

        (self.buttons[0][2]) = SquareButtonDark(self, (0, 2))
        (self.buttons[0][2]).configure(command=lambda: self.buttonCommand((self.buttons[0][2]).location))
        try:
            (self.buttons[0][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 2), self.board))
        except ValueError:
            pass
        (self.buttons[0][2]).grid(column=0, row=5)

        (self.buttons[1][2]) = SquareButtonLight(self, (1, 2))
        (self.buttons[1][2]).configure(command=lambda: self.buttonCommand((self.buttons[1][2]).location))
        try:
            (self.buttons[1][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 2), self.board))
        except ValueError:
            pass
        (self.buttons[1][2]).grid(column=1, row=5)

        (self.buttons[2][2]) = SquareButtonDark(self, (2, 2))
        (self.buttons[2][2]).configure(command=lambda: self.buttonCommand((self.buttons[2][2]).location))
        try:
            (self.buttons[2][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 2), self.board))
        except ValueError:
            pass
        (self.buttons[2][2]).grid(column=2, row=5)

        (self.buttons[3][2]) = SquareButtonLight(self, (3, 2))
        (self.buttons[3][2]).configure(command=lambda: self.buttonCommand((self.buttons[3][2]).location))
        try:
            (self.buttons[3][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 2), self.board))
        except ValueError:
            pass
        (self.buttons[3][2]).grid(column=3, row=5)

        (self.buttons[4][2]) = SquareButtonDark(self, (4, 2))
        (self.buttons[4][2]).configure(command=lambda: self.buttonCommand((self.buttons[4][2]).location))
        try:
            (self.buttons[4][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 2), self.board))
        except ValueError:
            pass
        (self.buttons[4][2]).grid(column=4, row=5)

        (self.buttons[5][2]) = SquareButtonLight(self, (5, 2))
        (self.buttons[5][2]).configure(command=lambda: self.buttonCommand((self.buttons[5][2]).location))
        try:
            (self.buttons[5][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 2), self.board))
        except ValueError:
            pass
        (self.buttons[5][2]).grid(column=5, row=5)

        (self.buttons[6][2]) = SquareButtonDark(self, (6, 2))
        (self.buttons[6][2]).configure(command=lambda: self.buttonCommand((self.buttons[6][2]).location))
        try:
            (self.buttons[6][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 2), self.board))
        except ValueError:
            pass
        (self.buttons[6][2]).grid(column=6, row=5)

        (self.buttons[7][2]) = SquareButtonLight(self, (7, 2))
        (self.buttons[7][2]).configure(command=lambda: self.buttonCommand((self.buttons[7][2]).location))
        try:
            (self.buttons[7][2]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 2), self.board))
        except ValueError:
            pass
        (self.buttons[7][2]).grid(column=7, row=5)

        (self.buttons[0][4]) = SquareButtonDark(self, (0, 4))
        (self.buttons[0][4]).configure(command=lambda: self.buttonCommand((self.buttons[0][4]).location))
        try:
            (self.buttons[0][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 4), self.board))
        except ValueError:
            pass
        (self.buttons[0][4]).grid(column=0, row=3)

        (self.buttons[1][4]) = SquareButtonLight(self, (1, 4))
        (self.buttons[1][4]).configure(command=lambda: self.buttonCommand((self.buttons[1][4]).location))
        try:
            (self.buttons[1][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 4), self.board))
        except ValueError:
            pass
        (self.buttons[1][4]).grid(column=1, row=3)

        (self.buttons[2][4]) = SquareButtonDark(self, (2, 4))
        (self.buttons[2][4]).configure(command=lambda: self.buttonCommand((self.buttons[2][4]).location))
        try:
            (self.buttons[2][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 4), self.board))
        except ValueError:
            pass
        (self.buttons[2][4]).grid(column=2, row=3)

        (self.buttons[3][4]) = SquareButtonLight(self, (3, 4))
        (self.buttons[3][4]).configure(command=lambda: self.buttonCommand((self.buttons[3][4]).location))
        try:
            (self.buttons[3][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 4), self.board))
        except ValueError:
            pass
        (self.buttons[3][4]).grid(column=3, row=3)

        (self.buttons[4][4]) = SquareButtonDark(self, (4, 4))
        (self.buttons[4][4]).configure(command=lambda: self.buttonCommand((self.buttons[4][4]).location))
        try:
            (self.buttons[4][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 4), self.board))
        except ValueError:
            pass
        (self.buttons[4][4]).grid(column=4, row=3)

        (self.buttons[5][4]) = SquareButtonLight(self, (5, 4))
        (self.buttons[5][4]).configure(command=lambda: self.buttonCommand((self.buttons[5][4]).location))
        try:
            (self.buttons[5][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 4), self.board))
        except ValueError:
            pass
        (self.buttons[5][4]).grid(column=5, row=3)

        (self.buttons[6][4]) = SquareButtonDark(self, (6, 4))
        (self.buttons[6][4]).configure(command=lambda: self.buttonCommand((self.buttons[6][4]).location))
        try:
            (self.buttons[6][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 4), self.board))
        except ValueError:
            pass
        (self.buttons[6][4]).grid(column=6, row=3)

        (self.buttons[7][4]) = SquareButtonLight(self, (7, 4))
        (self.buttons[7][4]).configure(command=lambda: self.buttonCommand((self.buttons[7][4]).location))
        try:
            (self.buttons[7][4]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 4), self.board))
        except ValueError:
            pass
        (self.buttons[7][4]).grid(column=7, row=3)

        (self.buttons[0][6]) = SquareButtonDark(self, (0, 6))
        (self.buttons[0][6]).configure(command=lambda: self.buttonCommand((self.buttons[0][6]).location))
        try:
            (self.buttons[0][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 6), self.board))
        except ValueError:
            pass
        (self.buttons[0][6]).grid(column=0, row=1)

        (self.buttons[1][6]) = SquareButtonLight(self, (1, 6))
        (self.buttons[1][6]).configure(command=lambda: self.buttonCommand((self.buttons[1][6]).location))
        try:
            (self.buttons[1][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 6), self.board))
        except ValueError:
            pass
        (self.buttons[1][6]).grid(column=1, row=1)

        (self.buttons[2][6]) = SquareButtonDark(self, (2, 6))
        (self.buttons[2][6]).configure(command=lambda: self.buttonCommand((self.buttons[2][6]).location))
        try:
            (self.buttons[2][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 6), self.board))
        except ValueError:
            pass
        (self.buttons[2][6]).grid(column=2, row=1)

        (self.buttons[3][6]) = SquareButtonLight(self, (3, 6))
        (self.buttons[3][6]).configure(command=lambda: self.buttonCommand((self.buttons[3][6]).location))
        try:
            (self.buttons[3][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 6), self.board))
        except ValueError:
            pass
        (self.buttons[3][6]).grid(column=3, row=1)

        (self.buttons[4][6]) = SquareButtonDark(self, (4, 6))
        (self.buttons[4][6]).configure(command=lambda: self.buttonCommand((self.buttons[4][6]).location))
        try:
            (self.buttons[4][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 6), self.board))
        except ValueError:
            pass
        (self.buttons[4][6]).grid(column=4, row=1)

        (self.buttons[5][6]) = SquareButtonLight(self, (5, 6))
        (self.buttons[5][6]).configure(command=lambda: self.buttonCommand((self.buttons[5][6]).location))
        try:
            (self.buttons[5][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 6), self.board))
        except ValueError:
            pass
        (self.buttons[5][6]).grid(column=5, row=1)

        (self.buttons[6][6]) = SquareButtonDark(self, (6, 6))
        (self.buttons[6][6]).configure(command=lambda: self.buttonCommand((self.buttons[6][6]).location))
        try:
            (self.buttons[6][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 6), self.board))
        except ValueError:
            pass
        (self.buttons[6][6]).grid(column=6, row=1)

        (self.buttons[7][6]) = SquareButtonLight(self, (7, 6))
        (self.buttons[7][6]).configure(command=lambda: self.buttonCommand((self.buttons[7][6]).location))
        try:
            (self.buttons[7][6]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 6), self.board))
        except ValueError:
            pass
        (self.buttons[7][6]).grid(column=7, row=1)

        (self.buttons[0][1]) = SquareButtonLight(self, (0, 1))
        (self.buttons[0][1]).configure(command=lambda: self.buttonCommand((self.buttons[0][1]).location))
        try:
            (self.buttons[0][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 1), self.board))
        except ValueError:
            pass
        (self.buttons[0][1]).grid(column=0, row=6)

        (self.buttons[1][1]) = SquareButtonDark(self, (1, 1))
        (self.buttons[1][1]).configure(command=lambda: self.buttonCommand((self.buttons[1][1]).location))
        try:
            (self.buttons[1][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 1), self.board))
        except ValueError:
            pass
        (self.buttons[1][1]).grid(column=1, row=6)

        (self.buttons[2][1]) = SquareButtonLight(self, (2, 1))
        (self.buttons[2][1]).configure(command=lambda: self.buttonCommand((self.buttons[2][1]).location))
        try:
            (self.buttons[2][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 1), self.board))
        except ValueError:
            pass
        (self.buttons[2][1]).grid(column=2, row=6)

        (self.buttons[3][1]) = SquareButtonDark(self, (3, 1))
        (self.buttons[3][1]).configure(command=lambda: self.buttonCommand((self.buttons[3][1]).location))
        try:
            (self.buttons[3][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 1), self.board))
        except ValueError:
            pass
        (self.buttons[3][1]).grid(column=3, row=6)

        (self.buttons[4][1]) = SquareButtonLight(self, (4, 1))
        (self.buttons[4][1]).configure(command=lambda: self.buttonCommand((self.buttons[4][1]).location))
        try:
            (self.buttons[4][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 1), self.board))
        except ValueError:
            pass
        (self.buttons[4][1]).grid(column=4, row=6)

        (self.buttons[5][1]) = SquareButtonDark(self, (5, 1))
        (self.buttons[5][1]).configure(command=lambda: self.buttonCommand((self.buttons[5][1]).location))
        try:
            (self.buttons[5][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 1), self.board))
        except ValueError:
            pass
        (self.buttons[5][1]).grid(column=5, row=6)

        (self.buttons[6][1]) = SquareButtonLight(self, (6, 1))
        (self.buttons[6][1]).configure(command=lambda: self.buttonCommand((self.buttons[6][1]).location))
        try:
            (self.buttons[6][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 1), self.board))
        except ValueError:
            pass
        (self.buttons[6][1]).grid(column=6, row=6)

        (self.buttons[7][1]) = SquareButtonDark(self, (7, 1))
        (self.buttons[7][1]).configure(command=lambda: self.buttonCommand((self.buttons[7][1]).location))
        try:
            (self.buttons[7][1]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 1), self.board))
        except ValueError:
            pass
        (self.buttons[7][1]).grid(column=7, row=6)

        (self.buttons[0][3]) = SquareButtonLight(self, (0, 3))
        (self.buttons[0][3]).configure(command=lambda: self.buttonCommand((self.buttons[0][3]).location))
        try:
            (self.buttons[0][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 3), self.board))
        except ValueError:
            pass
        (self.buttons[0][3]).grid(column=0, row=4)

        (self.buttons[1][3]) = SquareButtonDark(self, (1, 3))
        (self.buttons[1][3]).configure(command=lambda: self.buttonCommand((self.buttons[1][3]).location))
        try:
            (self.buttons[1][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 3), self.board))
        except ValueError:
            pass
        (self.buttons[1][3]).grid(column=1, row=4)

        (self.buttons[2][3]) = SquareButtonLight(self, (2, 3))
        (self.buttons[2][3]).configure(command=lambda: self.buttonCommand((self.buttons[2][3]).location))
        try:
            (self.buttons[2][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 3), self.board))
        except ValueError:
            pass
        (self.buttons[2][3]).grid(column=2, row=4)

        (self.buttons[3][3]) = SquareButtonDark(self, (3, 3))
        (self.buttons[3][3]).configure(command=lambda: self.buttonCommand((self.buttons[3][3]).location))
        try:
            (self.buttons[3][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 3), self.board))
        except ValueError:
            pass
        (self.buttons[3][3]).grid(column=3, row=4)

        (self.buttons[4][3]) = SquareButtonLight(self, (4, 3))
        (self.buttons[4][3]).configure(command=lambda: self.buttonCommand((self.buttons[4][3]).location))
        try:
            (self.buttons[4][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 3), self.board))
        except ValueError:
            pass
        (self.buttons[4][3]).grid(column=4, row=4)

        (self.buttons[5][3]) = SquareButtonDark(self, (5, 3))
        (self.buttons[5][3]).configure(command=lambda: self.buttonCommand((self.buttons[5][3]).location))
        try:
            (self.buttons[5][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 3), self.board))
        except ValueError:
            pass
        (self.buttons[5][3]).grid(column=5, row=4)

        (self.buttons[6][3]) = SquareButtonLight(self, (6, 3))
        (self.buttons[6][3]).configure(command=lambda: self.buttonCommand((self.buttons[6][3]).location))
        try:
            (self.buttons[6][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 3), self.board))
        except ValueError:
            pass
        (self.buttons[6][3]).grid(column=6, row=4)

        (self.buttons[7][3]) = SquareButtonDark(self, (7, 3))
        (self.buttons[7][3]).configure(command=lambda: self.buttonCommand((self.buttons[7][3]).location))
        try:
            (self.buttons[7][3]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 3), self.board))
        except ValueError:
            pass
        (self.buttons[7][3]).grid(column=7, row=4)

        (self.buttons[0][5]) = SquareButtonLight(self, (0, 5))
        (self.buttons[0][5]).configure(command=lambda: self.buttonCommand((self.buttons[0][5]).location))
        try:
            (self.buttons[0][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 5), self.board))
        except ValueError:
            pass
        (self.buttons[0][5]).grid(column=0, row=2)

        (self.buttons[1][5]) = SquareButtonDark(self, (1, 5))
        (self.buttons[1][5]).configure(command=lambda: self.buttonCommand((self.buttons[1][5]).location))
        try:
            (self.buttons[1][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 5), self.board))
        except ValueError:
            pass
        (self.buttons[1][5]).grid(column=1, row=2)

        (self.buttons[2][5]) = SquareButtonLight(self, (2, 5))
        (self.buttons[2][5]).configure(command=lambda: self.buttonCommand((self.buttons[2][5]).location))
        try:
            (self.buttons[2][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 5), self.board))
        except ValueError:
            pass
        (self.buttons[2][5]).grid(column=2, row=2)

        (self.buttons[3][5]) = SquareButtonDark(self, (3, 5))
        (self.buttons[3][5]).configure(command=lambda: self.buttonCommand((self.buttons[3][5]).location))
        try:
            (self.buttons[3][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 5), self.board))
        except ValueError:
            pass
        (self.buttons[3][5]).grid(column=3, row=2)

        (self.buttons[4][5]) = SquareButtonLight(self, (4, 5))
        (self.buttons[4][5]).configure(command=lambda: self.buttonCommand((self.buttons[4][5]).location))
        try:
            (self.buttons[4][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 5), self.board))
        except ValueError:
            pass
        (self.buttons[4][5]).grid(column=4, row=2)

        (self.buttons[5][5]) = SquareButtonDark(self, (5, 5))
        (self.buttons[5][5]).configure(command=lambda: self.buttonCommand((self.buttons[5][5]).location))
        try:
            (self.buttons[5][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 5), self.board))
        except ValueError:
            pass
        (self.buttons[5][5]).grid(column=5, row=2)

        (self.buttons[6][5]) = SquareButtonLight(self, (6, 5))
        (self.buttons[6][5]).configure(command=lambda: self.buttonCommand((self.buttons[6][5]).location))
        try:
            (self.buttons[6][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 5), self.board))
        except ValueError:
            pass
        (self.buttons[6][5]).grid(column=6, row=2)

        (self.buttons[7][5]) = SquareButtonDark(self, (7, 5))
        (self.buttons[7][5]).configure(command=lambda: self.buttonCommand((self.buttons[7][5]).location))
        try:
            (self.buttons[7][5]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 5), self.board))
        except ValueError:
            pass
        (self.buttons[7][5]).grid(column=7, row=2)

        (self.buttons[0][7]) = SquareButtonLight(self, (0, 7))
        (self.buttons[0][7]).configure(command=lambda: self.buttonCommand((self.buttons[0][7]).location))
        try:
            (self.buttons[0][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((0, 7), self.board))
        except ValueError:
            pass
        (self.buttons[0][7]).grid(column=0, row=0)

        (self.buttons[1][7]) = SquareButtonDark(self, (1, 7))
        (self.buttons[1][7]).configure(command=lambda: self.buttonCommand((self.buttons[1][7]).location))
        try:
            (self.buttons[1][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((1, 7), self.board))
        except ValueError:
            pass
        (self.buttons[1][7]).grid(column=1, row=0)

        (self.buttons[2][7]) = SquareButtonLight(self, (2, 7))
        (self.buttons[2][7]).configure(command=lambda: self.buttonCommand((self.buttons[2][7]).location))
        try:
            (self.buttons[2][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((2, 7), self.board))
        except ValueError:
            pass
        (self.buttons[2][7]).grid(column=2, row=0)

        (self.buttons[3][7]) = SquareButtonDark(self, (3, 7))
        (self.buttons[3][7]).configure(command=lambda: self.buttonCommand((self.buttons[3][7]).location))
        try:
            (self.buttons[3][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((3, 7), self.board))
        except ValueError:
            pass
        (self.buttons[3][7]).grid(column=3, row=0)

        (self.buttons[4][7]) = SquareButtonLight(self, (4, 7))
        (self.buttons[4][7]).configure(command=lambda: self.buttonCommand((self.buttons[4][7]).location))
        try:
            (self.buttons[4][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((4, 7), self.board))
        except ValueError:
            pass
        (self.buttons[4][7]).grid(column=4, row=0)

        (self.buttons[5][7]) = SquareButtonDark(self, (5, 7))
        (self.buttons[5][7]).configure(command=lambda: self.buttonCommand((self.buttons[5][7]).location))
        try:
            (self.buttons[5][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((5, 7), self.board))
        except ValueError:
            pass
        (self.buttons[5][7]).grid(column=5, row=0)

        (self.buttons[6][7]) = SquareButtonLight(self, (6, 7))
        (self.buttons[6][7]).configure(command=lambda: self.buttonCommand((self.buttons[6][7]).location))
        try:
            (self.buttons[6][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((6, 7), self.board))
        except ValueError:
            pass
        (self.buttons[6][7]).grid(column=6, row=0)

        (self.buttons[7][7]) = SquareButtonDark(self, (7, 7))
        (self.buttons[7][7]).configure(command=lambda: self.buttonCommand((self.buttons[7][7]).location))
        try:
            (self.buttons[7][7]).configure(bg_color="transparent",
                                           image=self.getPieceImageFromLocation((7, 7), self.board))
        except ValueError:
            pass
        (self.buttons[7][7]).grid(column=7, row=0)


def saveGame(game):
    try:
        with open("games/" + game.id + ".pickle", "wb") as f:
            pickle.dump(game, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)


def loadGame(gameID):
    try:
        with open("games/" + gameID + ".pickle", "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


def newGame():
    g = Game()
    games.append(g)
    gameIDs.append(g.id)
    return g.id


def getGame(gameID):
    return games[gameIDs.index(gameID)]


game1 = Game()
gui = BoardGUI(game1)
gui.mainloop()
