min_gallop = 4

def insertion_sort(arr, left, right):                # Not used since it is less efficient than binary insertion sort, but basic operation for tim sort
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, left, mid, right):
    temp = []
    i, j = left, mid + 1
    
    count_left_run = count_right_run = 0
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
            count_left_run += 1
            count_right_run = 0
        else:
            temp.append(arr[j])
            j += 1
            count_right_run += 1
            count_left_run = 0
            
        if count_left_run >= min_gallop and i <= mid:
            pos = gallop(arr[i], arr, j, right)
            temp.extend(arr[j:pos])
            j = pos
            count_left_run = 0
            count_right_run = 0

        elif count_right_run >= min_gallop and j <= right:
            pos = gallop(arr[j], arr, i, mid)
            temp.extend(arr[i:pos])
            i = pos
            count_left_run = 0
            count_right_run = 0

    if i <= mid:         
        temp.extend(arr[i:mid+1])
    if j <= right:
        temp.extend(arr[j:right+1])
    arr[left:right+1] = temp

def tim_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    min_run = calc_min_run(n)
    
    runs = []
    
    start = 0
    while start < n:
        run_len = count_run_and_make_ascending(arr, start, n - 1)
        if run_len < min_run:
            final_run = min(min_run, n - start)
            binary_insertion_sort(arr, start, start + final_run - 1)
            run_len = final_run
        runs.append((start, run_len))
        start += run_len
    
    while len(runs) > 1:
        (run1_start, length1) = runs.pop(0)
        (run2_start, length2) = runs.pop(0)

        mid = run1_start + length1 - 1
        right = run2_start + length2 - 1
        merge(arr, run1_start, mid, right)

        runs.insert(0, (run1_start, length1 + length2))

    return arr

def calc_min_run(n):                #[...] 200 -> 50~50~50~50
    r = 0
    while n >= 64:
        r = 1 if n % 2 == 1 else r
        n = n//2
    return n + r

def count_run_and_make_ascending(arr, start, end):      #[2,4,6,8,10,12,7,...]
    if start >= end:
        return 1
    i = start + 1
    if arr[i] >= arr[i - 1]:
        while i <= end and arr[i] >= arr[i - 1]:
            i += 1
    else:
        while i <= end and arr[i] < arr[i - 1]:
            i += 1
        arr[start:i] = reversed(arr[start:i])
    return i - start

def binary_search(arr, left, right, key):       #[...,8,9,11,...] Insert 10
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] <= key:
            left = mid + 1
        else:
            right = mid - 1
    return left

def binary_insertion_sort(arr, left, right):            #Faster than insertion_sort() , both sorting can used to compare time used
    for i in range(left + 1, right + 1):
        key = arr[i]
        pos = binary_search(arr, left, i - 1, key)
        j = i
        while j > pos:
            arr[j] = arr[j - 1]
            j -= 1
        arr[pos] = key

def gallop(key, arr, start, end):                       #[2,3,4,5,7,8,11,12,19,...]  [1,20,21,22,...]
    if start > end:
        return start

    if arr[start] > key:                                #If the first element is already greater than key, return start
        return start

    last = start
    step = 1
    pos = start
    while pos <= end and arr[pos] <= key:
        last = pos
        pos = start + step
        step *= 2
    
    # Binary search in [last, min(pos, end)]
    left = last
    right = min(pos, end)
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] <= key:
            left = mid + 1
        else:
            right = mid - 1
    return left


    """ Create a random list and do code testing """
import random
number = list(range(1,1000))
sample = random.sample(number, 200)
print(sample)
print("\n")
print(sorted(sample))
print("\n")
print(tim_sort(sample))
print("\n")
print(sorted(sample) == tim_sort(sample)) 
