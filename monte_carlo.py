# Данная программа считает объем гиперсферы в 8-мерном пространстве с радиусом = 1

import math
import random
import time
import multiprocessing


def check_in_hypersphere(a):
    result = 0
    for i in range(8):
        result += (1 - a[i]) ** 2
    if result > 1:
        return False
    return True

def count_volume(N):
    size = 2
    M = 0

    for i in range(N):
        a = []
        for j in range(8):
            a.append(random.uniform(0, size))
        if check_in_hypersphere(a):
            M += 1
    return size**8 * M / N

def test_all(pool, n):
    arr = pool.map(count_volume, [10000] * n)
    result = 0
    for i in range(n):
        result += arr[i]
    return result / n

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    t0 = time.time()
    print("Volume =", test_all(pool, 50))
    print("Expected volume = 4.0587")
    print("Time spent:", time.time() - t0)
else:
    print("__name__:", __name__)
