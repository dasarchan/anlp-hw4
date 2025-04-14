def bubble_sort(arr):
    """
    A buggy implementation of bubble sort.
    The bug is that the inner loop should go up to len(arr) - i - 1,
    but it incorrectly goes up to len(arr) - 1.
    """
    n = len(arr)
    for i in range(n):
        # Bug: Should be range(n - i - 1)
        for j in range(0, n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

if __name__ == "__main__":
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_arr)
    sorted_arr = bubble_sort(test_arr.copy())
    print("Sorted array:", sorted_arr)
    
    # Expected: [11, 12, 22, 25, 34, 64, 90]