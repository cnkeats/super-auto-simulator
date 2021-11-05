import random
import itertools
import copy
from anytree import Node, RenderTree, PreOrderIter, findall

class Pet:
    name = ""
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
    
    def combineWith(self, pet, team, bought=False):
        self.power = max(self.power, pet.power) + 1
        self.toughness = max(self.toughness, pet.toughness) + 1
        self.exp += 1

        if (self.level == 1 and self.exp == 2):
            self.level += 1
            self.exp = 0
        elif (self.level == 2 and self.exp == 3):
            self.level += 1


# ant beaver cricket duck fish horse mosquito otter pig

choiceDict = {}

possibleChoices = []
possibleChoices.append(Pet('Ant', 2, 1, 1, 3, False))
possibleChoices.append(Pet('Beaver', 2, 2, 1, 3, False))
possibleChoices.append(Pet('Cricket', 1, 2, 1, 3, False))
possibleChoices.append(Pet('Duck', 1, 2, 1, 3, False))
possibleChoices.append(Pet('Fish', 2, 3, 1, 3, False))
possibleChoices.append(Pet('Horse', 1, 1, 1, 3, False))
possibleChoices.append(Pet('Mosquito', 2, 2, 1, 3, False))
possibleChoices.append(Pet('Otter', 1, 2, 1, 3, False))
possibleChoices.append(Pet('Pig', 2, 2, 1, 3, False))
possibleChoices.append('HONEY1')
possibleChoices.append('HONEY2')
possibleChoices.append('HONEY3')
possibleChoices.append('APPLE1')
possibleChoices.append('APPLE2')
possibleChoices.append('APPLE3')
#possibleChoices.append('SELL 1')
#possibleChoices.append('SELL 2')
#possibleChoices.append('SELL 3')
possibleChoices.append('DONE')

choice = None


baseNode = Node(name='', gold=10, squad=[])

leaves = findall(baseNode, filter_=lambda node: len(node.children) == 0 and 'DONE' not in node.name)

while (len(leaves) > 0):
    for leaf in leaves:

        print()
        print('iterating choices for the following leaf:')
        for pre, fill, node in RenderTree(leaf):
            print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
            pass
        print()
        
        legalChoices = 0
        for choice in possibleChoices:
            choiceCopy = copy.deepcopy(choice)
            if choiceCopy == 'DONE':
                print('DONE')
                print(legalChoices)
                if (legalChoices == 0):
                    leaf.name = '{0} - DONE'.format(leaf.name)
                else:
                    Node(name = '{0} - DONE'.format(leaf.squad), gold = leaf.gold, squad = leaf.squad, parent = leaf)

            else:
                if (choiceCopy == 'HONEY1'):
                    if (len(leaf.squad) < 1 or leaf.gold < 3):
                        continue

                    print('HONEY1')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[0].honey = True

                    Node(name = honeySquad, gold = leaf.gold - 3, squad = honeySquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'HONEY2'):
                    if (len(leaf.squad) < 2 or leaf.gold < 3):
                        continue

                    print('HONEY2')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[1].honey = True

                    Node(name = honeySquad, gold = leaf.gold - 3, squad = honeySquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'HONEY3'):
                    if (len(leaf.squad) < 3 or leaf.gold < 3):
                        continue

                    print('HONEY3')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[2].honey = True

                    Node(name = honeySquad, gold = leaf.gold - 3, squad = honeySquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE1'):
                    if (len(leaf.squad) < 1 or leaf.gold < 3):
                        continue

                    print('APPLE1')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[0].power += 1
                    appleSquad[0].toughness += 1

                    Node(name = appleSquad, gold = leaf.gold - 3, squad = appleSquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE2'):
                    if (len(leaf.squad) < 2 or leaf.gold < 3):
                        continue

                    print('APPLE2')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[1].power += 1
                    appleSquad[1].toughness += 1

                    Node(name = appleSquad, gold = leaf.gold - 3, squad = appleSquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE3'):
                    if (len(leaf.squad) < 3 or leaf.gold < 3):
                        continue

                    print('APPLE3')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[2].power += 1
                    appleSquad[2].toughness += 1

                    Node(name = appleSquad, gold = leaf.gold - 3, squad = appleSquad, parent = leaf)
                    legalChoices += 1
                elif(choiceCopy == 'SELL 1'):
                    continue
                elif(choiceCopy == 'SELL 2'):
                    continue
                elif(choiceCopy == 'SELL 3'):
                    continue
                #elif(choiceCopy == 'COMBINE'):
                else:

                    gold = leaf.gold - choiceCopy.cost

                    if (gold < 0):
                        continue

                    # We chose a pet
                    print('PET - {0}'.format(choiceCopy))
                    legalChoices += 1

                    petName = choiceCopy.name

                    # Iterate over the existing squad to check if we can combine it
                    print('SQUAD: {0}'.format(leaf.squad))
                    for (index, member) in enumerate(leaf.squad):

                        # For every matching pet, combine it
                        if petName in member.name:
                            squad = copy.deepcopy(leaf.squad)
                            squad[index].combineWith(choiceCopy, squad, True)

                            # If the purchased pet was an Otter, we need to apply a buff to a friend if we have one
                            if ('Otter' in choiceCopy.name):

                                # Iterate over the of the squad
                                for (buffIndex, buffie) in enumerate(squad):

                                    # Only progress if we aren't ourselves
                                    if (buffIndex != index):

                                        # Prebuff squad is a copy of the existing, modified squad
                                        preBuffSquad = copy.deepcopy(squad)
                                        
                                        buffedUnit = copy.deepcopy(buffie)
                                        buffedUnit.power += squad[index].level
                                        buffedUnit.toughness += squad[index].level

                                        postBuffSquad = copy.deepcopy(preBuffSquad)
                                        postBuffSquad[buffIndex] = buffedUnit
                                        postBuffSquad[index] = copy.deepcopy(squad[index])

                                        Node(name = postBuffSquad, gold = gold, squad = postBuffSquad, parent = leaf)
                            else:
                                Node(name = squad, gold = gold, squad = squad, parent = leaf)
                        else:
                            print('invalid pet name - was {0} expecting {1}'.format(member.name, petName))
                    
                    # If the purchased pet was an Otter, we need to apply a buff to a friend if we have one
                    if ('Otter' in choiceCopy.name):
                        squad = copy.deepcopy(leaf.squad)
                        # Iterate over the of the squad
                        for (buffIndex, buffie) in enumerate(squad):
                            # Prebuff squad is a copy of the existing squad
                            preBuffSquad = copy.deepcopy(squad)
                            
                            buffedUnit = copy.deepcopy(buffie)
                            buffedUnit.power += choiceCopy.level
                            buffedUnit.toughness += choiceCopy.level
                            
                            horsePower = sum([pet.level for pet in leaf.squad if 'Horse' in pet.name])
                            choiceCopy.power += horsePower

                            postBuffSquad = copy.deepcopy(preBuffSquad) + [choiceCopy]
                            postBuffSquad[buffIndex] = buffedUnit

                            
                            Node(name = postBuffSquad, gold = gold, squad = postBuffSquad, parent = leaf)
                        if len(squad) == 0:
                            # Add the purchased pet to the end of the list
                            squad = copy.deepcopy(leaf.squad) + [choiceCopy]
                            Node(name = squad, gold = gold, squad = squad, parent = leaf)
                    else:
                        # Add the purchased pet to the end of the list

                        horsePower = sum([pet.level for pet in leaf.squad if 'Horse' in pet.name])
                        choiceCopy.power += horsePower

                        squad = copy.deepcopy(leaf.squad) + [choiceCopy]
                        Node(name = squad, gold = gold, squad = squad, parent = leaf)

    leaves = findall(baseNode, filter_=lambda node: len(node.children) == 0 and 'DONE' not in node.name)
    
    print()
    for pre, fill, node in RenderTree(baseNode):
        print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
        pass

    print('found {0} leaves'.format(len(leaves)))
    #input()

print('{0} possible teams'.format(len(findall(baseNode, filter_=lambda node: len(node.children) == 0))))

exit()


#print (list(itertools.permutations(petList, 3)))
allSquads = []

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