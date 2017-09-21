"""Gomoku routines.

    A) Class GomokuState

    A specializion of the StateSpace Class that is tailored to the game of Gomoku.

    B) Class Stone

    A specializion of the stone, either white or black

"""
import copy

p1 = 1  # x
p2 = 2  # O
player = [p1,p2]

class GomokuState():

    def __init__(self,turn=p1,boardsize=15,preinstall=None,last_stone=None):
        """
        Create a new GomokuState

        @param turn: represents whose turn next to place the stone 1:black 2:white
        @param boardsize: the size of the board to generate
        @param preinstall: martrix with 0: empty 1 :black 2:white
        @param last_stone:last_stone position (x,y)
        """
        self.turn = turn
        self.boardsize = boardsize
        self.last_stone = last_stone
        self.stones = dict()
        self.last_last_stone = None

        if not preinstall:
            self.board = [[0 for x in range(boardsize)] for y in range(boardsize)]
        else:
            self.board = preinstall
            for i in range(boardsize):
                for j in range(boardsize):
                    if preinstall[i][j] != 0:
                        self.stones[(i,j)] = True

        #
        self.visited = 0




    def addstone(self,row,col):
        """
        Add a new stone to the game board
        @param row: row position
        @param col: col position
        """
        if self.board[row][col] != 0:
            print("Occupied")
        else:
            self.board[row][col] = self.turn
            self.stones[(row,col)] = True
            self.last_last_stone = self.last_stone
            self.last_stone = (row,col) # -------------------- rememberd last stone
            self.switch_turn()




    def remove_stone(self,row,col):
        """
        helper function, remove a stone from the board
        """
        if self.board[row][col] == 0:
            return

        self.last_stone = self.last_last_stone
        self.stones.pop((row,col))
        self.board[row][col] = 0
        self.switch_turn()

    def collect_current_chess(self):
        """
        collect the current chesses on the board
        """
        rval = []
        for i in range(0,self.boardsize):
            for j in range(0,self.boardsize):
                if self.board[i][j] != 0:
                    rval.append((i,j,self.board[j][i]))
        return rval

    def successors(self):
        """
        remains to be done, generate all successors of the current node based on the turn
        """
        # new_turn = p1
        # if self.turn == p1:
        #     new_turn = p2



        if self.last_stone == None:
            mid = int(round(self.boardsize/2))
            return [(mid,mid)]


        rval = []
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                if self.board[i][j] == 0:
                    rval.append((i,j))
        return rval

    def reduced_successors(self):
        """
        generate all successors connected to at least one of the current node based on the turn
        """
        new_turn = p1
        if self.turn == p1:
            new_turn = p2


        if self.last_stone == None:
            mid = int(round(self.boardsize/2))
            return [(mid,mid)]


        record = dict()
        for t in self.stones:
            i,j = t[0],t[1]
            if self.board[i][j] == 1:
                neighbour = get_neighbours(t)
                for neigh in neighbour:
                    if self.empty_spot(neigh):
                        record[neigh] = True

        rval = []
        for t in record:
            rval.append(t)

        return rval

#################

    def hashable_state(self):
        """
        Return a data item that can be used as a dictionary key to UNIQUELY representation
        """
        return hash(self.board,self.turn)

    def state_string(self):   # ----------------------- fixed
        """
        Return a string representation of this Gomoku when *str* is called
        """
        s = ""
        for i in range(0,self.boardsize):
            if i >= 0:
                s += "\n"
            for j in range(0,self.boardsize):
                if self.board[i][j] == 0:
                    s += "*"
                if self.board[i][j] == 1:
                    s += "x"
                if self.board[i][j] == 2:
                    s += "O"
        return s



    def print_state(self):
        """
        Print the string representation of the state.
        """
        print(self.state_string())

    def switch_turn(self):
        """
        Switch the turn of the player
        """
        if self.turn == p1:
            self.turn = p2
        else:
            self.turn = p1

    def empty(self):
        """
        Return True iff board is empty
        """
        for i in range(self.boardsize):
            for j in range(self.boardsize):
                if chess[i][j]!=0:
                    return False
        return True


    def in_board(self,t):
        """
        Return True iff t is in the board
        """
        return t[0] in range(0,self.boardsize) and t[1] in range(0,self.boardsize)

    def empty_spot(self,t):
        """
        Return True iff t in board and is empty
        """
        return self.in_board(t) and self.board[t[0]][t[1]] == 0





def get_left(t):
    """
    get the left tuple of t
    """
    (i,j) = t
    return (i,j-1)

def get_right(t):
    """
    get the right tuple of t
    """
    (i,j) = t
    return (i,j+1)

def get_top(t):
    """
    get the top tuple of t
    """
    (i,j) = t
    return (i-1,j)

def get_bot(t):
    """
    get the bot tuple of t
    """
    (i,j) = t
    return (i+1,j)

def get_top_left(t):
    """
    get the top left tuple of t
    """
    return get_top(get_left(t))

def get_top_right(t):
    """
    get the top right tuple of t
    """
    return get_top(get_right(t))

def get_bot_left(t):
    """
    get the bot left tuple of t
    """
    return get_bot(get_left(t))

def get_bot_right(t):
    """
    get the bot right tuple of t
    """
    return get_bot(get_right(t))


def get_neighbours(t):
    """
    get the neightbour tuples of t
    """
    rval = []
    rval.append(get_left(t))
    rval.append(get_right(t))
    rval.append(get_top(t))
    rval.append(get_bot(t))
    rval.append(get_top_left(t))
    rval.append(get_top_right(t))
    rval.append(get_bot_left(t))
    rval.append(get_bot_right(t))
    return rval


def next_turn(turn):
    if turn == p1:
        return p2
    else:
        return p1
