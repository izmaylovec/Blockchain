import random
import time

class minheap:   
    def __init__(self):
        self.array = []
            
    def __getitem__(self, i):        
        return self.array[i]
    
    def __setitem__(self, i, a):
        self.array[i] = a

    def insert(self, elem):
        self.array.append(elem)
        i = len(self) - 1       
        while i > 0 and self[(i - 1) // 2] > self[i]:
            self[(i - 1) // 2], self[i] = self[i], self[(i - 1) // 2]
            i = (i - 1) // 2
        
    def __str__(self):
        return ' '.join(map(str, self.array))
     
    def __len__(self):
        return len(self.array)
    
    def childrennumber(self, i):
        if 2 * i + 2 < len(self):
            return 2
        if 2 * i + 1 < len(self):
            return 1
        return 0
        
    def extract(self):
        ans = self[0]
        self[0] = self[-1]
        self.array.pop()
        i = 0
        while i < len(self) and self.childrennumber(i) > 0:
            min_child = 2 * i + 1
            if 2 * i + 2 < len(self) and self[2 * i + 2] < self[2 * i + 1]:
                min_child = 2 * i + 2
            if self[i] > self[min_child]:
                self[i], self[min_child] = self[min_child], self[i]
                i = min_child
            else:
                i = len(self)                   
        return ans
    
    
def makeheap(A):
    ans = minheap()
    for i in A:
        ans.insert(i)
    return ans


def heapsort(A):
    B = makeheap(A)
    ans = []
    for i in range(len(B)):
        ans.append(B.extract())
    return ans


def mergesort(A):
    if len(A) > 1:
        mid = len(A) // 2
        B = mergesort(A[:mid])
        C = mergesort(A[mid:])
        return merge(B, C)
    return A


def merge(B, C):
    n = len(B)
    m = len(C)
    A = []
    i = 0
    j = 0
    while i < n and j < m:
        while i < n and B[i] <= C[j]:
            A.append(B[i])
            i += 1
        if i < n:
            while j < m and C[j] <= B[i]:
                A.append(C[j])
                j += 1
    
    while i < n:
        A.append(B[i])
        i += 1
    while j < m:
        A.append(C[j])
        j += 1
    return A


def qsort(A, beg, end):
    if beg < end:        
        pivot = partition(A, beg, end)
        qsort(A, beg, pivot)
        qsort(A, pivot + 1, end)
    

def partition(A, beg, end):
    mid = (beg + end) // 2
    if A[mid] < A[beg]:
        A[mid], A[beg] = A[beg], A[mid]
    if A[end] < A[beg]:
        A[end], A[beg] = A[beg], A[end]
    if A[mid] < A[end]:
        A[mid], A[end] = A[end], A[mid]
    
    pivot = A[end]
    
    i = beg - 1
    j = end + 1
    
    while True:
        i += 1
        while A[i] < pivot:
            i += 1
        j -= 1
        while A[j] > pivot:
            j -= 1        
        if i >= j:
            return j
        
        A[i], A[j] = A[j], A[i]
        
    
def randlist():
    return [random.randint(0, 10000) for i in range(100000)]

qsorttime = 0
mergesorttime = 0
heapsorttime = 0
builtinsorttime = 0
for i in range(1):
    A = random.choices(range(100), k=100000)
    h = time.clock()
    B = qsort(A, 0, len(A) - 1)
    qsorttime += time.clock() - h
    h = time.clock()
    B = mergesort(A)
    mergesorttime += time.clock() - h
    h = time.clock()
    B = heapsort(A)
    heapsorttime += time.clock() - h
    h = time.clock()
    B = sorted(A)
    builtinsorttime += time.clock() - h
    
    
print(qsorttime / 100, mergesorttime / 100, heapsorttime / 100, builtinsorttime / 100)
