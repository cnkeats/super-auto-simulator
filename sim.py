import random
import itertools
import copy
from anytree import Node, RenderTree, PreOrderIter, findall
from anytree.exporter import DotExporter
import traceback

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

def encode(item):
    if isinstance(item, Pet):
        pet = item
        return '{0} L{1}({2}) ({3} / {4}){5}'.format(pet.name, pet.level, pet.exp, pet.power, pet.toughness,' (honey)' if pet.honey else '')
    elif isinstance(item, list):
        output = '['
        for pet in item:
            output += encode(pet) + ','
        output += ']'
        return output
    else:
        return ''

def createNode(name, gold, squad, bonusChoices, petsBought, foodBought, parent):
    
    def isDuplicate(node):
        if 'DONE' in node.name and 'DONE' not in name:
            return False
        if 'DONE' in name and 'DONE' not in node.name:
            return False
        if node.gold != gold:
            #print('    gold mismatch!')
            #print('{0} compared to {1}'.format(squad, node.squad))
            return False
        if node.petsBought != petsBought:
            return False
        if node.foodBought != foodBought:
            return False
        if len(squad) != len(node.squad):
            #print('    different count!')
            #print('{0} compared to {1}'.format(squad, node.squad))
            return False
        if len(bonusChoices) != len(node.bonusChoices):
            #print('    bonus count mismatch!')
            #print('{0} compared to {1}'.format(squad, node.squad))
            return False
        for i in range(0, len(squad)):
            if squad[i] != node.squad[i]:
                #print('    squad[{0}] mismatch!'.format(i))
                #print('{0} compared to {1}'.format(squad, node.squad))
                return False
        for i in range(0, len(bonusChoices)):
            if bonusChoices[i] != node.bonusChoices[i]:
                #print('Bonus Choices were not equal! {0} compared to {1}'.format(bonusChoices, node.bonusChoices))
                return False
        #print('MATCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        #print('{0} compared to {1}'.format(squad, node.squad))
        return True

    # for some reason, using 'stop' makes the filter not work
    #leaves = findall(baseNode, filter_=lambda node: isDuplicate(node), stop=lambda nodex: isDuplicate(nodex))
    leaves = findall(baseNode, filter_=lambda node: isDuplicate(node))
    
    if len(leaves) > 0 and leaves[0] != baseNode:
        #print('FOUND DUPLICATE - not adding new node!')
        #print(leaves[0])
        #input()
        pass
    else:
        Node(name = name, gold = gold, squad = squad, bonusChoices = bonusChoices, petsBought = petsBought, foodBought = foodBought, parent = parent)
        #print('No duplicate - created new node!')

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
possibleChoices.append('HONEY 1')
possibleChoices.append('HONEY 2')
possibleChoices.append('HONEY 3')
possibleChoices.append('APPLE 1')
possibleChoices.append('APPLE 2')
possibleChoices.append('APPLE 3')
possibleChoices.append('SELL 1')
possibleChoices.append('SELL 2')
possibleChoices.append('SELL 3')
possibleChoices.append('REROLL')
possibleChoices.append('DONE')

duckCount = 0

choice = None


baseNode = Node(name='', gold=10, squad=[], bonusChoices=[], petsBought=0, foodBought=0)
#baseNode = Node(name=str(copy.deepcopy(possibleChoices[0])), gold=7, squad=[copy.deepcopy(possibleChoices[0])], bonusChoices=[])

leaves = findall(baseNode, filter_=lambda node: len(node.children) == 0 and 'DONE' not in node.name)

while (len(leaves) > 0):
    for leaf in leaves:

        #print()
        #print('iterating choices for the following leaf:')
        #for pre, fill, node in RenderTree(leaf):
        #    print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
        #    pass
        #print()
        
        legalChoices = 0
        for choice in possibleChoices + leaf.bonusChoices:
            choiceCopy = copy.deepcopy(choice)
            if choiceCopy == 'DONE':
                #print('DONE')
                if (legalChoices == 0):
                    leaf.name = '{0} - DONE'.format(leaf.name)
                else:
                    createNode('{0} - DONE'.format(leaf.squad), leaf.gold, leaf.squad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought, leaf)

            else:
                if (choiceCopy == 'HONEY 1'):
                    if (len(leaf.squad) < 1 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('HONEY 1')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[0].honey = True

                    createNode(honeySquad, leaf.gold - 3, honeySquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'HONEY 2'):
                    if (len(leaf.squad) < 2 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('HONEY 2')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[1].honey = True

                    createNode(honeySquad, leaf.gold - 3, honeySquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'HONEY 3'):
                    if (len(leaf.squad) < 3 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('HONEY 3')
                    
                    honeySquad = copy.deepcopy(leaf.squad)
                    honeySquad[2].honey = True

                    createNode(honeySquad, leaf.gold - 3, honeySquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE 1'):
                    if (len(leaf.squad) < 1 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('APPLE 1')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[0].power += 1
                    appleSquad[0].toughness += 1
                    #appleSquad[0].name += ' (apple)'

                    createNode(appleSquad, leaf.gold - 3, appleSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE 2'):
                    if (len(leaf.squad) < 2 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('APPLE 2')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[1].power += 1
                    appleSquad[1].toughness += 1
                    #appleSquad[1].name += ' (apple)'

                    createNode(appleSquad, leaf.gold - 3, appleSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'APPLE 3'):
                    if (len(leaf.squad) < 3 or leaf.gold < 3 or leaf.foodBought == 1):
                        continue

                    #print('APPLE 3')
                    
                    appleSquad = copy.deepcopy(leaf.squad)
                    appleSquad[2].power += 1
                    appleSquad[2].toughness += 1
                    #appleSquad[2].name += ' (apple)'

                    createNode(appleSquad, leaf.gold - 3, appleSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought + 1, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'SELL 1'):
                    if (len(leaf.squad) < 1):
                        continue

                    #print('SELL 1')

                    sellSquad = copy.deepcopy(leaf.squad)
                    soldFriend = sellSquad.pop(0)
                    change = soldFriend.level

                    if ('Beaver' in soldFriend.name):
                        # Add health to other units. We are always limited to 3 units in these scenarios, so we can just blindly apply it to all units
                        for friend in sellSquad:
                            friend.toughness += soldFriend.level
                    elif ('Duck' in soldFriend.name):
                        # Add extra possible choices to the list for each animal FOR THIS LEAF ONLY
                        bonusChoices = copy.deepcopy(leaf.bonusChoices)
                        for choice in [copy.deepcopy(choice) for choice in possibleChoices if isinstance(choice, Pet)]:
                            buffedChoice = choice
                            buffedChoice.power += soldFriend.level
                            buffedChoice.toughness += soldFriend.level
                            bonusChoices.append(buffedChoice)
                        createNode(str(sellSquad) + ' (sold 1)', leaf.gold + change, sellSquad, bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                        continue
                    elif ('Pig' in soldFriend.name):
                        change += soldFriend.level

                    createNode(str(sellSquad) + ' (sold 1)', leaf.gold + change, sellSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'SELL 2'):
                    if (len(leaf.squad) < 2):
                        continue

                    #print('SELL 2')

                    sellSquad = copy.deepcopy(leaf.squad)
                    soldFriend = sellSquad.pop(1)
                    change = soldFriend.level

                    if ('Beaver' in soldFriend.name):
                        # Add health to other units. We are always limited to 3 units in these scenarios, so we can just blindly apply it to all units
                        for friend in sellSquad:
                            friend.toughness += soldFriend.level
                    elif ('Duck' in soldFriend.name):
                        # Add extra possible choices to the list for each animal FOR THIS LEAF ONLY
                        bonusChoices = copy.deepcopy(leaf.bonusChoices)
                        for choice in [copy.deepcopy(choice) for choice in possibleChoices if isinstance(choice, Pet)]:
                            buffedChoice = choice
                            buffedChoice.power += soldFriend.level
                            buffedChoice.toughness += soldFriend.level
                            bonusChoices.append(buffedChoice)
                        createNode(str(sellSquad) + ' (sold 2)', leaf.gold + change, sellSquad, bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                        continue
                    elif ('Pig' in soldFriend.name):
                        change += soldFriend.level

                    createNode(str(sellSquad) + ' (sold 1)', leaf.gold + change, sellSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                    legalChoices += 1
                elif(choiceCopy == 'SELL 3'):
                    if (len(leaf.squad) < 3):
                        continue

                    #print('SELL 3')

                    sellSquad = copy.deepcopy(leaf.squad)
                    soldFriend = sellSquad.pop(2)
                    change = soldFriend.level

                    if ('Beaver' in soldFriend.name):
                        # Add health to other units. We are always limited to 3 units in these scenarios, so we can just blindly apply it to all units
                        for friend in sellSquad:
                            friend.toughness += soldFriend.level
                    elif ('Duck' in soldFriend.name):
                        # Add extra possible choices to the list for each animal FOR THIS LEAF ONLY
                        bonusChoices = copy.deepcopy(leaf.bonusChoices)
                        for choice in [copy.deepcopy(choice) for choice in possibleChoices if isinstance(choice, Pet)]:
                            buffedChoice = choice
                            buffedChoice.power += soldFriend.level
                            buffedChoice.toughness += soldFriend.level
                            bonusChoices.append(buffedChoice)
                        createNode(str(sellSquad) + ' (sold 3)', leaf.gold + change, sellSquad, bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                        continue
                    elif ('Pig' in soldFriend.name):
                        change += soldFriend.level

                    createNode(str(sellSquad) + ' (sold 1)', leaf.gold + change, sellSquad, leaf.bonusChoices, leaf.petsBought, leaf.foodBought, leaf)
                    legalChoices += 1
                #elif(choiceCopy == 'COMBINE'):
                elif(choiceCopy == 'REROLL'):
                    if (leaf.gold < 1):
                        continue

                    # If our gold + animal levels is less than 4 before rolling it is impossible to buy anything, so we can prune those branches
                    if (leaf.gold + sum([pet.level for pet in leaf.squad]) < 4):
                        continue

                    # If we haven't hit max pets bought or food bought, we can assume that we have perfect luck instead of continuing this branch, preventing reroll spam
                    if (leaf.petsBought != 3 and leaf.foodBought != 1):
                        continue

                    createNode(str(leaf.squad) + ' (reroll)', leaf.gold - 1, leaf.squad, [], 0, 0, leaf)
                    pass
                else:

                    gold = leaf.gold - choiceCopy.cost

                    if (gold < 0 or leaf.petsBought == 3):
                        continue

                    # We chose a pet
                    #print('PET - {0}'.format(choiceCopy))
                    legalChoices += 1

                    petName = choiceCopy.name

                    # Iterate over the existing squad to check if we can combine it
                    #print('SQUAD: {0}'.format(leaf.squad))
                    for (index, member) in enumerate(leaf.squad):
                    
                        # For every matching pet, combine it
                        if petName in member.name:
                            squad = copy.deepcopy(leaf.squad)
                            squad[index].combineWith(choiceCopy)

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

                                        createNode(postBuffSquad, gold, postBuffSquad, leaf.bonusChoices, leaf.petsBought + 1, leaf.foodBought, leaf)
                            else:
                                createNode(squad, gold, squad, leaf.bonusChoices, leaf.petsBought + 1, leaf.foodBought, leaf)
                                pass
                        else:
                            #print('invalid pet name - was {0} expecting {1}'.format(member.name, petName))
                            pass
                    
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
                            
                            createNode(postBuffSquad, gold, postBuffSquad, leaf.bonusChoices, leaf.petsBought + 1, leaf.foodBought, leaf)
                        if len(squad) == 0:
                            # Add the purchased pet to the end of the list
                            squad = copy.deepcopy(leaf.squad) + [choiceCopy]
                            createNode(squad, gold, squad, leaf.bonusChoices, leaf.petsBought + 1, leaf.foodBought, leaf)
                    else:
                        # Add the purchased pet to the end of the list
                        horsePower = sum([pet.level for pet in leaf.squad if 'Horse' in pet.name])
                        choiceCopy.power += horsePower

                        squad = copy.deepcopy(leaf.squad) + [choiceCopy]
                        createNode(squad, gold, squad, leaf.bonusChoices, leaf.petsBought + 1, leaf.foodBought, leaf)

    leaves = findall(baseNode, filter_=lambda node: len(node.children) == 0 and 'DONE' not in node.name)
    
    for pre, fill, node in RenderTree(baseNode):
        #print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
        pass

    print('found {0} leaves'.format(len(leaves)))
    #input()

allSquadNodes = findall(baseNode, filter_=lambda node: 'DONE' in node.name and len(node.bonusChoices)==0)

#strings = ['{0} - {1}g - {2}'.format(str(node.squad), str(node.gold), str(len(node.bonusChoices))) for node in allSquadNodes]
strings = ['{0}'.format(str(node.squad)) for node in allSquadNodes]
strings.sort()
#for string in strings:
#    print(string)

#file = open('tree.txt', 'w', encoding='utf-8')
#for pre, fill, node in RenderTree(baseNode):
#    #print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
#    file.write('{0}{1} - {2}g\n'.format(pre, node.name, node.gold))
#    pass

#file.close()


print('\n{0} final nodes'.format(len(allSquadNodes)))

unique = list(set(strings))
unique.sort()
print('\n{0} unique squads'.format(len(unique)))

#file = open('squads.txt', 'w', encoding='utf-8')
#for squad in unique:
#    #print('{0}{1} - {2}g'.format(pre, node.name, node.gold))
#    file.write('{0}\n'.format(squad))
#    pass

#file.close()

#print(temp)
#print(len(temp))

exit()
