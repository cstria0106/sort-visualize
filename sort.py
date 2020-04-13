import threading
from time import sleep
from typing import List

from main import Bar

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


def highlight(bars, color, delay):
    for bar in bars:
        bar.color = color
    sleep(delay)
    for bar in bars:
        bar.color = white


class Sorter:
    def __init__(self, data: List[Bar], delay, skip):
        self.data = data
        self.delay = delay
        self.sorting = False
        self.force_stop = False
        self.complete = False
        self.skip = skip
        self.count = 0

    def run(self):
        if len(self.data) == 0:
            return
        self.sorting = True
        self.complete = False
        self.force_stop = False
        self.count = 0
        thread = threading.Thread(target=self.qsort_thread, args=())
        thread.start()

    def stop(self):
        self.sorting = False
        self.force_stop = True

    def stalin_sort_thread(self):
        self.count = 0
        i = 0
        while i < len(self.data) - 1:
            if self.force_stop:
                self.complete = True
                return

            self.count += 1

            if self.count > self.skip:
                self.count = 0
                highlight((self.data[i], self.data[i + 1]), red, self.delay)

            killed = False
            if self.data[i].n > self.data[i + 1].n:
                del self.data[i + 1]
                killed = True

            if killed:
                i -= 1

            i += 1

        self.complete = True
        return

    def selection_sort_thread(self):
        self.count = 0
        for i in range(len(self.data) - 1):
            min_index = i
            for j in range(i + 1, len(self.data)):
                if self.force_stop:
                    self.complete = True
                    return

                self.count += 1

                if self.count > self.skip:
                    self.count = 0
                    highlight((self.data[min_index], self.data[j]), red, self.delay)

                if self.data[min_index].n > self.data[j].n:
                    min_index = j

            if self.force_stop:
                break

            temp = self.data[i]
            self.data[i] = self.data[min_index]
            self.data[min_index] = temp

            highlight((self.data[i],), green, self.delay)

        self.complete = True

    def qsort_thread(self):
        def qsort(i, j):
            if self.force_stop:
                self.complete = True
                return

            if i >= j:
                return

            left = i
            right = j
            pivot = i

            while left <= right:
                self.count += 1
                if self.count > self.skip:
                    self.count = 0
                    highlight((self.data[left], self.data[right]), red, self.delay)

                while self.data[left].n < self.data[pivot].n:
                    left += 1
                while self.data[right].n > self.data[pivot].n:
                    right -= 1
                if left <= right:
                    temp = self.data[left]
                    self.data[left] = self.data[right]
                    self.data[right] = temp
                    left += 1
                    right -= 1
            qsort(i, right)
            qsort(left, j)

        qsort(0, len(self.data) - 1)
        self.complete = True
        return
