import numpy as np

matrix = np.array(((1, -1), (1, 2)))
output = np.array((0, 8))

result = np.linalg.solve(matrix, output)

print(result)