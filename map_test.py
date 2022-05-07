def map_test(cols):
    cols = map(lambda x: x+2, cols)
    return cols


print(*map_test([1,2,3,4]))
