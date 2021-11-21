from math import comb
from os import system, terminal_size
from os import name as sysname
from random import random as roll
from time import sleep

# define our clear function
def clear():
  
    # for windows
    if sysname == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

#define fighter
class fighter:
    def __init__(self, pName:str, pMaxHp:int, pHp:int, pDmg:int, pSpd:int, pRange:int, pAcc:float, pTeam2:bool, pStun = 0, pSDur = 1) -> None:
        self.name = pName
        self.maxHp = pMaxHp
        self.currentHp = pHp
        self.Dmg = pDmg
        self.Range = pRange
        self.Spd = pSpd
        self.Acc = pAcc
        self.team1 = pTeam2
        self.location = 0
        self.stunned = 0
        self.stun = pStun
        self.SDur = pSDur
        #refers location on battle field
    
    def is_alive(self):
        return self.currentHp > 0
    
    def attack(self, enemy:object)->object:
        
        print(self.name + " attacks " + enemy.name + "!")
        if roll() < self.Acc:
            enemy.currentHp -= self.Dmg
            print("Hit for ", self.Dmg, "!")
            if self.stun != 0:
                if roll() < self.stun:
                    enemy.stunned = self.SDur
                    print("and they were stunned for " + str(self.SDur) + " turns!")
                else: 
                    print("but did not stun")

        else:
            print("but missed.")
        return enemy
    
    def move(self, tLocation):
        ii = 0
        if self.team1 == True:
            for ii in range(self.Spd):
                if self.location + self.Range != tLocation:
                    self.location += 1
                else:
                    break
            print(self.name +" moved " + str(ii+1) + " spaces forward")
        else:
            for ii in range(self.Spd):
                if self.location - self.Range != tLocation:
                    self.location -= 1
                else:
                    break
            print(self.name +" moved " + str(ii+1) + " spaces forward")
                
    #this code decides what the fighter will do and who it will attack.
    def act(self, arena)->list:
        opponents = []
        
        try:
            if self.is_alive() == True:    
                if self.stunned > 0:
                    self.stunned -= 1
                    if self.stunned > 0:
                        print(self.name + " is stunned for " + str(self.stunned) + " more turns")
                    else:
                        print(self.name + " was stunned and could not act")                    

                    return(arena)
                
                else:
                    #gets all fighters
                    index = 0
                    
                    for combatatent in arena:
                        #gets all alive fighters
                        if combatatent.is_alive():
                            #gets all alive enemy fighters
                            if combatatent.team1 != self.team1:
                                #creates a list containing alive enemy fighters location and their index
                                opponents.append([combatatent.location, index, combatatent])
                        index += 1
                    #sorts the list
                    #if the actor is in team 1 sorts ascending location
                    if self.team1 == True:
                        opponents.sort(reverse=False)
                    #if actor is in team 2 sorts descending location
                    else:
                        opponents.sort(reverse=True)
                    #sets the target to the closest alive enemey fighter
                    
                    target = opponents[0]

                    #finds the distance between actor and target
                    diffrence = abs(self.location - target[0])

                    #if target out of range move forward
                    
                    if diffrence > self.Range:
                        self.move(target[0])
                    #else attack
                    else:
                        #replaces target with new damaged version of target
                        arena[target[1]] = self.attack(arena[target[1]])
                    
                    return(arena)
            else:
                return(arena)
        except:
            pass

#function gets total team health  for display and when to end fight
def getTeamHp(arena:list, team:bool)->int:
    teamHp = 0
    for combatant in arena:
        if combatant.team1 == team:
            teamHp += combatant.currentHp
    return teamHp

def getTeamMaxHp(arena:list, team:bool)->int:
    teamMaxHp = 0
    for combatant in arena:
        if combatant.team1 == team:
            teamMaxHp += combatant.maxHp
    return teamMaxHp
        
def printScreen(arena:list, distance:int):
    T1Num = (round(getTeamHp(arena,True)/getTeamMaxHp(arena,True)*10))
    T2Num = (round(getTeamHp(arena,False)/getTeamMaxHp(arena,False)*10))
    T1Hpbar = "["+ str("#"*T1Num) + " "*(10-(T1Num)) + "]"
    T2Hpbar = "["+ str("#"*T2Num) + " "*(10-(T2Num)) + "]"
    
    amap = [ [] for _ in range(distance+1) ]
    for fighter in arena:
        if fighter.is_alive():
            initial = fighter.name[0]
        else:
            initial = "x"
        amap[fighter.location].append(initial)

    ii = 0
    for x in amap:
        if x == []:
            amap[ii] = "_"
        ii += 1

    boarder = "="*(distance+10) +"\n"
    display = boarder
    display += "Heros: "+ str(getTeamHp(arena,True)) + " "*(distance-14) + " " + "Villians: " + str(getTeamHp(arena,False)) +"\n"
    display += T1Hpbar + " "*(distance-17) + T2Hpbar +"\n"
    display += str(''.join(map(str, amap))).replace(",","").replace("'","")
    print(display)

def fight(fighters, distance=20):
    clear()
    fighters
    fighters.sort(key=lambda x: x.Spd, reverse=True)
    #puts team 2 on other side of arena
    for fighter in fighters:
        if fighter.team1 == False:
            fighter.location = distance

    team1Hp = getTeamHp(fighters, True)
    team2Hp = getTeamHp(fighters, False)
    while team1Hp > 0 and team2Hp > 0:
        for combatant in fighters:
            clear()
            printScreen(fighters, distance)
            arena = combatant.act(fighters)
            team1Hp = getTeamHp(fighters, True)
            team2Hp = getTeamHp(fighters, False)
            if combatant.currentHp > 0:
                sleep(0.5)
    
    clear()        
    printScreen(fighters, distance)
    if team1Hp > team2Hp:
        print("The heros have defeated the villians!")
    if team2Hp > team1Hp:
        print("Oh no! the heros have fallen") 
    
#====================================================================
#change any variables to test
#even add new fighters
            #Name   #max #H #D #S #R #ACC #Team #Stun #SDur
a = fighter("Jim",   10, 10, 5, 3, 1,  0.75, True)
b = fighter("Troll", 40, 40, 8, 2, 1,  0.5, False, 0.5, 1)
c = fighter("Sarah", 20, 20, 2, 1, 5, 0.6,  True)
e = fighter("Goblin", 10, 10, 5, 5, 0,  0.7,   False)

#don't forget to add new fighters
fighters = [a,b,c,e]
                #size of battlefield
end = input()
while end != "x":
    fight(fighters, 20)
    end = input()