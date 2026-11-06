
# legal moves per piece; 144 integer board means stepping 12 digits to go up one rank, and up 1 digit to go right/ -1 to go left, with 2 digits on each rank for a boundary.
whitePawn = {"pawn":[12], "capture":[13,11]}
blackPawn = {"pawn":[-12], "capture":[-13,-11]}
knight = {"knight":[23,25,14,-10,-23,-25,-14,10]} # covers all 8 knight moves
bishop = {"bishop":[-13,-11,11,13]} # covers all possible moves ++ -- +- -+
rook = {"rook":[12,1,-12,-1]}
king = {"king":[-13,-12,-11,-1,1,11,12,13]} # covers the 8 tiles around the king
queen = {"queen":[-13,-11,11,13,12,1,-12,1]} # same logic as bishop and rook
pieceVectors = {"bishop": bishop["bishop"],
             "rook": rook["rook"],
             "queen": queen["queen"],
             "king": king["king"],
             "knight": knight["knight"],
             "pawn": "pawn",
             "whitePawn": whitePawn["pawn"],
             "whitePawnCapture": whitePawn["capture"],
             "blackPawn": blackPawn["pawn"],
             "blackPawnCapture": blackPawn["capture"],
             "boundary": [0],
             "blank": [0]}
pieces = {0:"blank", 1:"self", 2:"pawn", 3:"rook", 4:"knight", 5:"bishop", 6:"queen", 7:"king", 9:"boundary"} # 1 is reserved for an occupied space of the player's own colour
class Chess(): # chess class
    def __init__(self):
        self.currentPlayer = True # true for white, false for black.
        self.mainBoard = 999999999999999999999999993456754399992222222299990000000099990000000099990000000099990000000099992222222299993457654399999999999999999999999999 # standard game of chess
        self.whiteBoard = 999999999999999999999999991111111199991111111199990000000099990000000099990000000099990000000099992222222299993457654399999999999999999999999999
        self.blackBoard = 999999999999999999999999993456754399992222222299990000000099990000000099990000000099990000000099991111111199991111111199999999999999999999999999
        # each player's pieces are mapped on their own bitboard, so the legal moves can understand, without multiple functions, if a piece is takeable or not.
    def translateToIndex(self, square): # converts traditional chess board squares; A1, B1, etc. to the correct index on the bitboard
        self._letterIndex = "ABCDEFGH".index(square[0])
        self._pieceIndex = int(square[1]) * 12 + 14 + self._letterIndex
        return self._pieceIndex
    def translateToSquare(self, index):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        letter = index % 12 - 2
        number = index // 12 - 1
        return letters[letter] + str(number)
        return letter, number
    def printBoard(self, board):
        temp = str(board)
        for i in range(0,13):
            print(temp[(12-i)*12:(12-i)*12+12])
    def updateBoard(self, board, prev, new):
        prev = self.translateToIndex(prev)
        new = self.translateToIndex(new)
        piece = int(str(board)[prev])
        board -= piece * 10**(143-prev)
        board -= int(str(board)[new]) * 10**(143-new)
        board += piece * 10**(143-new)
        return board
    def applyMove(self, prev, new):
        self.mainBoard = self.updateBoard(self.mainBoard, prev, new)
        self.whiteBoard = self.updateBoard(self.whiteBoard, prev, new)
        self.blackBoard = self.updateBoard(self.blackBoard, prev, new)
    def legalMoves(self, location):
        pieceIndex = self.translateToIndex(location)
        self.piece = pieces[int(str(self.mainBoard)[pieceIndex])]
        vectorSet = pieceVectors[self.piece]
        self.moveSet = []
        if self.piece in ["knight", "king"]: # first checks pieces that have a set values of moves that doesn't vary on position
            for vector in vectorSet:
                if str(self.mainBoard)[pieceIndex + vector] != "9":
                    if self.currentPlayer:
                        if str(self.whiteBoard)[pieceIndex + vector] != "1":
                            self.visionBoard()
                            if (pieceIndex + vector not in self.whiteVision and self.piece == "king") or self.piece == "knight":
                                self.moveSet.append(vector)
                    else:
                        if str(self.blackBoard)[pieceIndex + vector] != "1":
                            self.visionBoard()
                            if (pieceIndex + vector not in self.blackVision and self.piece == "king") or self.piece == "knight":
                                self.moveSet.append(vector)
        if self.piece in ["rook", "bishop", "queen"]: # now checks pieces that go across diagonals, ranks and files.
            if self.piece == "queen":
                top = 8
            else:
                top = 4
            for i in range(0,top):
                step = 1
                complete = False
                while not complete:
                    steppedVector = step*vectorSet[i]
                    if str(self.mainBoard)[pieceIndex + steppedVector] != "9":
                        if self.currentPlayer:
                            if str(self.whiteBoard)[pieceIndex + steppedVector] != "1":
                                self.moveSet.append(steppedVector)
                            else:
                                complete = True
                        else:
                            if str(self.blackBoard)[pieceIndex + steppedVector] != "1":
                                self.moveSet.append(steppedVector)
                            else:
                                complete = True
                        step += 1
                    else:
                        complete = True
        if self.piece == "pawn": # checks pawns and their potential capture locations
            if self.currentPlayer:
                vectorSet = pieceVectors["whitePawn"]
                captureSet = pieceVectors["whitePawnCapture"]
                if location[1] == "2":
                    vectorSet.append(24)
            else:
                vectorSet = pieceVectors["blackPawn"]
                captureSet = pieceVectors["blackPawnCapture"]
                if location[1] == "7":
                    vectorSet.append(-24)
            blocked = False
            for vector in vectorSet:
                if not blocked:
                    if str(self.mainBoard)[pieceIndex + vector] != "9":
                        if self.currentPlayer:
                            if str(self.whiteBoard)[pieceIndex + vector] == "0":
                                self.moveSet.append(vector)
                            else:
                                blocked = True
                        else:
                            if str(self.blackBoard)[pieceIndex + vector] == "0":
                                self.moveSet.append(vector)
                            else:
                                blocked = True
            for vector in captureSet:
                if str(self.mainBoard)[pieceIndex + vector] != "9":
                    if self.currentPlayer:
                        if str(self.whiteBoard)[pieceIndex + vector] not in ["0","1"]:
                            self.moveSet.append(vector)
                    else:
                        if str(self.blackBoard)[pieceIndex + vector] not in ["0","1"]:
                            self.moveSet.append(vector)
        return self.moveSet
    def visionMoves(self, location): # essentially the same as legalMoves but altered to show the full range of each piece, showing which pieces are protected, and allowing pins to function.
        self.piece = pieces[int(str(self.mainBoard)[location])]
        vectorSet = pieceVectors[self.piece]
        self.captureSet = []
        if self.piece in ["knight", "king"]: # first checks pieces that have a set values of moves that doesn't vary on position
            for vector in vectorSet:
                if str(self.mainBoard)[location + vector] != "9":
                    if self.currentPlayer:
                        self.captureSet.append(vector)
                    else:
                        self.captureSet.append(vector)
        if self.piece in ["rook", "bishop", "queen"]: # now checks pieces that go across diagonals, ranks and files.
            if self.piece == "queen":
                top = 8
            else:
                top = 4
            for i in range(0,top):
                step = 1
                complete = False
                while not complete:
                    steppedVector = step*vectorSet[i]
                    if str(self.mainBoard)[location + steppedVector] != "9":
                        if self.currentPlayer:
                            if str(self.whiteBoard)[location + steppedVector] != "1":
                                self.captureSet.append(steppedVector)
                            else:
                                self.captureSet.append(steppedVector)
                                complete = True
                        else:
                            if str(self.blackBoard)[location + steppedVector] != "1":
                                self.captureSet.append(steppedVector)
                            else:
                                self.captureSet.append(steppedVector)
                                complete = True
                        step += 1
                    else:
                        complete = True
        if self.piece == "pawn": # checks pawns and their potential capture locations
            if self.currentPlayer:
                vectorSet = pieceVectors["whitePawnCapture"]
            else:
                vectorSet = pieceVectors["blackPawnCapture"]
            for vector in vectorSet:
                if str(self.mainBoard)[location + vector] != "9":
                    if self.currentPlayer:
                        self.captureSet.append(vector)
                    else:
                        self.captureSet.append(vector)
        return self.captureSet
    def visionBoard(self): # runs through each element in the white and black bitboards, then creates a vision board, used to show protected pieces, and unprotected squares, etc. updates every time it is called.
        index = 0
        self.whiteVision = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
        for piece in str(self.whiteBoard):
            for move in self.visionMoves(index):
                newIndex = move + index
                self.whiteBoard += 1 * 10**(143-newIndex)
            index += 1
        index = 0
        self.blackVision = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
        for piece in str(self.blackBoard):
            for move in self.visionMoves(index):
                newIndex = move + index
                self.blackBoard += 1 * 10**(143-newIndex)
            index += 1

Game = Chess()
Game.visionBoard()
Game.printBoard(Game.whiteVision)
print("test")