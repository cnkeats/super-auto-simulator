
from PIL import Image
import numpy as np
import pandas
import ast


df = pandas.read_csv('newoutput.csv', header=0, index_col=0)
df = df.applymap(lambda x: {'W': 0, 'L': 0, 'D': 0} if pandas.isnull(x) else ast.literal_eval(x))

df = df.head(int(3450 / 5)).iloc[:, : int(3450 / 5)]

print('finished applying')

dfRows = list(df.index.values)
dfColumns = list(df.columns.values)

wld_dict = {}

data = np.zeros((3450, 3450, 3), dtype=np.uint8)

x = 0
y = 0
for row in dfRows:
    wld = [0, 0, 0]

    for column in dfColumns:
        cell_wld = df.at[row, column]

        r = int(cell_wld['L'] / 100 * 255)
        g = int(cell_wld['W'] / 100 * 255)
        b = int(cell_wld['D'] / 100 * 255)

        data[x, y] = [r, g, b]

        if ((x+1) % (int(3450 / 9)) == 0 or (y+1) % (int(3450 / 9)) == 0):
            data[x, y] = [255, 255, 255]
        x += 1
    
    if y % 256 == 0:
        print('finished row {0:,}'.format(y))

    x = 0
    y += 1
    wld_dict[row] = wld

print('done creating data')

image = Image.fromarray(data, 'RGB')
image.save('visualize.png')
image.show()
