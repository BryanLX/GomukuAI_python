from Tkinter import *
import os
import subprocess
import time
from AI import *



winner = 0


class Window(Frame):
    def __init__(self, master = None):
        """
        init a game window

        """
        Frame.__init__(self,master)


        self.board_start_x = 176
        self.board_start_y = 28
        ## turn is True if it is player's turn,false otherwise
        self.state = None
        ## state is the cur  board state
        self.AI = "EASY"
        self.AI_pool = []
        self.AI_pool.append(AI("Simple-1",2,simple_heurstic,simple_search))
        self.AI_pool.append(AI("Simple-2",1,simple_heurstic,simple_search))
        self.AI_pool.append(AI("Normal-1",2,simple_heurstic,minmax_alpha_beta))
        self.AI_pool.append(AI("Normal-2",1,simple_heurstic,minmax_alpha_beta))
        ## AI_pool contain all the AI class,with easy as first,normal as seconds
        ## master as third
        ## the cur AI fucntion used
        self.AI_cur = None
        self.AI_next = None
        self.board = None
        self.master = master
        self.side = None
        self.init_window()

    def init_window(self):
        """
        restart a window and fill the board

        """
        self.master.title("Gomuku")
        self.state = GomokuState(turn=p1,boardsize=15)

        self.pack(fill = BOTH,expand = 1)
        board = Canvas(self.master,width= 700,height =540,bd=0, highlightbackground="black",highlightcolor="black", highlightthickness=2)
        side = Canvas(self.master,width = 160,height = 540,bd=0,highlightbackground="black",highlightcolor="black", highlightthickness=2)
        side.place(x=700,y=0)
        side.create_image(0,0,anchor = NW,image =right )
        self.side = side
        self.board = board
        board.pack()
        board.place(x = 0,y = 0)
        board.create_image(0,0,anchor = NW,image = background)
        board.create_image(140,-10,anchor = NW,image = photo)
        self.fill_char()
        self.fill_menu()
        self.AI_cur = self.AI_pool[0]

    def fill_menu(self):
        """
        draw the left menu

        """
        self.board.create_text(20,60,anchor = NW,fill="black",activefill = "white",font="Herculanum 30 italic bold",text="Gomuku")
        self.board.create_text(20,140,anchor = NW,fill="black",activefill = "white",font="Luminari 20 italic",text="Simple-1")
        self.board.create_text(20,220,anchor = NW,fill="black",activefill = "white",font="Luminari 20 italic",text="Simple-2")
        self.board.create_text(20,300,anchor = NW,fill="black",activefill = "green",font="Luminari 20 italic",text="Normal-1")
        self.board.create_text(20,380,anchor = NW,fill="black",activefill = "red",font="Luminari 20 italic",text="Normal-2")
        self.board.create_text(20,460,anchor = NW,fill="black",activefill = "white",font="Luminari 20 italic",text="Quit")

    def fill_char(self,result = 0):
        """
        draw the char

        """
        self.side.delete(ALL)
        self.side.create_image(0,0,anchor = NW,image =right )
        self.side.create_image(120,160,anchor = NW,image = white)
        self.side.create_image(120,420,anchor = NW,image = black)
        self.side.create_image(40,180,anchor = NW,image = vs)
        AI = char2
        if self.AI == "Master":
            AI = char2
        if self.AI == "Normal":
            AI = char3
        if self.AI == "Easy":
            AI = char4
        if result ==0:
            self.side.create_image(0,0,anchor = NW,image =AI[0] )
            self.side.create_image(0,260,anchor = NW,image =char1[0] )
        elif result ==1:
            self.side.create_image(0,0,anchor = NW,image =AI[2] )
            self.side.create_image(0,260,anchor = NW,image =char1[1] )
        else:
            self.side.create_image(0,0,anchor = NW,image =AI[1] )
            self.side.create_image(0,260,anchor = NW,image =char1[2] )
        self.side.create_text(20,160,anchor = NW,fill="black",activefill = "white",font="Times 20 italic bold",text=self.AI)
        self.side.create_text(20,420,anchor = NW,fill="black",activefill = "white",font="Times 20 italic bold",text="Player")
        self.side.create_text(20,450,anchor = NW,fill="black",activefill = "white",font="Times 15 italic bold",text="Current AI = "+self.AI)
        self.side.create_text(20,500,anchor = NW,fill="black",activefill = "white",font="Times 20 italic bold",text="AI: 0")
        self.side.create_text(20,520,anchor = NW,fill="black",activefill = "white",font="Times 20 italic bold",text="Player: 0")

    def client_exit(self):
        exit()

    def draw_board(self):
        """
        clean the board first then redraw the board

        """
        self.clean()
        chess = self.state.board
        for i in range(15):
            for j in range(15):
                if chess[i][j] == 1:
                    self.draw_point("black",j,i)
                if chess[i][j] == 2:
                    self.draw_point("white",j,i)
        result = self.detect_winner()
        if(result!=0):
            if (result ==1):
                ##subprocess.Popen(["afplay", "./sound/wining.wav"])
                self.fill_char(result = 1)
                # self.reset()
            else:
                ##subprocess.Popen(["afplay", "./sound/lose.wav"])
                self.fill_char(result = 2)
                # self.reset()
        return result



    def detect_winner(self):
        """
        detect if the game has a winner, return 0 if no winner,1 if black win
        2,if white win

        """
        for i in range(15):
            for j in range(15):
                if(self.detect_point(i,j)!=0):
                    return self.detect_point(i,j)
        return 0

    def detect_point(self,x,y):
        """
        A helper function that used by detect_winner, detect winner on singe point

        """
        chess = self.state.board
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

    def draw_point(self,colour,x,y):
        """
        A helper function to draw a stone on a board

        @param colour: the colour of stone
        @param x: x pos
        @param y: y pos
        """
        pos_x = self.board_start_x+x*35
        pos_y = self.board_start_y+y*35
        if colour == "black":
            self.board.create_image(pos_x-15,pos_y-15,anchor = NW,image = black)
        if colour == "white":
            self.board.create_image(pos_x-15,pos_y-15,anchor = NW,image = white)

    def clean(self):
        """
        clean the board

        """
        self.board.delete(ALL)
        # board = Canvas(self.master,width= 700,height =540)
        # self.board = board
        # board.pack()
        self.board.place(x = 0,y = 0)
        self.board.create_image(0,0,anchor = NW,image = background)
        self.board.create_image(140,-10,anchor = NW,image = photo)
        self.fill_menu()
        self.fill_char(result =0)


    def reset(self,preinstall=None):
        """
        reset the board and set the diffculy to easy

        """
        # self.state = GomokuState(turn=p1,boardsize=15)
        self.state = GomokuState(preinstall=preinstall)
        global winner
        winner = 0
        self.draw_board()
        self.function = self.AI_pool[0]
def left_click(event):
    """
    this function is called when a left click event happen.
    it will detect the area where mouse click and respond to it

    """
    global winner

    if event.x > 20 and event.x <140 and event.y>140 and event.y <180:
        app.AI_cur = app.AI_pool[0]
        app.fill_char()
        app.reset()
        # app.AI_next = app.AI_pool[1]
        # find first hand


    elif event.x >20 and event.x <140 and event.y > 220 and event.y < 260:
        app.AI_cur = app.AI_pool[1]
        app.fill_char()
        app.reset()
        start_time = os.times()[0]

        app.state = app.AI_cur.next_step(app.state)
        stop_time = os.times()[0]

        print("AI choose to put : " + str(app.state.last_stone))
        print("AI used {} seconds ".format(stop_time-start_time))

        winner = app.draw_board()

    elif event.x >20 and event.x <140 and event.y > 300 and event.y < 340:
        app.AI_cur = app.AI_pool[2]
        app.fill_char()
        app.reset()
    elif event.x >20 and event.x <140 and event.y > 380 and event.y < 420:
        app.AI_cur = app.AI_pool[3]
        app.fill_char()
        app.reset()
        start_time = os.times()[0]

        app.state = app.AI_cur.next_step(app.state)
        stop_time = os.times()[0]

        print("AI choose to put : " + str(app.state.last_stone))
        print("AI used {} seconds ".format(stop_time-start_time))

        winner = app.draw_board()


    elif event.x > 155 and event.x <679 and event.y >12 and event.y <523:
        if winner != 0:
            return
        if not app.AI_next:
            pos = convert_location(event.x,event.y)
            if pos!= None:
                if (pos[1],pos[0]) in app.state.stones:
                    return
                app.state.addstone(pos[1],pos[0])

                winner = app.draw_board()
        else: # vs ai
            start_time = os.times()[0]

            app.state = app.AI_next.next_step(app.state)
            stop_time = os.times()[0]

            print("AI choose to put : " + str(app.state.last_stone))
            print("AI used {} seconds ".format(stop_time-start_time))

            winner = app.draw_board()

        if winner != 0:
            return

        # ai second hand
        start_time = os.times()[0]

        app.state = app.AI_cur.next_step(app.state)
        stop_time = os.times()[0]

        print("AI choose to put : " + str(app.state.last_stone))
        print("AI used {} seconds ".format(stop_time-start_time))

        winner = app.draw_board()

    elif event.x > 20 and event.x < 140 and event.y > 460 and event.y <500:
        exit()

    else:
        return

def convert_location(mouse_x,mouse_y):
    px = (mouse_x-app.board_start_x)//35
    py = (mouse_y-app.board_start_y)//35
    if inside_area(px,py,mouse_x,mouse_y):
        return (px,py)
    elif inside_area(px+1,py,mouse_x,mouse_y):
        return (px+1,py)
    elif inside_area(px+1,py+1,mouse_x,mouse_y):
        return (px+1,py+1)
    elif inside_area(px,py+1,mouse_x,mouse_y):
        return (px,py+1)
    else :
        return None

def inside_area(x,y,mouse_x,mouse_y):
    if mouse_x > (app.board_start_x+x*35-15) and mouse_x < (app.board_start_x+x*35+15):
        if mouse_y >(app.board_start_y+y*35-15) and mouse_y < (app.board_start_y+y*35+15):
            return True
    return False

def right_click(event):
    app.clean()

def move(event):
    print("x :"+ str(event.x) +" y:" + str(event.y))
root = Tk()
root.geometry("860x540")
root.resizable(width = False,height= False)

win_i = 1
wining = PhotoImage(file="img/wining.gif",format = 'gif -index %i' %(win_i))


photo =PhotoImage(file = "img/wuziqi.gif")
background = PhotoImage(file = "img/background.gif")
white =PhotoImage(file = "img/white.gif")
black =PhotoImage(file = "img/black.gif")
right = PhotoImage(file = "img/right.gif")
vs = PhotoImage(file = "img/vs.gif")
char1 = [PhotoImage(file = "img/char1_1.gif"),PhotoImage(file = "img/char1_2.gif"),PhotoImage(file = "img/char1_3.gif")]
char2 = [PhotoImage(file = "img/char2_1.gif"),PhotoImage(file = "img/char2_2.gif"),PhotoImage(file = "img/char2_3.gif")]
char3 = [PhotoImage(file = "img/char3_1.gif"),PhotoImage(file = "img/char3_2.gif"),PhotoImage(file = "img/char3_3.gif")]
char4 = [PhotoImage(file = "img/char4_1.gif"),PhotoImage(file = "img/char4_1.gif"),PhotoImage(file = "img/char4_1.gif")]
#wining = PhotoImage(file = "img/wining.gif")
app = Window(root)
root.bind("<Button-1>",left_click)
root.bind("<Button-2>",right_click)
# root.bind("<Motion>",move)

root.mainloop()
