import random
import tkinter as tk
from tkinter import messagebox

# game parameters which can be modified
x_range = 20
y_range = 20
mines_number = 80



# definitions
root = tk.Tk()

points=0                                                            # number of earned points (revealed field without mines); if it is equal total number of field without mines, the game is won
exploded_mines=0                                                    # number of accidentally exploded mines

signal = [[0 for y in range(y_range)] for x in range(x_range)]      # how many mines are nearby (value 9 means a mine placed in the current field)
revealed  = [[0 for y in range(y_range)] for x in range(x_range)]   # 1 means that current field is revealed, 0 means that it is not

buttons =  [[0 for x in range(y_range)] for x in range(x_range)]    # array of buttons



# adjusting sizes of buttons
def button_sizes(x_range,y_range):    
    global buttonsize_x             # that parameters mean how large buttons are
    global buttonsize_y             # that parameters will be used later outside this function, this is why they are labeled as global

    if(x_range>15):
        buttonsize_x=2              # if there is many fields on the board, buttons must be small
    else:
        buttonsize_x=4              # if there is no many fields, buttons can be larger
    if(y_range>15):
        buttonsize_y=1
    else:
        buttonsize_y = 2



# placing mines:
def placing_mines(x_range, y_range, mines_number):

    # statements
    if(mines_number>x_range*y_range):
        raise ValueError("Number of mines cannot be smaller than number of fields on the board!")
    if(x_range<1):
        raise ValueError("Size of the board is incorrect!")
    if(y_range<1):
        raise ValueError("Size of the board is incorrect!")
    if(mines_number<0):
        raise ValueError("Number of mines must not be negative!")
    
    # how this function works:    
    global signal

    n=0                                                 # parameter to increment in the while loop (it means how many mines have been placed so far)
    while n<mines_number:
        x_coordinate = random.randrange(0, x_range)     # randomly chosing coordinates of a mine
        y_coordinate = random.randrange(0, y_range)

        if (signal[x_coordinate][y_coordinate]==0):      # checking if there are no mines in the chosen field (we do not want to have two mines in the same field)
            signal[x_coordinate][y_coordinate]=9         # marking that in there are a mine in the chosen field
            n+=1



# calculating signal (number of mines in nearby fields) for every field:
def signal_calculation(x_range,y_range):
    global signal
    
    for x in range(x_range):
        for y in range(y_range):
            if signal[x][y]==9:                              # if we have a mine on a certain field we should increase signal of nearby fields
                if (x>0 and y>0 and signal[x-1][y-1]!=9):   # "signal[x-1][y-1]!=9" means that we do not increase signal on the fields where mines are placed
                    signal[x-1][y-1]+=1
                if (x>0 and signal[x-1][y]!=9):
                    signal[x-1][y]+=1
                if (x>0 and y<y_range-1 and signal[x-1][y+1]!=9):
                    signal[x-1][y+1]+=1
                if (y>0 and signal[x][y-1]!=9):
                    signal[x][y-1]+=1
                if (y<y_range-1 and signal[x][y+1]!=9):
                    signal[x][y+1]+=1
                if (x<x_range-1 and y>0 and signal[x+1][y-1]!=9):
                    signal[x+1][y-1]+=1
                if (x<x_range-1 and signal[x+1][y]!=9):
                    signal[x+1][y]+=1
                if (x<x_range-1 and y<y_range-1 and signal[x+1][y+1]!=9):
                    signal[x+1][y+1]+=1



# function defining what will happen after clicking on certain button
    # defautly buttons are blue and contain no text, which means that they are not revealed
    # clicking buttons will reveal them, i.e. show if there is a mine placed in this field or how strong signal is there

def reveal(c_x,c_y):
    global points
    global exploded_mines
    global revealed

    if signal[c_x][c_y]==9:
        buttons[c_x][c_y]['text'] = 'M'                 # if there is a mine in current field it will be marked by "M" 
    elif (signal[c_x][c_y]<9 and signal[c_x][c_y]>0):
        buttons[c_x][c_y]['text'] = signal[c_x][c_y]     # if there is no mine in current field, this field will show value of signal (if signal is 0 this value will not be displayed)

    buttons[c_x][c_y].configure(command=lambda:None)    # clicking second time in the same buttons does nothing
    revealed[c_x][c_y]=1                                # marking if this field is revealed yet

    if signal[c_x][c_y]==9:                              # checking if this field contains a mine
        buttons[c_x][c_y]['bg'] = "red"                 # marking exploded mine by red colour
        exploded_mines+=1                               # increasing number of exploded mines
        message_los = messagebox.showerror("Mine!", "You found a mine! But you can still play. Exploded mines: "+str( exploded_mines) ) # message showing finding a mine
    else:                                               # if this field contains no mines
        buttons[c_x][c_y]['bg'] = "white"               # marking revealed field by white color
        points=points+1                                 # increasing number of points

    if points==x_range*y_range-mines_number:            # if every field not containing mine is revealed 
        message_vic = messagebox.showinfo("Victory!", "You won! \n Exploded mines: "+str(exploded_mines)) # showing win message

    if signal[c_x][c_y]==0:                              # if signal is 0, every nearby field can be automatically revealed
        if (c_x>0 and c_y>0 and revealed[c_x-1][c_y-1]==0):
                reveal(c_x-1,c_y-1)
        if (c_x>0 and revealed[c_x-1][c_y]==0):
                reveal(c_x-1,c_y)
        if (c_x>0 and c_y<y_range-1 and revealed[c_x-1][c_y+1]==0):
                reveal(c_x-1,c_y+1)
        if (c_y>0 and revealed[c_x][c_y-1]==0):
                reveal(c_x,c_y-1)
        if (c_y<y_range-1 and revealed[c_x][c_y+1]==0):
                reveal(c_x,c_y+1)
        if (c_x<x_range-1 and c_y>0 and revealed[c_x+1][c_y-1]==0):
                reveal(c_x+1,c_y-1)
        if (c_x<x_range-1 and revealed[c_x+1][c_y]==0):
                reveal(c_x+1,c_y)
        if (c_x<x_range-1 and c_y<y_range-1 and revealed[c_x+1][c_y+1]==0):
                reveal(c_x+1,c_y+1)



# buttons
def placing_buttons(x_range,y_range):
    global buttons
    global mines_number
    global points
    global exploded_mines

    for x in range(x_range):
        for y in range(y_range):
            buttons[x][y] = tk.Button(text="",width=buttonsize_x,height=buttonsize_y,bg="blue",fg="green",command= lambda x_c=x, y_c=y : reveal(x_c,y_c))
            # defautly buttons are not revealed so contain no text and blue colour
            # command= executing the "reveal" function for the chosen field

            buttons[x][y].bind("<Button 3>", lambda x: print("Left fields without mines:",x_range*y_range-mines_number-points,"\nLeft fields with mines:",mines_number-exploded_mines))
            # right-click shows numbers of remaining field with and without mines

            buttons[x][y].grid(column=x, row=y)

    # additional buttons
    button_help = tk.Button(text="HELP",width=buttonsize_x,height=buttonsize_y,bg="green",fg="black",command=lambda: messagebox.showinfo("Help","left-click - reveal chosen field \n right click - show info about remaining fields")) # help
    button_quit = tk.Button(text="QUIT",width=buttonsize_x,height=buttonsize_y,bg="red",fg="black",command= root.destroy) # quit

    button_help.grid(column=0,row=y_range)
    button_quit.grid(column=x_range-1,row=y_range)



# executing all functions
button_sizes(x_range,y_range)
placing_mines(x_range, y_range, mines_number)
signal_calculation(x_range,y_range)
placing_buttons(x_range,y_range)

root.mainloop()
