import numpy as np
import time
from tkinter import *

'''
Constants for the canvas
'''
NUM_BAR = 100 # Size of the array
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500
CANVAS_OFFSET = 20
PAUSE_MILLISECOND = 1
FILL_COLOR = 'black'
BAR_WIDTH = CANVAS_WIDTH / NUM_BAR

'''
Creation of the canvas
'''
master = Tk()
w = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT + CANVAS_OFFSET)
w.pack()
rects = [w.create_rectangle(BAR_WIDTH * i, CANVAS_HEIGHT, BAR_WIDTH * (i + 1), CANVAS_HEIGHT, fill = FILL_COLOR) for i in range(NUM_BAR)]
arr = [np.random.randint(0, CANVAS_HEIGHT) for i in range(NUM_BAR)]
def visualizeArr():
	for i in range(NUM_BAR):
		w.coords(rects[i], (BAR_WIDTH * i, CANVAS_HEIGHT, BAR_WIDTH * (i + 1), CANVAS_HEIGHT - arr[i]))
tuples = [(1, 2), (2, 3), (3, 1)]
idx = 0
states = []

'''
Helper function that reads from the list tuples
Perform all those swaps and visualize
'''
def swap():
	global idx
	if idx == len(tuples):
		return
	i, j = tuples[idx]
	arr[i], arr[j] = arr[j], arr[i]
	visualizeArr()
	idx += 1
	w.after(PAUSE_MILLISECOND, swap)

'''
Helper function that walks through all the states in the array and visualize
share the global variable idx
'''
def directPlot():
	global idx
	global arr
	if idx == len(states):
		return
	arr = states[idx]
	visualizeArr()
	idx += 1
	w.after(PAUSE_MILLISECOND, directPlot)

'''
Selection sort visualization
Each time, select the minimum element forward
exchange the current with the minimum element, and advance
'''
def selectionSort():
	global tuples
	tuples = []
	arrCopy = arr.copy()
	for i in range(NUM_BAR):
		minIdx = i
		for j in range(i + 1, NUM_BAR):
			if arrCopy[j] < arrCopy[minIdx]:
				minIdx = j
		tuples.append((i, minIdx))
		arrCopy[i], arrCopy[minIdx] = arrCopy[minIdx], arrCopy[i]
	global idx
	idx = 0
	swap()

'''
Insertion sort
'''
def insertionSort():
	global states
	states = []
	arrCopy = arr.copy()
	for i in range(1, NUM_BAR):
		currGroup = []
		# bubble left arr[i]
		j = i
		while j != 0 and arrCopy[j] < arrCopy[j - 1]:
			currGroup.append((j, j - 1))
			arrCopy[j], arrCopy[j - 1] = arrCopy[j - 1], arrCopy[j]
			j = j - 1
		states.append(arrCopy.copy())
	global idx
	idx = 0
	directPlot()

'''
Merge sort
'''
def mergeSort():
	global states
	arrCopy = arr.copy()
	def mergeSortHelper(l, r):
		# Sort from l to r, inclusively
		if l == r:
			return
		m = (l + r) // 2
		mergeSortHelper(l, m)
		mergeSortHelper(m + 1, r)
		nonlocal arrCopy
		# Merge the two parts
		# Create a temporary list to store the result
		mergedList = []
		p1 = l
		p2 = m + 1
		while p1 <= m and p2 <= r:
			if arrCopy[p1] <= arrCopy[p2]:
				mergedList.append(arrCopy[p1])
				p1 += 1
			else:
				mergedList.append(arrCopy[p2])
				p2 += 1
		while p1 <= m:
			mergedList.append(arrCopy[p1])
			p1 += 1
		while p2 <= r:
			mergedList.append(arrCopy[p2])
			p2 += 1
		for i, v in enumerate(mergedList):
			arrCopy[l + i] = v
		global states
		states.append(arrCopy.copy())
	mergeSortHelper(0, NUM_BAR - 1)
	global idx
	idx = 0
	directPlot()

'''
Heap sort
'''

'''
Use Fisher-Yates shuffle algorithm to rearrange the array
triggered by shuffle
'''
def shuffle():
	for i in range(NUM_BAR - 1):
		j = np.random.randint(NUM_BAR - i)
		arr[i], arr[i + j] = arr[i + j], arr[i]
	visualizeArr()

btnShuffle = Button(text = 'Shuffle', command = shuffle)
btnShuffle.pack()
btnSelectionSort = Button(text = 'Selection sort', command = selectionSort)
btnSelectionSort.pack()
btnInsertionSort = Button(text = 'Insertion sort', command = insertionSort)
btnInsertionSort.pack()
btnMergeSort = Button(text = 'Merge sort', command = mergeSort)
btnMergeSort.pack()
shuffle()
mainloop()
