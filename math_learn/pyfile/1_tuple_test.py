import json
from py_lib.vectors import dot

# 新建一个矩阵
matrix = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9)
)

print(matrix)
zip_matrix = zip(*matrix)
for i in zip_matrix:
    print(i)

vector_1 = (1, 1, 1)
vector_2 = (2, 2)

print(dot(vector_1, vector_2))

print([i for i in range(0, 10)])
print(tuple(i for i in range(0, 10)))
