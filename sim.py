import random
import itertools

class Pet:
    name = ""
    power = 0
    toughness = 0
    level = 1
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

def getPetFamily(name, power, toughness):
    petFamily = []

    # Basic Level 1
    petFamily += [Pet(name, power, toughness, 1, 3, False)]

    # Basic Level 1 x2
    petFamily += [Pet(name, power+1, toughness+1, 1, 6, False)]

    # Basic Level 2
    petFamily += [Pet(name, power+2, toughness+2, 2, 9, False)]

    # Basic Level 2 x2
    petFamily += [Pet(name, power+3, toughness+3, 2, 12, False)]

    # Basic Level 2 x3
    petFamily += [Pet(name, power+4, toughness+4, 2, 15, False)]
    
    # Basic Level 3
    petFamily += [Pet(name, power+5, toughness+5, 2, 18, False)]


    return petFamily

pets = {}
#pets['ant'] = ['Ant', 2, 1, 1, 3, False]
#pets['ant_H'] = ['Ant', 2, 1, 1, 6, True]
#pets['beaver'] = ['Beaver', 2, 2, 1, 3, False]
#pets['beaver_H'] = ['Beaver', 2, 2, 1, 6, True]
#pets['cricket'] = ['Cricket', 1, 2, 1, 3, False]
#pets['cricket_H'] = ['Cricket', 1, 2, 1, 6, True]
#pets['duck'] = ['Duck', 1, 2, 1, 3, False]
#pets['duck_H'] = ['Duck', 1, 2, 1, 6, True]
#pets['fish'] = ['Fish', 2, 3, 1, 3, False]
#pets['fish_H'] = ['Fish', 2, 3, 1, 6, True]
#pets['horse'] = ['Horse', 1, 1, 1, 3, False]
#pets['horse_H'] = ['Horse', 1, 1, 1, 6, True]
#pets['mosquito'] = ['Mosquito', 2, 2, 1, 3, False]
#pets['mosquito_H'] = ['Mosquito', 2, 2, 1, 6, True]
#pets['otter'] = ['Otter', 1, 2, 1, 3, False]
#pets['otter_H'] = ['Otter', 1, 2, 1, 6, True]
#pets['pig'] = ['Pig', 2, 2, 1, 3, False]
#pets['pig_H'] = ['Pig', 2, 2, 1, 6, True]

pets['ant1'] = ['Ant', 2, 1, 1, 3, False]
pets['ant+'] = ['Ant', 3, 2, 1, 6, False]
pets['ant2'] = ['Ant', 4, 3, 2, 9, False]
pets['ant1_H'] = ['Ant', 2, 1, 1, 6, True]
pets['ant+_H'] = ['Ant', 3, 2, 1, 9, True]
pets['ant2_H'] = ['Ant', 4, 3, 2, 12, True]

print(getPetFamily('Ant', 2, 1))

wld = [0, 0, 0]

petList = list(pets.keys())
petList.sort()
exit()

def pet(petname):
    name = pets[petname][0]
    power = pets[petname][1]
    toughness = pets[petname][2]
    level = pets[petname][3]
    cost = pets[petname][4]
    honey = pets[petname][5]

    return Pet(name, power, toughness, level, cost, honey)

#print (list(itertools.permutations(petList, 3)))
all3MemberSquads = list(itertools.product(petList, petList, petList))
all2MemberSquads = list(itertools.product(petList, petList))
all1MemberSquads = list(itertools.product(petList))

allSquads = all1MemberSquads + all2MemberSquads + all3MemberSquads

allLegitimateSquads = []

for squad in allSquads:

    costs = [pet(squadMember).cost for squadMember in squad]
    cost = sum(costs)

    #if (p1.cost + p2.cost + p3.cost < 10):
    if (cost < 10):
        allLegitimateSquads.append(squad)
        print('accepting {0}'.format(squad))
    else:
        print('rejecting {0}'.format(squad))
    
    temp = [pet(squadMember)for squadMember in squad  if 'Horse' in pet(squadMember).name ]
    
    if len(temp) > 0:
        print(temp)
        input()
    

print('{0} unique squads'.format(len(all3MemberSquads)))
print('{0} unique legal squads'.format(len(allLegitimateSquads)))

allMatchups = list(itertools.product(all3MemberSquads, all3MemberSquads))
print('{0} unique matchups'.format(len(allMatchups)))
allLegalMatchups = list(itertools.product(allLegitimateSquads, allLegitimateSquads))
print('{0} unique legal matchups'.format(len(allLegalMatchups)))

#debug = True
debug = False

results = {}

exit()
#for x in range(0, 50000):
for matchup in allMatchups:
    squad1 = matchup[0]
    squad2 = matchup[1]

    originalTeam1 = [pet(member) for member in squad1]
    originalTeam2 = [pet(member) for member in squad2]
    team1 = [pet(member) for member in squad1]
    team2 = [pet(member) for member in squad2]

    def start(pet, team):
        if (team == team1):
            opponent = team2
        else:
            opponent = team1
        
        if ('Mosquito' in pet.name):
            hitPet = random.choice(opponent)
            if (debug):
                print('{0} was hit by a mosquito'.format(hitPet))
            hitPet.toughness -= pet.level
            if (debug):
                print('{0}'.format(hitPet))
                print()
            if (hitPet.toughness <= 0):
                death(hitPet, opponent)

    def death(pet, team):
        if (debug):
            print('{0} died :('.format(pet))
            print()
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

        if (debug):
            print('--------------------------------------------------')
            print(team1)
            print('vs')
            print(team2)
            print()

        [start(pet, team1) for pet in team1]
        [start(pet, team2) for pet in team2]

        while (len(team1) > 0 and len(team2) > 0):
            pet1 = team1[0]
            pet2 = team2[0]
                
            if (debug):
                print('--------------------------------------------------')
                print(team1)
                print('vs')
                print(team2)
                print()

            if (debug):
                print ('{0} fights {1}'.format(pet1, pet2))

            pet1.toughness -= pet2.power
            pet2.toughness -= pet1.power

            if (pet1.toughness <= 0):
                death(pet1, team1)
            
            if (pet2.toughness <= 0):
                death(pet2, team2)
            

        if (repr(originalTeam1) not in results.keys()):
            results[repr(originalTeam1)] = [0,0,0]
            
        if (len(team1) > 0 ):
            if (debug):
                print('Team 1 wins!')
            wld[0] += 1
            results[repr(originalTeam1)][0] += 1
        elif (len(team2) > 0):
            if (debug):
                print('Team 2 wins!')
            wld[1] += 1
            results[repr(originalTeam1)][1] += 1
        else:
            if (debug):
                print('Draw!')
            wld[2] += 1
            results[repr(originalTeam1)][2] += 1



        if (debug):
            print('--------------------------------------------------')
            print(team1)
            print('vs')
            print(team2)
            print()
            print('==================================================')

    fight(team1, team2)
    #break

print(wld)

for key in results.keys():
    print('{0} - {1}'.format(key, results[key]))

print('-----')
temp = {k: v for k, v in sorted(results.items(), key=lambda item: item[1])}

for key in temp.keys():
    print('{0} - {1}'.format(key, temp[key]))