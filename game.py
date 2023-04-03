class Pawn:

    def available_moves(self, game, pos):
        i,j = pos
        color = game.player

        # whites goes up 
        if color == 0:
            posibilities = []
            # + 1
            if game.in_board((i+1,j)) and game.pos_empty((i+1,j)):
                posibilities.append((i+1,j))
                # + 2
                if i == 1 and game.pos_empty((i+2,j)): 
                    posibilities.append((i+2,j))
            # eat left
            if j != 0 and game.in_board((i+1,j-1)) and not game.pos_empty((i+1,j-1)) and not game.same_color((i,j),(i+1,j-1)): 
                posibilities.append((i+1,j-1))
            # eat right
            if j != 7 and game.in_board((i+1,j+1)) and not game.pos_empty((i+1,j+1)) and not game.same_color((i,j),(i+1,j+1)):
                posibilities.append((i+1,j+1))

        # blacks goes left (down)
        else:
            posibilities = []
            # + 1
            if game.in_board((i-1,j)) and game.pos_empty((i-1,j)):
                posibilities.append((i-1,j))
                # + 2
                if i == 6 and game.pos_empty((i-2,j)): 
                    posibilities.append((i-2,j))
            # eat left
            if j != 0 and game.in_board((i-1,j-1)) and not game.pos_empty((i-1,j-1)) and not game.same_color((i,j),(i-1,j-1)): 
                posibilities.append((i-1,j-1))
            # eat right 
            if j != 7 and game.in_board((i-1,j+1)) and not game.pos_empty((i-1,j+1)) and not game.same_color((i,j),(i-1,j+1)):
                posibilities.append((i-1,j+1))

        return posibilities

class Rook:

    def available_moves(self, game, pos):
        i,j = pos
        posibilities = []

        # left (west)
        for n, k in enumerate(range(j-1,-1,-1)):
            if game.pos_empty((i,k)):
                posibilities.append((i,k))
            else:
                if not game.same_color((i,j), (i,k)):
                    posibilities.append((i,k))
                break

        # right (est)
        for n, k in enumerate(range(j+1,8)):
            if game.pos_empty((i,k)):
                posibilities.append((i,k))
            else:
                if not game.same_color((i,j), (i,k)):
                    posibilities.append((i,k))
                break

        # up (north)
        for n, k in enumerate(range(i+1,8)):
            if game.pos_empty((k,j)):
                posibilities.append((k,j))
            else:
                if not game.same_color((i,j), (k,j)):
                    posibilities.append((k,j))
                break

        # down (suth)
        for n, k in enumerate(range(i-1,-1,-1)):
            if game.pos_empty((k,j)):
                posibilities.append((k,j))
            else:
                if not game.same_color((i,j), (k,j)):
                    posibilities.append((k,j))
                break

        return posibilities

class Knight:

    def available_moves(self, game, pos):
        i,j = pos
        availables = [
            (i+2,j-1),
            (i+2,j+1),
            (i-2,j-1),
            (i-2,j+1),
            (i-1,j-2),
            (i+1,j-2),
            (i-1,j+2),
            (i+1,j+2)
        ]

        posibilities = [a for a in availables if game.in_board(a) and (game.pos_empty(a) or not game.same_color(pos,a))]

        return posibilities

class Bishop:

    def available_moves(self, game, pos): 
        i,j = pos
        posibilities = []

        # left + up
        for k in range(1,min(8-i,j+1)):
            if game.pos_empty((i+k,j-k)):
                posibilities.append((i+k,j-k))
            else:
                if not game.same_color((i,j),(i+k,j-k)):
                    posibilities.append((i+k,j-k))
                break

        # left + down
        for k in range(1,min(i+1,j+1)):
            if game.pos_empty((i-k,j-k)):
                posibilities.append((i-k,j-k))
            else:
                if not game.same_color((i,j),(i-k,j-k)):
                    posibilities.append((i-k,j-k))
                break

        # right + up
        for k in range(1,min(8-i,8-j)):
            if game.pos_empty((i+k,j+k)):
                posibilities.append((i+k,j+k))
            else:
                if not game.same_color((i,j),(i+k,j+k)):
                    posibilities.append((i+k,j+k))
                break

        # right + down
        for k in range(1,min(i+1,8-j)):
            if game.pos_empty((i-k,j+k)):
                posibilities.append((i-k,j+k))
            else:
                if not game.same_color((i,j),(i-k,j+k)):
                    posibilities.append((i-k,j+k))
                break

        return posibilities

class Queen:

    def __init__(self):
        self.bishop = Bishop()
        self.rook = Rook()

    def available_moves(self, game, pos):
        p1 = self.bishop.available_moves(game, pos)
        p2 = self.rook.available_moves(game, pos)
        return p1 + p2

class King:

    def available_moves(self, game, pos):
        i,j = pos
        available = [
            (i+1,j),
            (i-1,j),
            (i,j+1),
            (i,j-1),
            (i+1,j+1),
            (i-1,j-1),
            (i-1,j+1),
            (i+1,j-1),
        ]

        posibilities = [a for a in available if game.in_board(a) and (game.pos_empty(a) or not game.same_color(pos,a))]
                
        return posibilities

        
class Game:

    def __init__(self):
        self.history = True
        self.colors  = {0:"white", 1:"black"}
        self.names   = {0:"pawn", 1:"bishop", 2:"knight", 3:"rook", 4:"queen", 5:"king"}
        self.chips   = {0:Pawn(), 1:Bishop(), 2:Knight(), 3:Rook(), 4:Queen(), 5:King()}
        self.empty   = (-1,-1)
        self.reset_game()

    # we suposed that the movement is valid (we take care of this in a previous step)
    def move(self, pos, target_pos):
        self.last_move = (pos, target_pos)
        chip = self.board[pos[0]][pos[1]]
        i,j = target_pos
        if not self.pos_empty(target_pos):
            target_chip = self.board[i][j]
            self.board_chips[target_chip[0]].remove(target_pos)
            if target_chip[1] == 5:
                self.end_game = True
        self.board_chips[self.player].remove(pos)
        self.board_chips[self.player].append(target_pos)
        self.board[pos[0]][pos[1]] = self.empty
        self.board[i][j] = chip
        self.player = 0 if self.player == 1 else 1
        self.depth += 1

    # check if the position "pos" is empty
    def pos_empty(self, pos):
        i,j = pos
        return self.board[i][j] == self.empty

    # check if the 2 chips (in "pos" and "pos2") are of the same color
    def same_color(self, pos1, pos2):
        return self.board[pos1[0]][pos1[1]][0] == self.board[pos2[0]][pos2[1]][0]

    # check if the position "pos" is on board (range betwen 0 and 7)
    def in_board(self, pos):
        if pos[0] in range(8) and pos[1] in range(8):
            return True
        return False

    # check if a chip can move into a certain position
    def is_posible_to_move(self, chip, pos):
        i,j = pos
        actual_chip = self.board[i][j]
        if actual_chip == self.empty or actual_chip[0] != chip[0]:
            return True
        return False
    
    # reset game, all the chips and variables
    def reset_game(self):

        self.last_move = None
        self.end_game = False
        self.depth = 0
        self.board = [[self.empty for _ in range(8)] for _ in range(8)]
        self.player = 0
        self.board_chips = [[(i,j) for i in [0,1] for j in range(8)], [(i,j) for i in [6,7] for j in range(8)]]

        # pawn
        self.board[1] = [(0,0) for _ in range(8)]
        self.board[6] = [(1,0) for _ in range(8)]
        # bishop
        self.board[0][2] = (0,1)
        self.board[0][5] = (0,1)
        self.board[7][2] = (1,1)
        self.board[7][5] = (1,1)
        # knight
        self.board[0][1] = (0,2)
        self.board[0][6] = (0,2)
        self.board[7][1] = (1,2)
        self.board[7][6] = (1,2)
        # rook
        self.board[0][0] = (0,3)
        self.board[0][7] = (0,3)
        self.board[7][0] = (1,3)
        self.board[7][7] = (1,3)
        # quen
        self.board[0][3] = (0,4)
        self.board[7][4] = (1,4)
        # quen
        self.board[0][4] = (0,5)
        self.board[7][3] = (1,5)

    def print(self):
        sep = "\n\t---------------------------------\n\t"
        s = sep + "| "
        for row in self.board:
            for e in row:
                if e == self.empty:
                    s += "  | "
                elif e[0] == 0:
                    s += "+ | "
                else:
                    s += "o | "
            s += sep + "| "
        print(s[:-3])

