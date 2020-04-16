from comparable import C
from typing import List, Tuple


class heap:

    # List of tuples where the first
    # item is the distance
    def __init__(self, l: List[C]):
        self._h = l[:] # make a copy of l

        # keep a dictionary mapping
        # vertex names to indices
        self._d = dict()
        for i in range(len(l)):
            self._d[l[i][1]] = i

        self.heapify()

        # create a dictionary that maps vertex names
        # to indices in the heap

    # index of left child
    def left(self, i: int):
        return 2*i + 1

    # index of right child
    def right(self, i:int):
        return 2*i + 2

    def leftval(self, i:int):
        return self._h[self.left(i)]

    def rightval(self, i):
        return self._h[self.right(i)]

    def parent(self, i:int):
        return (i - 1)//2

    def parentval(self, i: int):
        return self._h[self.parent(i)]

    def __len__(self):
        return len(self._h)

    def heapify(self):
        for i in range(self.parent(len(self) - 1), -1, -1):
            self.siftdown(i)

    def delete_root(self) -> C:

        t = self._h[0]  # the min
        if len(self) == 1:
            self._h.pop()
            return t

        self._h[0] = self._h.pop()
        self.siftdown(0)
        return t

    def heapsort(self):
        """
        Heap is destroyed as we build sorted list
        :return:
        """
        l = []
        while len(self) > 0:
            l.append(self.delete_root())
        return l

    def siftup(self, i: int):
        """
        Push value at index i up the heap towards
        the root.
        :param i:
        :return:
        """

        while i > 0 and self._h[i][0] < self.parentval(i)[0]:

            (self._h[i], self._h[self.parent(i)]) = \
            (self._h[self.parent(i)], self._h[i])
            # update dictionary for vertices to
            # refer to proper list index
            self._d[self._h[i][1]] = i
            self._d[self._h[self.parent(i)][1]] = self.parent(i)
            i = self.parent(i)

    def insert(self,v)->None:
        self._h.append(v)
        self._d[v[1]] = len(self)-1
        self.siftup(len(self)-1)

    def decrease(self, v: C, d: int) -> None:
        """
        Decrease the key value at v
        :param v:
        :param d:
        :return:
        """
        self._h[self._d[v]] = (d,v)
        self.siftup(self._d[v])



    def siftdown(self, i: int) -> None:
        """
        :param i: index of heap node sifting down
        :return: None, side effect heap is modified
        """

        curr = i # current heap node

        while self.left(curr) < len(self) and         \
                (self.leftval(curr)[0] < self._h[curr][0]):

            smaller_child = self.left(curr)

            # pick the smaller of the two children
            if smaller_child < len(self) - 1 and  \
               self.rightval(curr)[0] < self.leftval(curr)[0]:
                smaller_child = smaller_child + 1

            # swap with parent if parent is
            # larger than smaller child
            if self._h[smaller_child] < self._h[curr]:

                # swap the parent and smaller child
                (self._h[smaller_child], self._h[curr]) = \
                (self._h[curr], self._h[smaller_child])

                # update the vertex/index dictionary
                self._d[self._h[smaller_child][1]] = smaller_child
                self._d[self._h[curr][1]] = curr

                curr = smaller_child

