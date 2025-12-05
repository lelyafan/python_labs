def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for cl in range(len(mat[0])):
        new_row = []
        for row in range(len(mat)):
            new_row.append(mat[row][cl])
        result.append(new_row)
    return result


print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))


def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for row in mat:
        result.append(sum(row))
    return result


print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))


def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for col in range(len(mat[0])):
        col_sum = 0
        for row in range(len(mat)):
            col_sum += mat[row][col]
        result.append(col_sum)
    return result


print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
