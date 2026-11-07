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
             "blank": [0],
             "self": [0]}
pieces = {0:"blank", 1:"self", 2:"pawn", 3:"rook", 4:"knight", 5:"bishop", 6:"queen", 7:"king", 9:"boundary"} # 1 is reserved for an occupied space of the player's own colour
class Chess(): # chess class
    def __init__(self):
        self.currentPlayer = True # true for white, false for black.
        self.mainBoard = 999999999999999999999999993456754399992222222299990000000099990000000099990000000099990000000099992222222299993457654399999999999999999999999999 # standard game of chess
        self.whiteBoard = 999999999999999999999999991111111199991111111199990000000099990000000099990000000099990000000099992222222299993457654399999999999999999999999999
        self.blackBoard = 999999999999999999999999993456754399992222222299990000000099990000000099990000000099990000000099991111111199991111111199999999999999999999999999
        self.madeTest = False
        # each player's pieces are mapped on their own bitboard, so the legal moves can understand, without multiple functions, if a piece is takeable or not.
    def translateToIndex(self, square): # converts traditional chess board squares; A1, B1, etc. to the correct index on the bitboard
        self._letterIndex = "ABCDEFGH".index(square[0])
        self._pieceIndex = int(square[1]) * 12 + 14 + self._letterIndex
        return self._pieceIndex
    def translateToSquare(self, index):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        letter = index % 12 - 2
        number = index // 12 - 1
        if not (letter < 0 or letter > 7 or number < 1 or number > 8):
            return letters[letter] + str(number)
    def printBoard(self, board):
        temp = str(board)
        for i in range(0,13):
            print(temp[(12-i)*12:(12-i)*12+12])
    def updateBoard(self, board, prev, new):
        global piece
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
    def testMove(self, prev, new):
        self.madeTest = True
        self.mainBoardTest = self.updateBoard(self.mainBoard, prev, new)
        self.whiteBoardTest = self.updateBoard(self.whiteBoard, prev, new)
        self.blackBoardTest = self.updateBoard(self.blackBoard, prev, new)
    def legalMoves(self, location):
        pieceIndex = self.translateToIndex(location)
        piece = pieces[int(str(self.mainBoard)[pieceIndex])]
        vectorSet = pieceVectors[piece]
        self.moveSet = []
        if piece in ["knight", "king"]: # first checks pieces that have a set values of moves that doesn't vary on position
            for vector in vectorSet:
                if vector == 1:
                    self.visionBoard()
                if str(self.mainBoard)[pieceIndex + vector] != "9":
                    if self.currentPlayer:
                        if str(self.whiteBoard)[pieceIndex + vector] != "1":
                            self.visionBoard()
                            if (int(str(self.blackVision)[pieceIndex + vector]) == 0 and piece == "king") or piece == "knight":
                                self.moveSet.append(vector)
                    else:
                        if str(self.blackBoard)[pieceIndex + vector] != "1":
                            self.visionBoard()
                            if (int(str(self.whiteVision[pieceIndex + vector])) == 0 and piece == "king") or piece == "knight":
                                self.moveSet.append(vector)
        if piece in ["rook", "bishop", "queen"]: # now checks pieces that go across diagonals, ranks and files.
            if piece == "queen":
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
                            if str(self.whiteBoard)[pieceIndex + steppedVector] == "0":
                                self.moveSet.append(steppedVector)
                            else:
                                if str(self.whiteBoard)[pieceIndex + steppedVector] != "1":
                                    self.moveSet.append(steppedVector)
                                complete = True
                        else:
                            if str(self.blackBoard)[pieceIndex + steppedVector] == "0":
                                self.moveSet.append(steppedVector)
                            else:
                                if str(self.blackBoard)[pieceIndex + steppedVector] != "1":
                                    self.moveSet.append(steppedVector)
                                complete = True
                        step += 1
                    else:
                        complete = True
        if piece == "pawn": # checks pawns and their potential capture locations
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
        removeList = []
        for move in self.moveSet:
            try:
                self.testMove(location, self.translateToSquare(self.translateToIndex(location) + move))
                self.visionBoard()
                self.kingStates()
                if self.currentPlayer:
                    if self.whiteCheckedTest:
                        removeList.append(move)
                else:
                    if self.blackCheckedTest:
                        removeList.append(move)
            except ValueError:
                continue
        for move in removeList:
            self.moveSet.remove(move)
        return self.moveSet
    def visionMoves(self, location, board, test): # essentially the same as legalMoves but altered to show the full range of each piece, showing which pieces are protected, and allowing pins to function.
        piece = pieces[int(str(board)[location])]
        vectorSet = pieceVectors[piece]
        self.captureSet = []
        if piece in ["knight", "king"]: # first checks pieces that have a set values of moves that doesn't vary on position
            for vector in vectorSet:
                if str(board)[location + vector] not in ["1","9"]:
                    if self.currentPlayer:
                        self.captureSet.append(vector)
                    else:
                        self.captureSet.append(vector)
        if piece in ["rook", "bishop", "queen"]: # now checks pieces that go across diagonals, ranks and files.
            if piece == "queen":
                top = 8
            else:
                top = 4
            for i in range(0,top):
                step = 1
                complete = False
                while not complete:
                    steppedVector = step*vectorSet[i]
                    if str(board)[location + steppedVector] != "9":
                        if self.currentPlayer:
                            if test:
                                if str(self.whiteBoardTest)[location + steppedVector] == "0":
                                    self.captureSet.append(steppedVector)
                                else:
                                    self.captureSet.append(steppedVector)
                                    complete = True
                            else:
                                if str(self.whiteBoard)[location + steppedVector] == "0":
                                    self.captureSet.append(steppedVector)
                                else:
                                    self.captureSet.append(steppedVector)
                                    complete = True
                        else:
                            if test:
                                if str(self.blackBoardTest)[location + steppedVector] == "0":
                                    self.captureSet.append(steppedVector)
                                else:
                                    self.captureSet.append(steppedVector)
                                    complete = True
                            else:
                                if str(self.blackBoard)[location + steppedVector] == "0":
                                    self.captureSet.append(steppedVector)
                                else:
                                    self.captureSet.append(steppedVector)
                                    complete = True
                        step += 1
                    else:
                        complete = True
        if piece == "pawn": # checks pawns and their potential capture locations
            if self.currentPlayer:
                vectorSet = pieceVectors["whitePawnCapture"]
            else:
                vectorSet = pieceVectors["blackPawnCapture"]
            for vector in vectorSet:
                if str(board)[location + vector] != "9":
                    if self.currentPlayer:
                        self.captureSet.append(vector)
                    else:
                        self.captureSet.append(vector)
        return self.captureSet
    def visionBoard(self): # runs through each element in the white and black bitboards, then creates a vision board, used to show protected pieces, and unprotected squares, etc. updates every time it is called.
        startvalue = self.currentPlayer
        self.currentPlayer = True
        index = 0
        self.whiteVision = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
        for piece in str(self.blackBoard):
            for move in self.visionMoves(index, self.blackBoard, False):
                newIndex = move + index
                self.whiteVision += 1 * 10**(143-newIndex)
            index += 1
        if self.madeTest:
            index = 0
            self.whiteVisionTest = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
            for piece in str(self.blackBoardTest):
                for move in self.visionMoves(index, self.blackBoardTest, True):
                    newIndex = move + index
                    self.whiteVisionTest += 1 * 10**(143-newIndex)
                index += 1
        self.currentPlayer = False
        index = 0     
        self.blackVision = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
        for piece in str(self.whiteBoard):
            for move in self.visionMoves(index, self.whiteBoard, False):
                newIndex = move + index
                self.blackVision += 1 * 10**(143-newIndex)
            index += 1
        if self.madeTest:
            index = 0     
            self.blackVisionTest = 999999999999999999999999990000000099990000000099990000000099990000000099990000000099990000000099990000000099990000000099999999999999999999999999
            for piece in str(self.whiteBoardTest):
                for move in self.visionMoves(index, self.whiteBoardTest, True):
                    newIndex = move + index
                    self.blackVisionTest += 1 * 10**(143-newIndex)
                index += 1
        self.currentPlayer = startvalue
    def kingStates(self): # checks the vision boards for each piece after normal and test moves to let me determine if a piece is pinned to the king, if the king is in check, etc.
        self.whiteChecked = False
        self.blackChecked = False
        index = str(self.blackBoard).index("7")
        if str(self.blackVision)[index] != "0":
            self.whiteChecked = True
        index = str(self.whiteBoard).index("7")
        if str(self.whiteVision)[index] != "0":
            self.blackChecked = True
        if self.madeTest:
            self.whiteCheckedTest = False
            self.blackCheckedTest = False
            index = str(self.blackBoardTest).index("7")
            if str(self.blackVisionTest)[index] != "0":
                self.whiteCheckedTest = True
            index = str(self.whiteBoardTest).index("7")
            if str(self.whiteVisionTest)[index] != "0":
                self.blackCheckedTest = True



Game = Chess()