import random
import time
from numba import njit, prange
from numba.typed import List
import bogosort_without_numba as bgw

@njit
def bogoSort(arr):
    while is_sorted(arr):
        sort(arr)

@njit
def is_sorted(arr):
    for i in range(0, len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return True
    return False

@njit
def sort(arr):
    size = len(arr)
    for i in range(0, size):
        r = random.randint(0, size - 1)
        arr[i], arr[r] = arr[r], arr[i]

print("Данная программа сортирует массив от 0 до n-1 с помощью сортировки bogosort")
size = 0
while size < 1 or size > 13:
    size = int(input("Введите количество элементов массива (от 1 до 13): "))
arr = bgw.create_arr(size)

t0 = time.time()
typed_arr = List()
[typed_arr.append(i) for i in arr]
bogoSort(typed_arr)
print("Время сортировки с ускорением: ", time.time() - t0)

bgw.main(size)

print(typed_arr)
