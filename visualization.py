# TODO: finish quick sort, bubble sort, shell sort, comb sort, counting sort, bucket sort, radix sort
import numpy as np
import random
import time
from tkinter import *
from heapq import heapify, heappop

'''
Constants for the canvas
'''
NUM_BAR = 100 # Size of the array
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500
CANVAS_OFFSET = 20
PAUSE_MILLISECOND = 1
FILL_COLORS = ['black', 'blue', 'orange']
BAR_WIDTH = CANVAS_WIDTH / NUM_BAR

'''
Creation of the canvas
'''
master = Tk()
w = Canvas(master, width = CANVAS_WIDTH, height = CANVAS_HEIGHT + CANVAS_OFFSET, bg = 'black')
w.pack()
rects = [w.create_rectangle(BAR_WIDTH * i, CANVAS_HEIGHT, BAR_WIDTH * (i + 1), CANVAS_HEIGHT, fill = '#' + ('%06x' % random.randint(0, 16777215))) for i in range(NUM_BAR)]
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
	while i == j:
		idx += 1
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
btnHeapSort = Button(text = 'Heap sort', command = heapSort)
btnHeapSort.pack()
btnQuickSort = Button(text = 'Quick sort', command = quickSort)
btnQuickSort.pack()
shuffle()
mainloop()
