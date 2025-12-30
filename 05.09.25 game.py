# catch the non-red circles for points
# avoid the red circles which end the game
import tkinter
import random

# handles when user first presses the key
def check_input(event):
    global move_direction, move_direction_2

    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    elif key == "Left":
        move_direction = "Left"

    if key == "Up":
        move_direction = "Up"

    elif key == "Down":
        move_direction = "Down"

    if key == "d":
        move_direction_2 = "Right"
    elif key == "a":
        move_direction_2 = "Left"

    if key == "w":
        move_direction_2 = "Up"

    elif key == "s":
        move_direction_2 = "Down"






# move the player left or right
# unless player is on edge of window
def move_player():
    if (move_direction == "Left") and \
       (canvas.coords(player)[0] > 0):
        canvas.move(player,-10,0)
    elif (move_direction == "Right") and \
         (canvas.coords(player)[0] < CANVAS_WD/2 -45):
          canvas.move(player,10,0)
    elif (move_direction == "Up") and \
       (canvas.coords(player)[1] > 0):
        canvas.move(player,0,-10)

    elif (move_direction == "Down") and \
       (canvas.coords(player)[1] < CANVAS_HT):
        canvas.move(player,0,10)

    if (move_direction_2 == "Left") and \
       (canvas.coords(player_2)[0] > 345):
        canvas.move(player_2,-10,0)
        
    elif (move_direction_2 == "Right") and \
         (canvas.coords(player_2)[0] < CANVAS_WD):
          canvas.move(player_2,10,0)
          
    elif (move_direction_2 == "Up") and \
       (canvas.coords(player_2)[1] > 0):
        canvas.move(player_2,0,-10)

    elif (move_direction_2 == "Down") and \
       (canvas.coords(player_2)[1] < CANVAS_HT):
        canvas.move(player_2,0,10)




    # schedule this function to move
    # the player at 60 frames per sec
    window.after(16,move_player)


# handles when user releases the key
def end_input(event):
    global move_direction, move_direction_2
    
    move_direction = "None"

    move_direction_2 = "None"


# get rid of instructions and title
def end_title_instr():
    canvas.delete(title)
    canvas.delete(directions)


# destroy our window at end of game
def end_game_over():
    window.destroy()


# check for collisions
def collision(item1,item2,distance):
    x_dis = abs(canvas.coords(item1)[0] - \
                canvas.coords(item2)[0])
    y_dis = abs(canvas.coords(item1)[1] - \
                canvas.coords(item2)[1])
    overlap = (x_dis < distance) and (y_dis < distance)
    return overlap

# check if player "hits" a circle
#  a bad circle - game over
#  a good circle - update score (possibly level and speed)
#                 get rid of that piece of circle
def check_hits():
    # bad circle
    for circle in bad_circle_list:
        if collision(player,circle,CIRCLE_WD):
            game_over = canvas.create_text(CANVAS_WD/2,\
                                           CANVAS_HT/2,
                                           text="Game Over. "+\
                                           "Player 2 wins.",\
                                           fill="red",\
                                           font=("Helvetica",30))

            window.after(2000,end_game_over)

            return

        if collision(player_2,circle,CIRCLE_WD):
            game_over = canvas.create_text(CANVAS_WD/2,\
                                           CANVAS_HT/2,
                                           text="Game Over. "+\
                                           "Player 1 wins.",\
                                           fill="red",\
                                           font=("Helvetica",30))
            window.after(2000,end_game_over)

            return


            
           
        

    # good circle
    for circle in circle_list:
        if collision(player,circle,CIRCLE_WD):
            canvas.delete(circle)
            circle_list.remove(circle)
            update_score_level_speed()
            


    #create a circle
    
    # schedule this function
    window.after(100,check_hits)





# update the score and if appropriate,
# the speed and level
def update_score_level_speed():
    global score,level,circle_speed, CIRCLE_WD
    score = score + 1
    score_display.config(text="Score: " +str(score))

    # decide if level increases

    if score%10 == 0: 

        level = level +1
        level_display.config(text="Level: " + str(level))
        circle_speed = circle_speed + 1
        CIRCLE_WD


        
def make_circle():
    CIRCLE_WD = 30
    # make circles at random locations
    x_pos = random.randint(0,CANVAS_WD)
    circle_color = random.choice(circle_color_list)
    # create circle
    circle = canvas.create_oval(x_pos,0,x_pos+CIRCLE_WD,CIRCLE_WD,\
                         fill=circle_color)
    # build our list of circles
    circle_list.append(circle)
    if circle_color == "red":
        bad_circle_list.append(circle)
    # schedule this function
    window.after(1000,make_circle)


def move_circles():

        # loop thru the circle list
        # to move the circles down the window

    for circle in circle_list:
        canvas.move(circle,0,circle_speed)

        
        # check if circle is at the bottom of screen
        # and move back to top
            
        if canvas.coords(circle)[1] > CANVAS_HT:
            x_pos = random.randint(1,CANVAS_WD-1)
            canvas.coords(circle, x_pos,1,x_pos+CIRCLE_WD,CIRCLE_WD)
        

    # schedule this function
    window.after(50,move_circles)


################################## main routine ###############################

    
# create a window

window = tkinter.Tk()
window.title("Catching/Avoding circles Games")

# create a canvas to put objects on

CANVAS_WD = 600
CANVAS_HT = 600
canvas = tkinter.Canvas(window,width=CANVAS_WD,height=CANVAS_HT,\
                        bg="black")

canvas.create_line(300, 0, 300, 650, width=3, fill="white")
canvas.pack()


# create and put title and directions on the canvas

title = canvas.create_text(CANVAS_WD/2,CANVAS_HT/2,\
                          fill="Red",font=("Helvetica",20),\
                          text="Catching/Avoiding cirles game!")

directions = canvas.create_text(CANVAS_WD/2,CANVAS_HT/2+40,\
                               fill="Red",font=("Helvetica",20),\
                          text="Catch the non-red circles!\n"+\
                               "avoid the red circles")

                               

# create variables to hold score and level

level = 1
score = 0

# put score and level on the window

score_display = tkinter.Label(window,text="Score: "+str(score))

score_display.pack()


level_display = tkinter.Label(window,text="Level: "+str(level))

level_display.pack()




# create our image to catch the circles and put it on the canvas

player_image = tkinter.PhotoImage(file="cookie monster.png")
player = canvas.create_image(CANVAS_WD/4,CANVAS_HT-45,\
                                  image=player_image)

player_image_2 = tkinter.PhotoImage(file="cookie monster 2.png")

player_2 = canvas.create_image(CANVAS_WD/2+150,CANVAS_HT-45,\
                                  image=player_image_2)

# create variables to manage the circles

circle_color_list = ["red", "yellow", "green", "purple", "blue"]

circle_list = [] #contains all the circles
bad_circle_list = [] #contains all the bad (red) circle

circle_speed = 2 # how fast objects drop

CIRCLE_WD = 30 #width circle

# variable to track which direction the player is moving

move_direction = "None"

move_direction_2 = "None"


# bind the keys user uses to move player

canvas.bind_all("<KeyPress>",check_input)  # when user presses a key

canvas.bind_all("<KeyRelease>",end_input)  # when user releases a key

# start the game by scheduling needed functions

window.after(1000,end_title_instr)
window.after(1000,make_circle)
window.after(1000,move_circles)
window.after(1000,check_hits)
window.after(1000,move_player)

# must be last line of file (i think)

window.mainloop()
