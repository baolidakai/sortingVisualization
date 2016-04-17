import numpy as np
import random
import time
try:
	from tkinter import *
except:
	from Tkinter import *
from heapq import heapify, heappop
try:
	from queue import Queue
except:
	from Queue import Queue

'''
Constants for the canvas
'''
NUM_BAR = 300 # Size of the array
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
CANVAS_OFFSET = 100
PAUSE_MILLISECOND = 1
BACKGROUND_COLOR = 'black'
FOREGROUND_COLOR = 'white'

'''
Creation of the canvas
'''
master = Tk()
master.geometry('%dx%d+%d+%d' % (CANVAS_WIDTH + 2 * CANVAS_OFFSET, CANVAS_HEIGHT + 2 * CANVAS_OFFSET, 0, 0))
w = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT, bg = BACKGROUND_COLOR)
w.place(x = CANVAS_OFFSET, y = CANVAS_OFFSET)

tuples = []
idx = 0
states = []
rects = []
arr = np.array([])
def initialize():
	global rects
	BAR_WIDTH = CANVAS_WIDTH / (NUM_BAR + 2)
	rects = [w.create_rectangle(BAR_WIDTH * (i + 1), CANVAS_HEIGHT, BAR_WIDTH * (i + 2), CANVAS_HEIGHT, fill = FOREGROUND_COLOR) for i in range(NUM_BAR)]
	global arr
	arr = np.array([np.random.randint(0, CANVAS_HEIGHT) for i in range(NUM_BAR)])

def visualizeArr():
	BAR_WIDTH = CANVAS_WIDTH / (NUM_BAR + 2)
	for i in range(NUM_BAR):
		w.coords(rects[i], (BAR_WIDTH * (i + 1), CANVAS_HEIGHT, BAR_WIDTH * (i + 2), CANVAS_HEIGHT - arr[i]))

'''
Clean everything
'''
def cleanFill():
	for i in range(NUM_BAR):
		w.itemconfig(rects[i], fill = FOREGROUND_COLOR)

'''
Helper function that reads from the list tuples
Perform all those swaps and visualize
'''
def swap():
	global idx
	cleanFill()
	if idx == len(tuples):
		return
	i, j = tuples[idx]
	try:
		w.itemconfig(rects[i], fill = 'red')
		w.itemconfig(rects[j], fill = 'red')
	except:
		'Do nothing'
	arr[i], arr[j] = arr[j], arr[i]
	idx += 1
	visualizeArr()
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
	global tuples
	tuples = []
	arrCopy = arr.copy()
	for i in range(1, NUM_BAR):
		# bubble left arr[i]
		j = i
		while j != 0 and arrCopy[j] < arrCopy[j - 1]:
			tuples.append((j, j - 1))
			arrCopy[j], arrCopy[j - 1] = arrCopy[j - 1], arrCopy[j]
			j = j - 1
	global idx
	idx = 0
	swap()

'''
Merge sort
'''
def mergeSort():
	global states
	states = []
	global arr
	def mergeSortHelper(l, r):
		# Sort from l to r, inclusively
		global arr
		if l == r:
			return
		m = (l + r) // 2
		mergeSortHelper(l, m)
		mergeSortHelper(m + 1, r)
		# Merge the two parts
		# Create a temporary list to store the result
		mergedList = []
		p1 = l
		p2 = m + 1
		while p1 <= m and p2 <= r:
			if arr[p1] <= arr[p2]:
				mergedList.append(arr[p1])
				p1 += 1
			else:
				mergedList.append(arr[p2])
				p2 += 1
		while p1 <= m:
			mergedList.append(arr[p1])
			p1 += 1
		while p2 <= r:
			mergedList.append(arr[p2])
			p2 += 1
		for i, v in enumerate(mergedList):
			arr[l + i] = v
		global states
		states.append(arr.copy())
	mergeSortHelper(0, NUM_BAR - 1)
	global idx
	idx = 0
	directPlot()

'''
Heap sort
'''
def heapSort():
	global states
	states = []
	# Construct a min-heap
	heapify(arr)
	minHeap = arr.copy()
	# Extract elements from the heap
	extracted = []
	while minHeap:
		extracted.append(heappop(minHeap))
		states.append(extracted.copy() + minHeap.copy())
	global idx
	idx = 0
	directPlot()

'''
Quick Sort using random pivot
'''
def quickSort():
	arrCopy = arr.copy()
	def quickSortHelper(l, r):
		# In-place quick sort from l to r inclusive
		if l >= r:
			return []
		rtn = []
		# Choose a random pivot p
		pivotIdx = l + np.random.randint(r - l + 1)
		p = arrCopy[pivotIdx]
		# Count number of elements < p
		pivotTarget = l + len([arrCopy[i] for i in range(l, r + 1) if arrCopy[i] < p])
		# Exchange the pivot with that element
		rtn.append((pivotIdx, pivotTarget))
		arrCopy[pivotIdx], arrCopy[pivotTarget] = arrCopy[pivotTarget], arrCopy[pivotIdx]
		# Use two pointers to partition the array in place
		p1 = l
		p2 = r
		while p1 < pivotTarget and p2 > pivotTarget:
			while arrCopy[p1] < p and p1 < pivotTarget:
				p1 += 1
			while arrCopy[p2] >= p and p2 > pivotTarget:
				p2 -= 1
			# arrCopy[p1] is either a large element or the array is already partitioned
			# arrCopy[p2] is either a small element or the array is already partitioned
			if p1 == pivotTarget or p2 == pivotTarget:
				break
			# Exchange two elements
			rtn.append((p1, p2))
			arrCopy[p1], arrCopy[p2] = arrCopy[p2], arrCopy[p1]
			p1 += 1
			p2 -= 1
		# Recurse on left part and right part
		leftOps = quickSortHelper(l, pivotTarget - 1)[:]
		rightOps = quickSortHelper(pivotTarget + 1, r)[:]
		rtn += leftOps
		rtn += rightOps
		return rtn
	global tuples
	tuples = quickSortHelper(0, NUM_BAR - 1)[:]
	global idx
	idx = 0
	swap()

'''
Bubble sort
At most n loops, each time swap two adjacent elements if their order is incorrect
'''
def bubbleSort():
	global tuples
	tuples = []
	arrCopy = arr.copy()
	finished = False
	for iteration in range(NUM_BAR):
		if not finished:
			finished = True
			for i in range(NUM_BAR - 1):
				if arrCopy[i] > arrCopy[i + 1]:
					finished = False
					arrCopy[i], arrCopy[i + 1] = arrCopy[i + 1], arrCopy[i]
					tuples.append((i, i + 1))
	global idx
	idx = 0
	swap()

'''
Shell sort
'''
def shellSort():
	gaps = [701, 301, 132, 57, 23, 10, 4, 1]
	global tuples
	tuples = []
	arrCopy = arr.copy()
	for gap in gaps:
		# Do a gapped insertion sort for this gap size.
		for i in range(gap, NUM_BAR):
			j = i
			while j >= gap and arrCopy[j] < arrCopy[j - gap]:
				# Exchange j and j - gap
				tuples.append((j, j - gap))
				arrCopy[j], arrCopy[j - gap] = arrCopy[j - gap], arrCopy[j]
				j -= gap
	global idx
	idx = 0
	swap()

'''
Comb sort
A variant of bubble sort, which instead of comparing the adjacent pairs,
compare all pairs of a gap diminishing from size to 1
'''
def combSort():
	global tuples
	tuples = []
	arrCopy = arr.copy()
	finished = False
	gap = NUM_BAR
	shrinkingFactor = 1.3
	while gap > 1 or not finished:
		gap = int(gap / shrinkingFactor)
		if gap < 1:
			gap = 1
		finished = True
		for i in range(NUM_BAR - gap):
			if arrCopy[i] > arrCopy[i + gap]:
				finished = False
				arrCopy[i], arrCopy[i + gap] = arrCopy[i + gap], arrCopy[i]
				tuples.append((i, i + gap))
	global idx
	idx = 0
	swap()

'''
Counting sort
To visualize, each time we add a new element, refresh the screen
'''
def countingSort():
	global states
	states = []
	counts = [0] * CANVAS_HEIGHT
	for v in arr:
		counts[v] += 1
	currIdx = 0
	for i in range(CANVAS_HEIGHT):
		count = counts[i]
		for j in range(count):
			arr[currIdx + j] = i
		currIdx += count
		states.append(arr.copy())
	global idx
	idx = 0
	directPlot()

'''
Bucket sort
Go over the original array, putting each object in its bucket.
Sort each non-empty bucket
Visit the buckets in order and put all elements back into the original array
'''
def bucketSort():
	bucketSize = 10
	bucketNum = CANVAS_HEIGHT // bucketSize + 1
	buckets = [[] for i in range(bucketNum)]
	for v in arr:
		buckets[v // bucketSize].append(v)
	# Sort each bucket
	for i in range(bucketNum):
		bucketElements = buckets[i]
		# Apply insertion sort
		for j in range(1, len(bucketElements)):
			k = j
			while k != 0 and bucketElements[k] < bucketElements[k - 1]:
				bucketElements[k], bucketElements[k - 1] = bucketElements[k - 1], bucketElements[k]
				k = k - 1
		buckets[i] = bucketElements
	# Concatenate all results
	global states
	states = []
	currIdx = 0
	for i in range(bucketNum):
		for j in range(len(buckets[i])):
			arr[currIdx + j] = buckets[i][j]
		currIdx += len(buckets[i])
		states.append(arr.copy())
	global idx
	idx = 0
	directPlot()

'''
Radix sort
Display results after sorting each digit
'''
def radixSort():
	base = 10
	# Compute the longest element
	global arr
	maxLength = int(np.log(max(arr)) / np.log(base)) + 1
	global states
	states = []
	# Construct queues to store the elements
	queues = [Queue() for i in range(base)]
	for l in range(maxLength):
		# Enqueue each element
		for v in arr:
			queueId = (int(v) // (base ** l)) % base
			queues[queueId].put(v)
		# Dequeue each element in order
		arr = np.array([])
		for i in range(base):
			currQueue = queues[i]
			while not currQueue.empty():
				arr = np.append(arr, currQueue.get())
		states.append(arr.copy())
	global idx
	idx = 0
	directPlot()

'''
Use Fisher-Yates shuffle algorithm to rearrange the array
triggered by shuffle
'''
def shuffle():
	for i in range(NUM_BAR - 1):
		j = np.random.randint(NUM_BAR - i)
		arr[i], arr[i + j] = arr[i + j], arr[i]
	visualizeArr()

initialize()
def changeArraySize(event):
	'''
	By entering the array size, the user specifies how many swaps to display within one pause
	'''
	# Empty the original plot
	global NUM_BAR
	global rects
	for k in range(NUM_BAR):
		w.delete(rects[k])
	NUM_BAR = int(str(ety.get()))
	initialize()
	shuffle()

def changeColor(c):
	def rtn():
		w.configure(bg = c)
	return rtn
def changeForegroundColor(c):
	def rtn():
		global rects
		for k in range(NUM_BAR):
			w.delete(rects[k])
		global FOREGROUND_COLOR
		FOREGROUND_COLOR = c
		initialize()
		shuffle()
	return rtn

# Place the color options at the bottom of the screen
colors = ['red', 'yellow', 'pink', 'green', 'purple', 'orange', 'blue']
Label(text = 'Background color').place(x = 0, y = CANVAS_HEIGHT + CANVAS_OFFSET * 1.2)
col = 2
for c in colors:
	Button(text = c, fg = c, bg = c, command = changeColor(c)).place(x = col * 60, y = CANVAS_HEIGHT + CANVAS_OFFSET * 1.2)
	col += 1

Label(text = 'Foreground color').place(x = 0, y = CANVAS_HEIGHT + CANVAS_OFFSET * 1.6)
col = 2
for c in colors:
	Button(text = c, fg = c, bg = c, command = changeForegroundColor(c)).place(x = col * 60, y = CANVAS_HEIGHT + CANVAS_OFFSET * 1.6)
	col += 1

Label(text = 'Enter the array size:').place(x = CANVAS_OFFSET, y = 0)
ety = Entry(master)
ety.bind('<Return>', changeArraySize)
ety.place(x = CANVAS_OFFSET, y = CANVAS_OFFSET * 0.5)
Button(text = 'Shuffle', command = shuffle).place(x = CANVAS_OFFSET * 0.2, y = CANVAS_OFFSET)
commands = [('Selection sort', selectionSort), ('Insertion sort', insertionSort),\
		('Merge sort', mergeSort), ('Quick sort', quickSort),\
		('Bubble sort', bubbleSort), ('Shell sort', shellSort),\
		('Comb sort', combSort), ('Counting sort', countingSort),\
		('Bucket sort', bucketSort), ('Radix sort', radixSort)]
row = 2
for key, cmd in commands:
	Button(text = key, command = cmd).place(x = CANVAS_OFFSET * 0.0, y = row * 20 + CANVAS_OFFSET)
	row += 1
shuffle()
mainloop()
