import random
import copy



S = 14  # board size
allSquares = set([(x,y) for x in range(S) for y in range(S)])

pieces = [
    ([(1,1)],
     ["e"], "line-1"),

    ([(1,1), (2,1)],
     ["e", "R"], "line-2"),

    ([(1,1), (2,1), (3,1)],
     ["e", "R"], "line-3"),

    ([(1,1), (2,1), (3,1), (4,1)],
     ["e", "R"], "line-4"),

    ([(1,1), (2,1), (3,1), (4,1), (5,1)],
     ["e", "R"], "line 5"),

    ([(1,1), (2,1), (3,1), (4,1), (4,2)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "long L"),

    ([(1,1), (2,1), (3,1), (3,2)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "letter L"),

    ([(1,1), (2,1), (2,2)],
     ["e", "R", "RR", "RRR"], "short L"),

    ([(1,1), (2,1), (3,1), (3,2), (3,3)],
     ["e", "R", "RR", "RRR"], "symmetric L"),

    ([(1,1), (2,1), (2,2), (3,1)],
     ["e", "R", "RR", "RRR"], "short T"),

    ([(1,1), (2,1), (2,2), (2,3), (3,1)],
     ["e", "R", "RR", "RRR"], "letter T"),

    ([(1,1), (2,1), (2,2), (3,1), (4,1)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "uneven T"),

    ([(1,1), (2,1), (2,2), (3,1), (2,0)],
     ["e"], "plus"),

    ([(1,0), (2,1), (2,2), (3,1), (2,0)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "TF"),

    ([(1,1), (2,1), (1,2), (2,2)],
     ["e"], "square"),

    ([(1,1), (2,1), (1,2), (2,2), (2,3)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "square plus"),

    ([(1,1), (2,1), (3,2), (2,2)],
     ["e", "R", "F", "FR"], "short z"),

    ([(1,1), (2,1), (2,2), (3,2), (3,3)],
     ["e", "R", "F", "FR"], "long z"),

    ([(0,1), (1,1), (2,1), (3,2), (2,2)],
     ["e", "R", "RR", "RRR", "F", "FR", "FRR", "FRRR"], "short extended z"),

    ([(1,1), (1,2), (2,2), (2,3), (3,3)],
     ["e", "R", "RR", "RRR"], "stairs"),

    ([(1,1), (2,1), (1,2), (1,3), (2,3)],
     ["e", "R", "RR", "RRR"], "letter u"),
]

totalSquares = sum([len(piece[0]) for piece in pieces])  # 89

def rotate(coords):
    res = []
    for c in coords:
        res.append((c[1], -c[0]))
    return res


def flip(coords):
    res = []
    for c in coords:
        res.append((-c[0], c[1]))
    return res

def add(coords, dc):
    res = []
    for c in coords:
        res.append((c[0] + dc[0], c[1] + dc[1]))
    return res

def subtract(coords, dc):
    res = []
    for c in coords:
        res.append((c[0] - dc[0], c[1] - dc[1]))
    return res

def normalize(coords):
    minx, miny = 1000, 1000
    for c in coords:
        minx = min(minx, c[0])
        miny = min(miny, c[1])

    return subtract(coords, (minx, miny))


"""
tfPieces = [ {symmetry: coordinates} for each piece ] 
"""
tfPieces = []
for pieceCoords, symmetries, _ in pieces:
    transformedCoordss = {}
    for symm in symmetries:
        coords = pieceCoords
        for a in symm:
            if a == "e":
                continue
            elif a == "R":
                coords = rotate(coords)
            elif a == "F":
                coords = flip(coords)

        coords = normalize(coords)
        transformedCoordss[symm] = coords
    tfPieces.append(transformedCoordss)


def drawPiece(coords):
    minx, miny = 1000, 1000
    maxx, maxy = -1000, -1000

    for c in coords:
        minx = min(minx, c[0])
        miny = min(miny, c[1])
        maxx = max(maxx, c[0])
        maxy = max(maxy, c[1])

    for y in range(miny-1, maxy + 2):
        entr = ["X" if (x,y) in coords else " " for x in range(minx-1, minx + 6)]
        row = ['{0: <3}'.format(str(x)) for x in entr]
        print("".join(row))


def testDraw():
    for piece in tfPieces:
        for coords in piece.values():
            drawPiece(coords)
            print("\n\n")


class BlokusState:
    def __init__(self, player, grid, freePieces, skips, lazyAttr):
        self.player = player
        self.grid = grid
        self.freePieces = freePieces  # dict, not list because indexed with player (1 or 2)
        self.skips = skips

        self.lazyAttr = lazyAttr

    @classmethod
    def initial(cls):
        grid = [0 for _ in range(S*S)]
        freePieces = {1: list(range(len(pieces))),
                      2: list(range(len(pieces)))}
        skips = {1: False, 2: False}
        lazyAttr = {1: {"blockedSquares": None, "takenSquares": None, "pivotSquares": None, "actions": None},
                    2: {"blockedSquares": None, "takenSquares": None, "pivotSquares": None, "actions": None}}
        return BlokusState(1, grid, freePieces, skips, lazyAttr)

    def newState(self):
        # TODO rename to deepcopy
        freePiecesCopy = {1: [x for x in self.freePieces[1]],
                               2: [x for x in self.freePieces[2]]}
        return BlokusState(self.otherPlayer(), self.grid.copy(),
                           freePiecesCopy, self.skips.copy(),
                           copy.deepcopy(self.lazyAttr))

    def print(self, viewCoords=True):
        if viewCoords:
            entry = ['{0: <3}'.format(" ")]
            entry += ['{0: <3}'.format(str(x)) for x in range(S)]
            print("".join(entry))
        for y in range(S):
            entr = []
            if viewCoords:
                entr.append(str(y) + " ")
            entr += [self.playerStr(self.getCell(x,y)) for x in range(S)]
            row = ['{0: <3}'.format(str(x)) for x in entr]
            print("".join(row))
        print("")

    def otherPlayer(self):
        return 3-self.player

    def cost(self):
        return (totalSquares - self.count(1), totalSquares - self.count(2))

    def winner(self):
        if not all(self.skips.values()):
            return -1
        else:
            cost = self.cost()
            if cost[1] > cost[0]:
                return 1
            elif cost[0] > cost[1]:
                return 2
            else:
                return 0

    def playerStr(self, player):
        return {1: "X", 2: "O", 0: "."}[player]

    def getCell(self, x, y):
        return self.grid[x+S*y]

    def setCells(self, coords, value):
        """note: should be called on a new state"""
        for (x,y) in coords:
            self.grid[x+S*y] = value

    def count(self, player):
        return self.grid.count(player)

    def onBoard(self, x, y):
        return x >= 0 and y >= 0 and x < S and y < S

    def takenSquares(self, player):
        """set of coordinates taken by player"""
        if self.lazyAttr[player]["takenSquares"]:
            return self.lazyAttr[player]["takenSquares"]

        res = set()
        for x in range(S):
            for y in range(S):
                if self.getCell(x, y) == player:
                    res.add((x, y))

        self.lazyAttr[player]["takenSquares"] = res
        return res

    def pivotSquares(self, player, takenSquares):
        """set of coordinates diagonal to takenSquares of player.
        note: doesn't filter by availability for efficiency"""
        if self.lazyAttr[player]["pivotSquares"]:
            return self.lazyAttr[player]["pivotSquares"]

        res = set()

        if len(takenSquares) == 0:
            if player == 1:
                res = set([(S-1, S-1)])
            else:
                res = set([(0, 0)])
        else:
            for (x,y) in takenSquares:
                res.update([(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)])

        self.lazyAttr[player]["pivotSquares"] = res
        return {c for c in res if self.onBoard(*c)}

    def blockedSquares(self, player, takenSquares):
        if self.lazyAttr[player]["blockedSquares"]:
            return self.lazyAttr[player]["blockedSquares"]

        res = takenSquares.copy()
        for (x,y) in takenSquares:
            res.update([(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)])

        self.lazyAttr[player]["blockedSquares"] = res
        return res

    def availableSquares(self, player, takenSquares):
        return allSquares\
            .difference(self.blockedSquares(player, takenSquares))\
            .difference(self.takenSquares(3-player))

    def actions(self, player=None):
        res = []  # (pieceId, symmetry, coordinate)
        res.append('pass')
        if player is None:
            player = self.player
        takenSquares = self.takenSquares(player)
        availableSquares = self.availableSquares(player, takenSquares)
        pivotSquares = self.pivotSquares(player, takenSquares)

        for pivot in pivotSquares:
            if pivot not in availableSquares:
                continue

            for pieceId in self.freePieces[player]:
                for symmetry in tfPieces[pieceId].keys():
                    coords = tfPieces[pieceId][symmetry]

                    for localPivot in coords:
                        translatedCoords = subtract(coords, localPivot)
                        globalCoords = add(translatedCoords, pivot)

                        if all([c in availableSquares for c in globalCoords]):
                            place = (pivot[0]-localPivot[0], pivot[1]-localPivot[1])
                            # eg. if piece is [(0,0), (1,0), (0,1), (1,1)] and the bottom right
                            # corner is used as pivot, ie. localPivot (1,1).
                            # The move is identified with place (0,0)
                            # Now place + tfPieces[pieceId][symmetry]
                            # gives the global coordinates of the placed piece
                            # place = (pivot[0] - localPivot[0], pivot[1] - localPivot[1])
                            res.append((pieceId, symmetry, place, set(globalCoords)))

        self.lazyAttr[player]["actions"] = res
        return res

    @staticmethod
    def actionStr(action):
        if action == 'pass':
            return action
        else:
            pieceId, symmetry, place, _ = action
            if symmetry == "e":
                symmetryStr = ""
            else:
                symmetryStr = f"({symmetry}) "
            return f"{pieces[pieceId][2]} {symmetryStr}at {place}"


    def successor(self, action):
        if action != 'pass':
            pieceId, symmetry, place, _ = action
            sstate = self.newState()
            localCoords = tfPieces[pieceId][symmetry]
            globalCoords = add(localCoords, place)

            sstate.setCells(globalCoords, self.player)
            sstate.freePieces[self.player] = [a for a in self.freePieces[self.player]
                                              if a != pieceId]
            sstate.skips[self.player] = False
            sstate.updatelazyAttr(self.player, globalCoords)
            return sstate

        else:
            sstate = self.newState()
            sstate.skips[self.player] = True
            return sstate

    def updatelazyAttr(self, player, globalCoords):
        globalCoords = set(globalCoords)
        # note: attributes unchanged by other player's moves
        def updateTakenSquares():
            self.lazyAttr[player]["takenSquares"] = \
                self.lazyAttr[player]["takenSquares"].union(globalCoords)

        def updateBlockedSquares():
            blockedCoords = set()
            for (x, y) in globalCoords:
                blockedCoords.update([(x - 1, y), (x, y + 1),
                                       (x + 1, y), (x, y - 1)])
            self.lazyAttr[player]["blockedSquares"] = \
                self.lazyAttr[player]["blockedSquares"].union(blockedCoords)

        def updatePivotSquares():
            pivotCoords = set()
            for (x, y) in globalCoords:
                pivotCoords.update([(x - 1, y - 1), (x + 1, y + 1),
                                    (x + 1, y - 1), (x + 1, y - 1)])
            self.lazyAttr[player]["pivotSquares"] = \
                self.lazyAttr[player]["pivotSquares"].union(pivotCoords)

        def updateActions():
            # TODO
            pass

        updateTakenSquares()
        updateBlockedSquares()
        updatePivotSquares()
        updateActions()
