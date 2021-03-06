
import itertools
import random
import copy
import pandas
import time
import datetime
import ast

class Pet:
    name =''
    power = 0
    toughness = 0
    level = 1
    exp = 0
    cost = 3
    honey = False

    def __init__(self, name, power, toughness, level, cost, honey):
        self.name = name
        self.power = power
        self.toughness = toughness
        self.level = level
        self.cost = cost
        self.honey = honey

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{0} L{1} ({2} / {3}){4}'.format(self.name, self.level, self.power, self.toughness,' (honey)' if self.honey else '')
    
    def __eq__(self, other):
        if not isinstance(other, Pet):
            return NotImplemented
        if self.name != other.name:
            return False
        elif self.power != other.power:
            return False
        elif self.toughness != other.toughness:
            return False
        elif self.level != other.level:
            return False
        elif self.honey != other.honey:
            return False
        else:
            return True
    
    def combineWith(self, pet):
        self.power = max(self.power, pet.power) + 1
        self.toughness = max(self.toughness, pet.toughness) + 1
        self.exp += 1

        if (self.level == 1 and self.exp == 2):
            self.level += 1
            self.exp = 0
        elif (self.level == 2 and self.exp == 3):
            self.level += 1

def stringToPet(string):
    string = string.strip()
    name = string.split()[0]
    level = int(string.split()[1][1:])
    power = int(string.split('/')[0].split('(')[1].strip())
    toughness = int(string.split('/')[1].split(')')[0].strip())
    honey = 'honey' in string
    output = Pet(name, power, toughness, level, 3, honey)
    return output

start_time = time.time()

fileSquads = []
with open ('squads.txt') as f:
    fileSquads = f.read().splitlines()
    
petSquads = []
for squadString in fileSquads:
    memberStrings = squadString[1:-1].split(', ')
    for perm in itertools.permutations(memberStrings):
        if len(perm) > 0:
            petSquads.append(list(perm))


petSquadStrings = [list(x) for x in set(tuple(x) for x in petSquads)]
petSquadStrings.sort()

allSquads = []
for squad in petSquadStrings:
    allSquads.append([stringToPet(pet) for pet in squad if len(pet) > 0])


allMatchups = list(itertools.product(allSquads, allSquads))
print('{0} unique matchups'.format(len(allMatchups)))

pre_df = time.time()

post_df = time.time()
last_time = post_df

wld = {}

while (sum(wld.values()) < 100):

    iter_start = time.time()

    try:
        print('checking if df exists')
        df
    except NameError:
        print('df didn\'t exist - checking csv')
        try:
            df = pandas.read_csv('output.csv', header=0, index_col=0)
        except FileNotFoundError:
            print('csv didn\'t exist')
            df = pandas.DataFrame(columns = [str(squad) for squad in allSquads], index = [str(squad) for squad in allSquads], dtype=object)
        print('done reading csv')
        df = df.applymap(lambda x: {'W': 0, 'L': 0, 'D': 0} if pandas.isnull(x) else ast.literal_eval(x))
        print('done applying map')
    first_wld = df['[]']['[]']
    wld = first_wld
    
    print('starting iteration {0}'.format(int(sum(wld.values()) / 2)))
    i = 0

    #for x in range(0, 50000):
    for matchup in allMatchups:
        squad1 = matchup[0]
        squad2 = matchup[1]

        originalTeam1 = [copy.deepcopy(member) for member in squad1]
        originalTeam2 = [copy.deepcopy(member) for member in squad2]
        team1 = [copy.deepcopy(member) for member in squad1]
        team2 = [copy.deepcopy(member) for member in squad2]

        def start(pet, team):
            if (team == team1):
                opponent = team2
            else:
                opponent = team1
            if ('Mosquito' in pet.name and len(opponent) > 0):
                hitPet = random.choice(opponent)
                hitPet.toughness -= pet.level
                if (hitPet.toughness <= 0):
                    death(hitPet, opponent)

        def death(pet, team):
            team.remove(pet)

            L1Horses = [pet for pet in team if pet.name == 'Horse' and pet.level == 1]
            L2Horses = [pet for pet in team if pet.name == 'Horse' and pet.level == 2]
            boost = len(L1Horses) + 2 * len(L2Horses)

            if ('Cricket' in pet.name):
                team.insert(0, Pet('Subcricket', 1 + boost, 1, 1, 0, False))
            elif ('Ant' in pet.name):
                if (len(team) > 0):
                    buffPet = random.choice(team)
                    buffPet.power += 2
                    buffPet.toughness += 1
            
            if (pet.honey):
                team.insert(0, Pet('Bee', 1 + boost, 1, 1, 0, False))

        def fight(team1, team2):

            [start(pet, team1) for pet in team1]
            [start(pet, team2) for pet in team2]

            while (len(team1) > 0 and len(team2) > 0):
                pet1 = team1[0]
                pet2 = team2[0]

                pet1.toughness -= pet2.power
                pet2.toughness -= pet1.power

                if (pet1.toughness <= 0):
                    death(pet1, team1)
                
                if (pet2.toughness <= 0):
                    death(pet2, team2)

            # Win
            if len(team1) > 0:
                df.at[str(originalTeam1), str(originalTeam2)]['W'] += 1
                df.at[str(originalTeam2), str(originalTeam1)]['L'] += 1
            # Loss
            elif len(team2) > 0:
                df.at[str(originalTeam1), str(originalTeam2)]['L'] += 1
                df.at[str(originalTeam2), str(originalTeam1)]['W'] += 1
            # Draw
            else:
                df.at[str(originalTeam1), str(originalTeam2)]['D'] += 1
                df.at[str(originalTeam2), str(originalTeam1)]['D'] += 1

        fight(team1, team2)

        i += 1

    print('-----')

    df.to_csv('output.csv')
    print(df)

    print('finished iteration {0} - total runtime: {1}'.format(int(sum(wld.values()) / 2), str(datetime.timedelta(seconds=int(time.time() - iter_start)))))

print('finished all iterations - total runtime: {0}'.format(str(datetime.timedelta(seconds=int(time.time() - start_time)))))
