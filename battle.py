
import itertools
import random
import copy
import pandas
import time
import datetime
import ast
from multiprocessing import Pool

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

def battle(matchup):
    squad1 = [stringToPet(pet) for pet in matchup[0]]
    squad2 = [stringToPet(pet) for pet in matchup[1]]
    return fight(squad1, squad2)

def fight(team1, team2):

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
        #print('{0} died :('.format(pet))
        #print()
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
    
    originalTeam1 = [copy.deepcopy(member) for member in team1]
    originalTeam2 = [copy.deepcopy(member) for member in team2]

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
        return (originalTeam1, originalTeam2, {'W': 1, 'L': 0, 'D': 0}, {'W': 0, 'L': 1, 'D': 0})
    # Loss
    elif len(team2) > 0:
        return (originalTeam1, originalTeam2, {'W': 0, 'L': 1, 'D': 0}, {'W': 1, 'L': 0, 'D': 0})
    # Draw
    else:
        return (originalTeam1, originalTeam2, {'W': 0, 'L': 0, 'D': 1}, {'W': 0, 'L': 0, 'D': 1})

#while (sum(wld.values()) < 1):

if __name__ == "__main__":

    start_time = time.time()

    fileSquads = []
    with open ('squads.txt') as f:
        fileSquads = f.read().splitlines()

    petSquads = []
    for squadString in fileSquads:
        memberStrings = squadString[1:-1].split(', ')

        for perm in itertools.permutations(memberStrings):
            if len(perm) > 0:
                #print(list(perm))
                petSquads.append(list(perm))

    #petSquadStrings = [list(x) if len(x) > 0 else [] for x in set(tuple(x) for x in petSquads)]
    petSquadStrings = [list(x) if x[0] != '' else [] for x in set(tuple(x) for x in petSquads)]
    petSquadStrings.sort()

    #allSquads = []
    #for squad in petSquadStrings:
    #    allSquads.append([stringToPet(pet) for pet in squad if len(pet) > 0])
    allSquads = petSquadStrings

    allMatchups = list(itertools.product(allSquads, allSquads))
    print('{0:,} unique matchups'.format(len(allMatchups)))

    wld = {}

    try:
        df = pandas.read_csv('output_parallel.csv', header=0, index_col=0)
    except FileNotFoundError:
        print('csv didn\'t exist')
        df = pandas.DataFrame(columns = [str(squad) for squad in allSquads], index = [str(squad) for squad in allSquads], dtype=object)
    print('done reading csv')
    df = df.applymap(lambda x: {'W': 0, 'L': 0, 'D': 0} if pandas.isnull(x) else ast.literal_eval(x))
    print('done applying map')

    p = Pool(4)

    for i in range (0, 50):
        print('starting iteration {0:,}'.format(i))
        iter_start = time.time()

        count = 0
        for packed_data in p.imap(battle, allMatchups):
            #print(packed_data)
            count += 1

            team1_row = str([str(data) for data in packed_data[0]])
            team1_column = str([str(data) for data in packed_data[1]])
            team1_results = packed_data[2]
            team1_existing_results = df.at[team1_row, team1_column]
            team1_new_results = {'W': team1_existing_results['W'] + team1_results['W'], 'L': team1_existing_results['L'] + team1_results['L'], 'D': team1_existing_results['D'] + team1_results['D']}
            
            team2_row = str([str(data) for data in packed_data[1]])
            team2_column = str([str(data) for data in packed_data[0]])
            team2_results = packed_data[3]
            team2_existing_results = df.at[team2_row, team2_column]
            team2_new_results = {'W': team2_existing_results['W'] + team2_results['W'], 'L': team2_existing_results['L'] + team2_results['L'], 'D': team2_existing_results['D'] + team2_results['D']}
            
            #print(team1_new_results)
            #print(team2_new_results)

            df.at[team1_row, team1_column] = team1_new_results
            df.at[team2_row, team2_column] = team2_new_results

            if count % (len(allSquads) * 100) == 0 or count == len(allMatchups):
                print('finished {0:,} of {1:,} - {2} vs {3} now at {4}\n'.format(count, len(allMatchups), team1_row, team1_column, team1_new_results))

        print('-----')

        df.to_csv('output_parallel.csv')
        print(df)

        print('finished iteration {0:,} - total runtime: {1}'.format(i, str(datetime.timedelta(seconds=int(time.time() - iter_start)))))

    print('finished all iterations - total runtime: {0}'.format(str(datetime.timedelta(seconds=int(time.time() - start_time)))))

