import numpy as np
import time
import sys
import tkinter as tk

from PIL import Image, ImageDraw, ImageTk
# 0 - white, 1 - black


f = 0
HEIGHT = 320   # of window
WIDTH = 320
size = [0, 0]   # cell, of field
x = 0
y = 0
x0 = 0
y0 = 0
step = 1
value = 0
direction = 0     # 0 - North, 1 - East, 2 - South, 3 - West
color = ["White",
         "Red",
         "Lime",
         "Cyan",
         "Gold",
         "DeepPink",
         "Gray",
         "Maroon",
         "DarkGreen",
         "MidnightBlue"]   # 0 - white, 1 - red
color_numbers = len(color)
# 1 - counterclockwise, 0 - clockwise
# 1 - left, 0 - right
turns = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0]

""" cool ants
1. ["White", "Red", "Lime"] [1, 1, 0]
2. ["White", "Red", "Lime", "Cyan", "Gold", "DeepPink", "Gray",
Maroon", "DarkGreen","MidnightBlue"] [0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
"""


class UnexpectedError(Exception):
    def __init__(self, value):
        self.value = value


def data():   # First window, get size of image, ant's coordinates
    global f, HEIGHT, WIDTH, size, way, x, y, arrray
    global ent_size0, ent_size1, ent_y, ent_x, root1

    root1 = tk.Tk()
    root1.geometry('+500+400')
    lb1 = tk.Label(root1, text="Size of field in cells:", font="arial 12")
    lb_size0 = tk.Label(root1, text="height", font="arial 12")
    lb_size1 = tk.Label(root1, text="width", font="arial 12")
    ent_size0 = tk.Entry(root1)
    ent_size1 = tk.Entry(root1)
    lb2 = tk.Label(root1, text="Original ant's coordinates:", font="arial 12")
    lb_x = tk.Label(root1, text="x", font="arial 12")
    lb_y = tk.Label(root1, text="y", font="arial 12")
    ent_x = tk.Entry(root1)
    ent_y = tk.Entry(root1)
    bt = tk.Button(root1, text="done", command=ok, font="arial 14")

    lb1.grid(row=1, column=1)
    lb_size0.grid(row=2, column=1)
    lb_size1.grid(row=3, column=1)
    ent_size0.grid(row=2, column=2)
    ent_size1.grid(row=3, column=2)
    lb2.grid(row=4, column=1)
    lb_x.grid(row=5, column=1)
    lb_y.grid(row=6, column=1)
    ent_x.grid(row=5, column=2)
    ent_y.grid(row=6, column=2)
    bt.grid(row=7, column=2)

    root1.mainloop()


def ok():  # Second window, get size of field or way
    global x, y, size, array

    x = int(ent_x.get())
    y = int(ent_y.get())
    size = (int(ent_size0.get())-1, int(ent_size1.get())-1)
    array = np.zeros((size[0]+1, size[1]+1), dtype=int)
    
    root1.destroy()


def image_():  # generate image with ant's way
    global im, color
    
    if (step % 500) == 0:  # maybe, it'll be faster without print
        print(step, "step")
        
    draw = ImageDraw.Draw(im)
    step1 = HEIGHT / (size[0]+1)
    step2 = WIDTH / (size[1]+1)
    value = array[x0][y0]

    if step != 1:
        draw.rectangle((x0*step2, y0*step1, (x0+1)*step2, (y0+1)*step1),
                        fill=color[value])
    draw.rectangle((x*step2, y*step1, (x+1)*step2, (y+1)*step1),
                    fill="black",
                    outline="black")


def show_():   # update image on root
    """ update image on root
    """
    global label

    image_()
    photo = ImageTk.PhotoImage(im)
    label['image'] = photo
    label.image = photo


# LOGIC FUNCTIONS
def turn(move):   # by turns[] rules
    global direction

    if move == 1:   # clockwise
        direction = (direction - 1) % 4
    elif move == 0:  # counterclockwise
        direction = (direction + 1) % 4


def step_():
    global direction, x, y, size
    if direction == 0:   # North
        if y != 0:
            y -= 1
        else:
            y = size[0]
    elif direction == 1:   # East  ->
        if x != size[1]:
            x += 1
        else:
            x = 0
    elif direction == 2:    # South
        if y != size[0]:
            y += 1
        else:
            y = 0
    elif direction == 3:    # West   <--
        if x != 0:
            x -= 1
        else:
            x = size[1]


def main():
    global step, x0, y0, turns, color_numbers, color, value
    
    show_()

    x0 = x
    y0 = y
    value = array[x][y]
    if isinstance(array[x][y],np.int32) and (-1 < array[x][y] < color_numbers):
        turn(turns[value])
        array[x][y] = (value+1) % color_numbers
    else:
        print(array[x][y], type(array[x][y]))
        raise(UnexpectedError("Something goes wrong!"))
        sys.exit()
    step_()
    step += 1

    label.after(2, main)


if __name__ == "__main__":
    data()
    
    root = tk.Tk()
    im = Image.new("RGBA", (WIDTH+1, HEIGHT+1), "LightGray")
    photo = ImageTk.PhotoImage(im)
    label = tk.Label()
    label['image'] = photo
    label.image = photo
    label.pack()
    
    label.after_idle(main)
    root.mainloop()
