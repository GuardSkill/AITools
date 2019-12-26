import pandas as pd
import numpy as np

single_column = np.array([1, 2, 3, 4, 5])

matrixs=[]
for column in range(5):
    matrix = np.tile(single_column, (30, 1))
    for i in range(30):
        if i%3==0:
            matrix[i, :]=np.array([4, 5,1, 2, 3])
            np.random.shuffle(matrix[i, 2:])
            np.random.shuffle(matrix[i, :2])
        else:
            np.random.shuffle(matrix[i, :])
    matrixs.append(matrix)


for column in range(5):
    arrays = [matrixs[j][:, column] for j in range(5)]
    data=np.stack(arrays, axis=1)
    df = pd.DataFrame(data)
    df.to_csv("csv_random_%d.csv"%column)

