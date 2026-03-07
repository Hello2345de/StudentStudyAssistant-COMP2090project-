def insertion_sort(arr, left, right):
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
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    temp.extend(arr[i:mid+1])
    temp.extend(arr[j:right+1])
    arr[left:right+1] = temp

def tim_sort(arr):
    n = len(arr)
    min_run = 32

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, size * 2):
            mid = left + size - 1
            right = min(left + size * 2 - 1, n - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2

    return arr
#Code Explanation:

#insertion_sort: sorts small segments efficiently (adaptive on nearly sorted data).
#merge: combines two sorted halves using temporary storage.
#tim_sort: first creates small sorted runs with insertion sort, then merges them in doubling sizes.
#This is a simplified version; real TimSort includes galloping and dynamic min_run calculation.
