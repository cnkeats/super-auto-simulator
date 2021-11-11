#
import pandas
import ast

from pandas.core.frame import DataFrame

df = pandas.read_csv('output.csv', header=0, index_col=0)

#df = df.head(10).iloc[:, : 10]

print(df)


dfRows = list(df.index.values)
dfColumns = list(df.columns.values)

wld_dict = {}

for row in dfRows:
    wld = [0, 0, 0]
    for column in dfColumns:
        #print('{0} vs {1} - {2}'.format(row, column, df.at[row, column]))
        cell_wld = ast.literal_eval(df.at[row, column])
        wld[0] += cell_wld['W']
        wld[1] += cell_wld['L']
        wld[2] += cell_wld['D']
    #print('{0} results are {1}'.format(row, wld))
    wld_dict[row] = wld

out_dict = sorted(wld_dict.keys(), key=lambda k: (wld_dict[k][0], wld_dict[k][2]), reverse=True)

out_df = DataFrame(index=out_dict, columns=['Pet 3', 'Pet 2', 'Pet 1', '', 'Wins', 'Losses', 'Draws', '', 'Winrate', 'Lossrate', 'Drawrate'])

for x in out_dict:
    #print('{0}\t - {1}'.format(wld_dict[x], x))
    squadString = x[1:-1]

    pet1 = squadString.split(', ')[0]
    pet2 = squadString.split(', ')[1] if len(squadString.split(', ')) > 1  else ''
    pet3 = squadString.split(', ')[2] if len(squadString.split(', ')) > 2  else ''

    wins = wld_dict[x][0]
    losses = wld_dict[x][1]
    draws = wld_dict[x][2]
    
    out_df.at[x, 'Pet 1'] = pet1
    out_df.at[x, 'Pet 2'] = pet2
    out_df.at[x, 'Pet 3'] = pet3

    out_df.at[x, 'Wins'] = wins
    out_df.at[x, 'Losses'] = losses
    out_df.at[x, 'Draws'] = draws

out_df.to_excel('leaderboard.xlsx', index=False)
