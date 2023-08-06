def print_arr(arr):
    for row in arr:
        if isinstance(row, list):
            print_arr(row)
        else:
            print(row)
