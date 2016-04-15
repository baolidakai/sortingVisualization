import numpy as np
import time
from tkinter import *

NUM_BAR = 10 # Size of the array
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 100
CANVAS_OFFSET = 50
PAUSE_SECOND = 1
BAR_WIDTH = CANVAS_WIDTH / NUM_BAR

master = Tk()
w = Canvas(master, width = CANVAS_WIDTH + CANVAS_OFFSET, height = CANVAS_HEIGHT)
w.pack()
rects = [w.create_rectangle(BAR_WIDTH * i, CANVAS_HEIGHT, BAR_WIDTH * (i + 1), CANVAS_HEIGHT, fill = 'blue') for i in range(NUM_BAR)]
arr = [np.random.randint(0, CANVAS_HEIGHT) for i in range(NUM_BAR)]
def visualizeArr():
	for i in range(NUM_BAR):
		w.coords(rects[i], (BAR_WIDTH * i, CANVAS_HEIGHT, BAR_WIDTH * (i + 1), CANVAS_HEIGHT - arr[i]))
tuples = [(1, 2), (2, 3), (3, 1)]
idx = 0
def swap():
	global idx
	print(idx)
	if idx == len(tuples):
		return
	i, j = tuples[idx]
	arr[i], arr[j] = arr[j], arr[i]
	visualizeArr()
	idx += 1
	w.after(PAUSE_SECOND * 1000, swap)
swap()
mainloop()
