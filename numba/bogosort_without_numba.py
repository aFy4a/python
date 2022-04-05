import random
import time

def create_arr(size):
    arr = []
    i = 0
    while len(arr) < size:
        t = random.randint(0, size - 1)
        if t in arr:
            continue
        arr.append(t)
        i += 1
    return arr

def bogoSort(arr):
    while is_sorted(arr):
        sort(arr)

def is_sorted(arr):
    for i in range(0, len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return True
    return False

def sort(arr):
    size = len(arr)
    for i in range(0, size):
        r = random.randint(0, size - 1)
        arr[i], arr[r] = arr[r], arr[i]

def main(size):
    arr = create_arr(size)
    t0 = time.time()
    bogoSort(arr)
    print("Время сортировки без ускорения:", time.time() - t0)
