

fileSquads = []
with open ('squads.txt') as f:
    fileSquads = f.read().splitlines()


for s in fileSquads:
    print(s)