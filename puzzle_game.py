'''
    CS5001
    Fall 22
    Final Project
    Zhen LU
'''

import turtle
from turtle import *
import math
import time
import random
import os

class PuzzleGame():
    def __init__(self):  
        '''
            Method -- __init__
                initialize all kinds of attributes for later use
        '''
        super().__init__()
        self.puz_file = "mario.puz"
        self.screen = turtle.Screen()
        self.turtle = turtle.Turtle()
        self.t_thumbnail = turtle.Turtle()
        self.blank = None
        self.blank_index = 0
        self.puzzle_choice = None
        self.lst = []
        self.ordered_index = []
        self.positions = []
        self.reset_pressed = False
        self.image_name = None
        self.xy_num_tile = 0
        self.thumbnail = None
        self.tile_length = 0
        self.half_tile_length = 0
        self.t_num = turtle.Turtle()
        self.turtles = []
        self.shuffled_turtles = []
        self.tiles = []
        self.shuffled_index = None
        self.copy_shuffled_index = []
        self.leader_lst = []
        self.blank_x = None
        self.blank_y = None
        self.click_x = 0  # initialize player's any click with dummy values
        self.click_y = 0
        self.player_name = None
        self.moves = 0
        self.blank_num = 0
        self.click_num = 0
        self.click_num_index = 0
        self.blank_num_index = 0

    def screen_setup(self):
        '''
            Method -- screen_setup
                put on splash screen, title, screen size, etc.
                get player's name and choice of moves
        '''
        self.screen.setup(800, 800)
        self.screen.title("CS5001 Sliding Puzzle Game")
        self.screen.bgcolor("white")
        self.screen.bgpic(os.path.relpath("Resources/splash_screen.gif"))
        time.sleep(3)

        self.player_name = turtle.textinput("CS5001 Puzzle Slide", "Your Name:")
        self.moves_choice = int(turtle.numinput("CS5001 Puzzle Slide - Moves",
                            "Enter the number of moves (chances) you want (5-200)?",
                            None, 5, 200))

    def draw_frames(self):
        '''
            Method -- draw_frames
                draw three rectangular frames for screen set up
        '''
        self.screen.bgpic("nopic")
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.penup()
        t.goto(-350, 300)
        t.pendown()
        t.color("black")
        t.pensize(6)
        for i in range(2):
            t.forward(450)
            t.right(90)
            t.forward(450)
            t.right(90)

        t.penup()
        t.goto(-350, -180)
        t.pendown()
        for i in range(2):
            t.forward(680)
            t.right(90)
            t.forward(100)
            t.right(90)

        t.penup()
        t.goto(330, 300)
        t.pendown()
        t.color("blue")
        for i in range(2):
            t.right(90)
            t.forward(450)
            t.right(90)
            t.forward(190)

    def place_leaders(self):
        '''
            Method -- place_leaders
                place word "leaders" on the up right corner
        '''
        t8 = turtle.Turtle()
        t8.speed(0)
        t8.color("blue")
        t8.pensize(6)
        t8.hideturtle()
        t8.penup()
        t8.goto(150, 255)
        t8.write("Leaders:", font=("Arial", 20, 'bold'))
        t8.pendown()

    def place_leader_names(self):
        '''
            Methond -- place_leader_names
                according to moves, place all players' names in order
                write down error message to 5001_puzzle.err
        '''
        try:
            with open("leaderboard.txt", "r") as sequence:
                lines = sequence.readlines()
                for i in range(len(lines)):
                    line = lines[i].strip('\n').split(":")
                    self.leader_lst.append(line)
            # use the first element (number) of nested list
            # to sort the whole leaders' list
            self.leader_lst.sort(key=lambda x: int(x[0]))

        except FileNotFoundError:
            t_no_leaderboard_file = turtle.Turtle()
            self.screen.addshape(os.path.relpath("Resources/leaderboard_error.gif"))
            t_no_leaderboard_file.shape(os.path.relpath("Resources/leaderboard_error.gif"))
            t_no_leaderboard_file.penup()
            t_no_leaderboard_file.goto(0, 8)
            time.sleep(3)
            t_no_leaderboard_file.hideturtle()

            with open("5001_puzzle.err.txt", "a") as e:
                current_time = time.ctime()
                e.write(f"{current_time}:Error: Could not open leaderboard.txt. "
                        f"LOCATION: game.place_leader_names()\n")
        else:
            # rewrite with sorted moves and leaders' names
            with open("leaderboard.txt", "w") as sorted_content:
                for i in range(len(self.leader_lst)):
                    sorted_content.write(f"{self.leader_lst[i][0]}:{self.leader_lst[i][1]}\n")

            # let turtle with each leader's moves and name go to specific area
            with open("leaderboard.txt", "r") as r:
                lines = r.readlines()
                for i in range(len(lines)):
                    leader = turtle.Turtle()
                    leader.hideturtle()
                    leader.color("blue")
                    leader.speed(0)
                    leader.penup()
                    leader.goto(155, 200 - i * 30)
                    leader.write(lines[i], font=("Arial", 17, 'bold'))

    def place_quitbutton(self):
        '''
            Method -- place_quitbutton
                put the quitbutton on board
                use onclick to pass coordinates to click quitbutton
        '''
        quit_button = turtle.Turtle()  
        quit_button.speed(0)
        quit_button.penup()
        self.screen.addshape(os.path.relpath("Resources/quitbutton.gif"))
        quit_button.shape(os.path.relpath("Resources/quitbutton.gif"))
        quit_button.goto(270, -229)
        quit_button.pendown()
        quit_button.onclick(self.click_quit)

    def click_quit(self, x, y):
        '''
            Method -- click_quit
                if user's click is within the range of quibutton
                a quit message pops up
            Parameters:
                x: user's click's x coordinate on screen
                y: user's click's y coordinate on screen
        '''

        # x, y area of quitbutton
        if 237 <= x <= 304 and -252 <= y <= -210:
            t2 = turtle.Turtle()
            self.screen.addshape(os.path.relpath("Resources/quitmsg.gif"))
            t2.showturtle()
            t2.shape(os.path.relpath("Resources/quitmsg.gif"))
            t2.penup()
            t2.goto(0, 8)
            t2.pendown()
            time.sleep(1)
            self.screen.bye()

    def place_loadbutton(self):
        '''
            Method -- place_loadbutton
                put the loadbutton on board
        '''
        load_button = turtle.Turtle()  
        load_button.hideturtle()
        load_button.speed(0)
        load_button.penup()
        load_button.showturtle()
        self.screen.addshape(os.path.relpath("Resources/loadbutton.gif"))
        load_button.shape(os.path.relpath("Resources/loadbutton.gif"))
        load_button.goto(180, -229)
        load_button.pendown()
        load_button.onclick(self.click_load)

    def click_load(self, x, y):
        '''
            Method -- click_load
                if user's click is within the range of loadbutton
                a textinput window pops up
                and write exception into 5001_puzzle.err
            Parameters:
                x: user's click's x coordinate on screen
                y: user's click's y coordinate on screen
        '''

        # x,y area of loadbutton
        if 144 <= x <= 216 and -264 <= y <= -195:
            t4 = turtle.Turtle()
            t4.penup()
            t4.goto(0, 8)
            t4.pendown()

            self.puz_file = textinput("Load Puzzle",
                                      "Enter the name of the puzzle "
                                      "you wish to load. Choice are:"
                                      "\nluigi.puz\nsmiley,puz\nfifteen.puz"
                                      "\nyoshi.puz\nmario.puz")

            puz_choice_lst = ["luigi.puz", "smiley.puz", "fifteen.puz",
                              "yoshi.puz", "mario.puz"]
            if self.puz_file not in puz_choice_lst:
                self.screen.addshape(os.path.relpath("Resources/file_error.gif"))
                t4.shape(os.path.relpath("Resources/file_error.gif"))
                t4.penup()
                t4.goto(0, 8)
                t4.pendown()
                time.sleep(2)
                t4.hideturtle()

                with open("5001_puzzle.err.txt", "a") as e:
                    current_time = time.ctime()
                    e.write(f"{current_time}:Error: File {self.puz_file} does not exist "
                            f"LOCATION: game.click_load()\n")
                raise FileNotFoundError

            else:
                self.open_file()

                # reset moves to 0 when loading a new puzzle
                self.moves = 0
                self.num_of_moves()

            # clear all the turtles with last puzzle's images
            for i in range(len(self.turtles)):
                self.turtles[i].hideturtle()
                self.turtles[i].reset()

            # set some lists to empty for new puzzle's use
            self.ordered_index = []
            self.positions = []
            self.shuffled_turtles = []
            self.copy_shuffled_index = []

            # recall methods for new puzzle's use
            self.place_tiles()
            self.get_screenclick()

    def open_file(self):
        '''
            Method -- open_file
                read puzzle file to get all the information
                for placing turtles on screen
                default puzzle is mario.puz if player didn't load
                a new puzzle
        '''

        with open(self.puz_file, "r") as f:
            self.lst = []
            for each in f:
                each_line = each.split()
                self.lst.append(each_line)

        # for mario, x is 4, y is 4, for yoshi, x is 2, y is  2
        self.xy_num_tile = int(math.sqrt(int(self.lst[1][1])))
        self.thumbnail = self.lst[3][1]
        self.tile_length = int(self.lst[2][1])

        # each time clear tiles list no matter player loads a
        # new puzzle or not. if he does, tiles list will be cleared
        # and be put in tiles images of new puzzle
        self.tiles = []

        for i in range(len(self.turtles)):
            self.turtles[i].reset()

        # the same reason as clearing tiles list
        self.turtles = []

        # start from line 4 to get the images of tiles
        for i in range(4, len(self.lst)):
            each_tile = self.lst[i]
            self.tiles.append(each_tile)
            self.turtles.append(turtle.Turtle())

    def place_resetbutton(self):
        '''
            Method -- place_resetbutton
                put the resetbutton on board
        '''
        reset_button = turtle.Turtle()  
        reset_button.hideturtle()
        reset_button.speed(0)
        reset_button.penup()
        reset_button.showturtle()
        self.screen.addshape(os.path.relpath("Resources/resetbutton.gif"))
        reset_button.shape(os.path.relpath("Resources/resetbutton.gif"))
        reset_button.goto(85, -229)
        reset_button.pendown()

    def place_tiles(self):
        '''
            Method -- place_tiles
                use shuffled indexes to represent #turtle to ordered place
                place thumbnail here as well
        '''

        # place thumbnail on screen
        self.t_thumbnail.clear()
        self.t_thumbnail.speed(0)
        self.screen.addshape(os.path.relpath(self.thumbnail))
        self.t_thumbnail.shape(os.path.relpath(self.thumbnail))
        self.t_thumbnail.penup()
        self.t_thumbnail.goto(310, 280)

        index = 0
        for i in range(self.xy_num_tile):

            for j in range(self.xy_num_tile):
                self.turtles[index].speed(0)
                tile_file_name = self.tiles[index][1]
                self.screen.addshape(os.path.relpath(tile_file_name))

                # adding turtles to correct positions (in order) and hide turtles first.
                self.turtles[index].hideturtle()
                self.turtles[index].shape(os.path.relpath(tile_file_name))
                self.turtles[index].penup()
                self.turtles[index].goto(-275 + (self.tile_length + 2) * j,
                                         225 - (self.tile_length + 2) * i)
                self.positions.append(self.turtles[index].pos())
                index = index + 1

        self.shuffled_index = list(range(len(self.turtles)))

        # before shuffle indexes, create a list to store
        # ordered indexes, for later win or lose comparison use
        for each in self.shuffled_index:
            self.ordered_index.append(each)

        # [3, 5, 2, 1...]
        random.shuffle(self.shuffled_index)

        # make a copy of shuffled_index for later win or lose comparison use
        # because self.shuffled_index is a changeable attribute, affecting all
        for each in self.shuffled_index:
            self.copy_shuffled_index.append(each)

        self.shuffled_turtles = []
        for i in range(len(self.turtles)):
            x, y = self.positions[i]
            # make turtle3 go to turtle1's position which is ordered
            # make turtle5 go to turtle2's position
            self.turtles[self.shuffled_index[i]].goto(x, y)
            self.turtles[self.shuffled_index[i]].showturtle()
            self.shuffled_turtles.append(self.tiles[self.shuffled_index[i]])

        
    def get_screenclick(self):
        '''
            Method -- get_screenclick
                to check if the player click on the movable tiles
                and tell if the player win or lose
        '''

        def click_tile_helper(x, y):
            '''
                Method -- click_tile_helper
                    a nested helper method to use onclick to give
                    x,y coordinates of tiles
                Parameters:
                    x: mouse click x coordinate
                    y: mouse click y coordinate
            '''
            self.click_x = x
            self.click_y = y

            # if player clicks on reset button
            if 46 <= self.click_x <= 123 and -266 <= self.click_y <= -192:

                # each time goes into reset, sort current changing indexes list
                # because tiles are ordered now
                # [0, 1, 2, 3,...]
                self.copy_shuffled_index.sort()

                # place ordered images on screen
                for i in range(len(self.turtles)):
                    x, y = self.positions[i]
                    self.turtles[self.ordered_index[i]].goto(x, y)

                for t in range(len(self.shuffled_turtles)):
                    # to find the blank tile
                    if int(self.shuffled_turtles[t][0].strip(":")) \
                            == int(len(self.shuffled_turtles)):
                        self.blank_x, self.blank_y = \
                            self.turtles[self.shuffled_index[t]].pos()

                        # for instance, blank number15's position in list is 4
                        self.blank_index = t

                        # blank num is always the last number
                        blank_num = self.shuffled_index[t]


            # click within the square of all tiles
            if -275 - (self.tile_length / 2) < self.click_x < \
                    -275 - (self.tile_length / 2) + (self.tile_length + 2) \
                    * self.xy_num_tile and \
                    225 + (self.tile_length / 2) > self.click_y > \
                    225 + (self.tile_length / 2) - (self.tile_length + 2) \
                    * self.xy_num_tile:

                for t in range(len(self.shuffled_turtles)):
                    # to find the blank tile
                    if int(self.shuffled_turtles[t][0].strip(":")) == \
                            int(len(self.shuffled_turtles)):
                        self.blank_x, self.blank_y = \
                            self.turtles[self.shuffled_index[t]].pos()

                        self.blank_index = t
                        blank_num = self.shuffled_index[t]

                for i in range(len(self.turtles)):
                    # to get the coordinates of the tile that player clicks on
                    if abs(self.click_x - self.turtles[self.shuffled_index[i]].xcor()) \
                            <= self.tile_length / 2 and \
                            abs(self.click_y - self.turtles[self.shuffled_index[i]].ycor()) \
                            <= self.tile_length / 2:

                        turtle_clicked = self.turtles[self.shuffled_index[i]]

                        click_num = self.shuffled_index[i]

                        # click on the upside tile of blank tile
                        if turtle_clicked.xcor() == self.blank_x \
                                and turtle_clicked.ycor() > self.blank_y \
                                and turtle_clicked.ycor() - self.blank_y <= self.tile_length + 2:

                            # swap position of blank tile with the clicked-on tile
                            self.turtles[self.shuffled_index[self.blank_index]].\
                                setpos(turtle_clicked.xcor(), turtle_clicked.ycor())
                            turtle_clicked.setpos(self.blank_x, self.blank_y)

                            # the number of clicked tile and blank tile is unchangeable
                            # but their positions/index in the list is changing
                            # when swapping blank tile with a movable tile
                            # thus to get the updated index every time from the same number
                            click_num_index = self.copy_shuffled_index.index(click_num)
                            blank_num_index = self.copy_shuffled_index.index(blank_num)

                            self.copy_shuffled_index[click_num_index], \
                            self.copy_shuffled_index[blank_num_index] = \
                                self.copy_shuffled_index[blank_num_index], \
                                self.copy_shuffled_index[click_num_index]

                            self.moves += 1
                            self.num_of_moves()
                            break

                        # click on the downside tile of blank tile
                        elif turtle_clicked.xcor() == self.blank_x \
                                and turtle_clicked.ycor() < self.blank_y \
                                and self.blank_y - turtle_clicked.ycor() \
                                <= self.tile_length + 2:
                            self.turtles[self.shuffled_index[self.blank_index]].\
                                setpos(turtle_clicked.xcor(), turtle_clicked.ycor())
                            turtle_clicked.setpos(self.blank_x, self.blank_y)

                            click_num_index = self.copy_shuffled_index.index(click_num)
                            blank_num_index = self.copy_shuffled_index.index(blank_num)

                            self.copy_shuffled_index[click_num_index], \
                            self.copy_shuffled_index[blank_num_index] = \
                                self.copy_shuffled_index[blank_num_index], \
                                self.copy_shuffled_index[click_num_index]

                            self.moves += 1
                            self.num_of_moves()
                            break

                        # click on the leftside tile of blank tile
                        elif turtle_clicked.ycor() == self.blank_y \
                                and turtle_clicked.xcor() < self.blank_x \
                                and self.blank_x - turtle_clicked.xcor() <= self.tile_length + 2:

                            self.turtles[self.shuffled_index[self.blank_index]].\
                                setpos(turtle_clicked.xcor(), turtle_clicked.ycor())
                            turtle_clicked.setpos(self.blank_x, self.blank_y)

                            click_num_index = self.copy_shuffled_index.index(click_num)
                            blank_num_index = self.copy_shuffled_index.index(blank_num)

                            self.copy_shuffled_index[click_num_index], \
                            self.copy_shuffled_index[blank_num_index] = \
                                self.copy_shuffled_index[blank_num_index], \
                                self.copy_shuffled_index[click_num_index]

                            self.moves += 1
                            self.num_of_moves()
                            break

                        # click on the rightside tile of blank tile
                        elif turtle_clicked.ycor() == self.blank_y \
                                and turtle_clicked.xcor() > self.blank_x \
                                and turtle_clicked.xcor() - self.blank_x <= self.tile_length + 2:

                            self.turtles[self.shuffled_index[self.blank_index]].\
                                setpos(turtle_clicked.xcor(),turtle_clicked.ycor())
                            turtle_clicked.setpos(self.blank_x, self.blank_y)

                            click_num_index = self.copy_shuffled_index.index(click_num)
                            blank_num_index = self.copy_shuffled_index.index(blank_num)

                            self.copy_shuffled_index[click_num_index], \
                            self.copy_shuffled_index[blank_num_index] = \
                                self.copy_shuffled_index[blank_num_index], \
                                self.copy_shuffled_index[click_num_index]

                            self.moves += 1
                            self.num_of_moves()
                            break

                # this part for deciding player win or lose
                if self.moves <= self.moves_choice:
                    # after all the swapping, when the copy_shuffled_index lst
                    # is the same as the correct order [0, 1, 2, 3,..], player won
                    if self.ordered_index == self.copy_shuffled_index:
                        t_win = turtle.Turtle()
                        t_win.speed(0)
                        self.screen.addshape(os.path.relpath("Resources/winner.gif"))
                        t_win.shape(os.path.relpath("Resources/winner.gif"))
                        t_win.penup()
                        t_win.goto(0, 8)
                        time.sleep(3)

                        with open("leaderboard.txt", "a") as contents:
                            contents.write(f"{self.moves}: {self.player_name}")

                        t_win_credits = turtle.Turtle()
                        self.screen.addshape((os.path.relpath("Resources/credits.gif")))
                        t_win_credits.shape(os.path.relpath("Resources/credits.gif"))
                        t_win_credits.penup()
                        t_win_credits.goto(0, 8)
                        time.sleep(1)
                        self.screen.bye()

                elif self.moves > self.moves_choice:
                    t_lose = turtle.Turtle()
                    t_lose.speed(0)
                    self.screen.addshape(os.path.relpath("Resources/Lose.gif"))
                    t_lose.shape(os.path.relpath("Resources/Lose.gif"))
                    t_lose.penup()
                    t_lose.goto(0, 8)
                    time.sleep(1)

                    t_lose_credits = turtle.Turtle()
                    self.screen.addshape((os.path.relpath("Resources/credits.gif")))
                    t_lose_credits.shape(os.path.relpath("Resources/credits.gif"))
                    t_lose_credits.penup()
                    t_lose_credits.goto(0, 8)
                    self.screen.bye()

        self.screen.onclick(click_tile_helper)
        turtle.mainloop()

    def player_moves(self):
        '''
            Method -- player_moves
                let turtle write "Player Moves:" and go
                to down lest
        '''
        t_moves = turtle.Turtle()
        t_moves.pensize(6)
        t_moves.penup()
        t_moves.hideturtle()
        t_moves.goto(-330, -239)
        t_moves.speed(0)
        t_moves.write(f"Player Moves: ", font=("Arial", 20, 'bold'))
        t_moves.pendown()
        # t_moves.clear()

    def num_of_moves(self):
        '''
            Method -- num_of_mvoes
                to show the number of player's moves
        '''
        self.t_num.clear()
        self.t_num.hideturtle()
        self.t_num.pensize(6)
        self.t_num.speed(0)
        self.t_num.penup()
        self.t_num.goto(-180, -239)
        self.t_num.write(f"{self.moves}", font=("Arial", 20, 'bold'))

def main():
    game = PuzzleGame()
    game.screen_setup()
    game.draw_frames()
    game.place_quitbutton()

    game.place_loadbutton()
    game.open_file()

    game.place_resetbutton()
    game.player_moves()
    game.place_leaders()
    game.place_leader_names()
    game.place_tiles()
    game.get_screenclick()

    turtle.done()

if __name__ == "__main__":
    main()

