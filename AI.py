import copy
from Gomoku import *


class AI():
    """
    A AI class has search function and heuristic fucntion, it can return
    the a (x,y) position ai would go next by running next_step
    """
    def __init__(self,turn,hardness,h_fun,s_fun):
        """
        Create a new AI

        @param hardness: string representation of hardness
        @param turn: either 1 or 2(1:black :2:white)
        @param h_fun: heuristic function it uses
        @param s_fun: search function it uses
        """
        self.hardness = hardness
        self.turn = turn
        self.h_fun = h_fun
        self.s_fun = s_fun

    def next_step(self,node):
        """
        Using s_fun with heuristic function to get next step on the given
        board,return a (x,y) position the next step should be

        @param node: a given board state
        """

        return self.s_fun(self.h_fun,node)


################### Simple Search ###########################
def simple_search(h_fun,node):
    """
    A simple search basicly using h_fun to compare the value increase if put a stone
    at a empty spot and compare all of them to choose the maximum pos, and add that
    stone to the board

    @param h_fun: heuristic function
    @param node: a given gomuku node
    """

    result = copy.deepcopy(node)
    max_her = -9999999
    check = 0
    ideal = None

    for t in node.reduced_successors():
        result.addstone(t[0],t[1])
        after = h_fun(result)
        if after > max_her:
            max_her = after
            ideal = t
        result.remove_stone(t[0],t[1])

    if ideal != None:
        result.addstone(ideal[0],ideal[1])
    return result

################### Minmax Search ###########################

def minmax(h_fun,state):
    """
    GAME-TREE SEARCH
    """
    max_num = -float('inf')
    depth = 2
    node = copy.deepcopy(state)


    if len(state.stones) < 1:
        mid = int(round(state.boardsize/2))
        position = (mid,mid)
        if state.board[mid][mid] != 0:
            position = (mid-1,mid)
    else:

        for t in node.reduced_successors():
            node.visited += 1
            node.addstone(t[0],t[1])
            result = find_best(node,state.turn,h_fun,depth)

            if result > max_num:
                position = t
                max_num = result
            node.remove_stone(t[0],t[1])
    if position != None:
        node.addstone(position[0],position[1])

    print("Node visited : {}".format(node.visited))

    return node


def find_best(node,turn,h_fun,depth):
    if depth == 0:
        if node.turn == turn:
            return -h_fun(node)
        else:
            return h_fun(node)

    winner = detect_winner(node.board)
    if winner == 1:
        return -float('inf')
    elif winner == 2:
        return float('inf')
    else:
        minimize = float('inf')
        maximize = -float('inf')
        if turn == node.turn:
            succ = node.reduced_successors()
        else:
            succ = node.successors()
        for t in succ:
            node.visited += 1
            node.addstone(t[0],t[1])
            result = find_best(node,turn,h_fun,depth-1)
            if result < minimize:
                minimize = result
            if result > maximize:
                maximize = result
            node.remove_stone(t[0],t[1])

        if turn == node.turn:
            return maximize
        return minimize


#######
def minmax_alpha_beta(h_fun,state):
    """
    return next move based on minmax algorithm
    """
    position = None
    max_num = -float('inf')
    depth = 2

    node = copy.deepcopy(state)

    if len(state.stones) < 1:
        mid = int(round(state.boardsize/2))
        position = (mid,mid)
        if state.board[mid][mid] != 0:
            position = (mid-1,mid)
    else:
        alpha = -float('inf')
        beta = float('inf')
        for t in node.reduced_successors():
            node.visited += 1
            node.addstone(t[0],t[1])
            result = min_check(node,state.turn,h_fun,depth,alpha,beta) #####
            if result > max_num:
                position = t
                max_num = result
            node.remove_stone(t[0],t[1])
    if position != None:
        node.addstone(position[0],position[1])
    print("Node visited : {}".format(node.visited))
    return node


def min_check(node,turn,h_fun,depth,alpha,beta):
    if depth == 0:
        if node.turn == turn:
            return -h_fun(node)
        else:
            return h_fun(node)

    winner = detect_winner(node.board)
    if winner == 1:
        return -float('inf')
    elif winner == 2:
        return float('inf')
    else:
        result = float('inf')
        succ = node.successors()
        for t in succ:
            node.addstone(t[0],t[1])
            node.visited += 1
            re = max_check(node,turn,h_fun,depth-1,alpha,beta)
            if re < result:
                result = re
            if result <= alpha:
                node.remove_stone(t[0],t[1]) # cut
                return result
            if result < beta:
                beta = result
            node.remove_stone(t[0],t[1])
        return result

def max_check(node,turn,h_fun,depth,alpha,beta):
    if depth == 0:
        if node.turn == turn:
            return -h_fun(node)
        else:
            return h_fun(node)

    winner = detect_winner(node.board)
    if winner == 1:
        return -float('inf')
    elif winner == 2:
        return float('inf')
    else:
        result = -float('inf')
        succ = node.reduced_successors()
        for t in succ:
            node.visited += 1
            node.addstone(t[0],t[1])
            re = min_check(node,turn,h_fun,depth-1,alpha,beta)
            if re > result:
                result = re
            if result >= beta:
                node.remove_stone(t[0],t[1]) # cut
                return result
            if result > alpha:
                alpha = result
            node.remove_stone(t[0],t[1])
        return result

################### Helper Method ###########################################
def detect_winner(chess):
    """
    detect if the game has a winner, return 0 if no winner,1 if black win
    2,if white win

    """
    for i in range(15):
        for j in range(15):
            if(detect_point(chess,i,j)!=0):
                return detect_point(chess,i,j)
    return 0
def detect_point(chess,x,y):
    """
    A helper function that used by detect_winner, detect winner on singe point

    """
    c = chess[x][y]
    if x- 4 >= 0:
        if chess[x-1][y] == c and chess[x-2][y] == c and \
        chess[x-3][y] == c and chess[x-4][y] == c:
            return c
        if y - 4 >= 0:
            if chess[x-1][y-1] == c and chess[x-2][y-2] == c and \
            chess[x-3][y-3] == c and chess[x-4][y-4] == c:
                return c
        if y + 4 <= 14:
            if chess[x-1][y+1] == c and chess[x-2][y+2] == c and \
            chess[x-3][y+3] == c and chess[x-4][y+4] == c:
                return c
    if x+ 4 <= 14:
        if chess[x+1][y] == c and chess[x+2][y] == c and \
        chess[x+3][y] == c and chess[x+4][y] == c:
            return c
        if y - 4 >= 0:
            if chess[x+1][y-1] == c and chess[x+2][y-2] == c and \
            chess[x+3][y-3] == c and chess[x+4][y-4] == c:
                return c
        if y + 4 <= 14:
            if chess[x+1][y+1] == c and chess[x+2][y+2] == c and \
            chess[x+3][y+3] == c and chess[x+4][y+4] == c:
                return c
    if y+ 4 <= 14:
        if chess[x][y+1] == c and chess[x][y+2] == c and   \
        chess[x][y+3] == c and chess[x][y+4] == c:
            return c
    if y- 4 >= 0:
        if chess[x][y-1] == c and chess[x][y-2] == c and   \
        chess[x][y-3] == c and chess[x][y-4] == c:
            return c
    return 0

################### Simple heurstic function########################
def simple_heurstic(node):
    """
    A simple heurstic basicly evualte the current board for player, return a
    postive number if palyer has advantage,negative otherwise

    @param node: a given GomokuState
    @param player: a given player
    """
    result = 0
    chess = node.board
    for stone in node.stones:
        result += sim_on_one(chess,stone[0],stone[1])
    if node.turn == 2: # the player took last_stone
        result = - result
    return result


def sim_on_one(chess,y,x):
    """
    evualte the pos x,y and return a heurstic value

    @param chess: a given chess board
    @param x: a given x pos
    @param y: a given y pos

    """
    op = 1
    ## oppent is 1:black or 2: white
    sf = 2
    ## self is 1:black or 2: white
    tf = True
    ## tf indicate if i should count it as a negative value or postive value
    ## if it is false, then heurstic value should be a negative value
    blocked = False
    ## blocked indicate if this stone has no way of formming 5 stone
    result = 0
    ## result is the heuristic value
    if chess[y][x] == 1:
        ## if we are evlate oppent, then the value should be negative
        sf = 1
        op = 2
        tf = False
    if x -1 >= 0 and x +5<=14 and chess[y][x-1] == op and chess[y][x+5] == op:
        blocked = True
    if x -5 >= 0 and x +1<=14 and chess[y][x-5] == op and chess[y][x+1] == op:
        blocked = True
    if y -5 >= 0 and y +1<=14 and chess[y-5][x] == op and chess[y+1][x] == op:
        blocked = True
    if y -1 >= 0 and y +5<=14 and chess[y-1][x] == op and chess[y+5][x] == op:
        blocked = True
    if blocked:
        return 0;
    if x- 4 >= 0:
        te = True
        if x+1 >14 or chess[y][x+1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y][x-i] == sf:
                point += 1
            if chess[y][x-i] == 0:
                empty += 1
            if chess[y][x-i]  == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if x+ 4 <= 14:
        te = True
        if x-1 <0 or chess[y][x+1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y][x+i] == sf:
                point += 1
            if chess[y][x+i] == 0:
                empty += 1
            if chess[y][x+i] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if y+ 4 <= 14:
        te = True
        if y-1 <0 or chess[y-1][x] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y+i][x] == sf:
                point += 1
            if chess[y+i][x] == 0:
                empty+= 1
            if chess[y+i][x] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if y- 4 >= 0:
        te = True
        if y+1 > 14 or chess[y+1][x] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y-i][x] == sf:
                point += 1
            if chess[y-i][x] == 0:
                empty+= 1
            if chess[y-i][x] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if x- 4 >= 0 and  y- 4 >= 0:
        te = True
        if x+1 > 14 or chess[y][x+1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y-i][x-i] == sf:
                point += 1
            if chess[y-i][x-i] == 0:
                empty+= 1
            if chess[y-i][x-i] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if x- 4 >= 0 and  y+ 4 <= 14:
        te = True
        if x+1 >14 or y-1 < 0 or chess[y-1][x+1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y+i][x-i] == sf:
                point += 1
            if chess[y+i][x-i] == 0:
                empty += 1
            if chess[y+i][x-i] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if x+ 4 <= 14 and  y+ 4 <= 14:
        te = True
        if x-1 <0 or y-1< 0 or chess[y-1][x-1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y+i][x+i] == sf:
                point += 1
            if chess[y+i][x+i] == 0:
                empty += 1
            if chess[y+i][x+i] == op:
                con = False
                break

        result += her_value(con,point,empty,te)
    if x+ 4 <= 14 and  y- 4 >= 0:
        te = True
        if x-1 <0 or y+1 >14 or chess[y+1][x-1] == op:
            te = False
        con = True
        point = 1
        empty = 0
        for i in range(1,5):
            if chess[y-i][x+i] == sf:
                point += 1
            if chess[y-i][x+i] == 0:
                empty += 1
            if chess[y-i][x+i] == op:
                con = False
                break
        result += her_value(con,point,empty,te)

    if not tf:
        if result >100:
            result += 100
        result = -result
    return result
def her_value(con,point,empty,te):
    """
    evualte a bunch of stone given condition

    @param con: true if stones are continues,false otherwise
    @param point: how many stones(not include oppopent's stone) on a direction
    @param empty: how many empty space between stones
    @param te: ture if it is blocked on the other side ,false otherwise

    """
    if point == 5:
        return 500
    if not te and not con:
        return 0
    if not te:
        if point == 4 :
            return 300
        else:
            return point + empty

    if te and con:
        if point == 4:
            return 200
        if point == 3:
            return 150
        if point == 2:
            return 5
        if point == 1:
            return 1
    if te and not con:
        if empty == 0:
            if point == 4:
                return 100
            if point == 3:
                return 5
            else:
                return point
        else:
            if point == 4:
                return 200
            if point ==3:
                return 100
    return 0


def check_empty(chess,i,j):
    """
    return True if x,y is empty and no stone are nearby,false otherwise
    @param chess: a given gomuku state
    @param x: x pos of empty
    @param x: y pos of empty
    """

    if j!=0 and j != 14:
        if i != 0 and i != 14:
            tf = True
            if chess[j+1][i] != 0:
                tf = False
            if chess[j+1][i-1] != 0:
                tf = False
            if chess[j+1][i+1] != 0:
                tf = False
            if chess[j][i-1] != 0:
                tf = False
            if chess[j][i+1] != 0:
                tf = False
            if chess[j-1][i-1] != 0:
                tf = False
            if chess[j-1][i] != 0:
                tf = False
            if chess[j-1][i+1] != 0:
                tf = False
    return tf
