from multiprocessing import Pool, Process, Event
from functools import partial
import os
import random
from time import sleep


def element(index, A, B, m):
    i, j = index
    res = 0
    for k in range(len(B)):
        res += A[i][k] * B[k][j]
    with open(f'output/element_{m}_{i}_{j}', 'w') as f:
        print(res, end='', file=f)


def dot_product(A, B, m):
    with Pool() as pool:
        pool.map(partial(element, A=A, B=B, m=m), ((i, j)
                 for i in range(len(A)) for j in range(len(B[0]))))

    result = []

    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            path = f'output/element_{m}_{i}_{j}'
            with open(path) as f:
                row.append(float(f.read()))
            os.remove(path)
        result.append(row)

    with open(f'output/matrix_{m}', 'w') as f:
        print(result, end='', file=f)


N = 10


def generation_loop(exit_event):
    m = 0
    while not exit_event.is_set():
        m += 1
        A = [[random.random() for _ in range(N)] for _ in range(N)]
        B = [[random.random() for _ in range(N)] for _ in range(N)]
        sleep(0.3)
        Process(target=dot_product, args=[A, B, m]).start()


def main():
    if not os.path.exists('output'):
        os.makedirs('output')
    exit_event = Event()
    Process(target=generation_loop, args=[exit_event]).start()
    while True:
        if input() == 'exit':
            exit_event.set()
            break


if __name__ == '__main__':
    main()
