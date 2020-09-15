"""
input : [1, 4, 5, 2, 3, 7, 8, 20, 10, 9]
output: sort array
using sort merge algorithm
"""
a = [38, 27, 43, 3, 9, 82, 10]

def merge_sort(arr, l, r):
    """
    if r > l
        1. find the middle point to divide the array into two halves:
            middle m = (l + r) / 2
        2. Call merge Sort for first half
            Call merge Sort (arr, l, m)
        3. Call merge sort for second half:
            Call merge Sort (arr, m +1, r)
        4. Merge the two halves sorted in step 2 and 3:
            Call merge(arr, l, m, r)
    """

if __name__ == "__main__":
    print('I love u')
