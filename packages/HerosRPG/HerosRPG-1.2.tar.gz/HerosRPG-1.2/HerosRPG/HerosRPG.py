import sys
import os
import pickle
sys.path.append('../')
from herosrpg.Hero import Hero
from herosrpg.statemachine.RPGController import RPGController


## FUNCTIONS ###

def display_title_bar():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\t**********************************************")
    print("\t***  -=- Simple Battle Adventure v1.0 -=-  ***")
    print("\t**********************************************")
    print("")


def get_user_choice():
    print("\nL = Look Around, A = Attack, Q = Quit")
    return input("Score [" + str(hero.iCurrentScore) + "] Level [" + str(hero.iCurrentLevel) + "] Action [L,A,Q]: ")

def quit():
    try:
        file_object = open('hero.pydata', 'wb')
        pickle.dump(hero, file_object)
        file_object.close()
        print("\nThanks for playing. I will remember you Hero.")
    except Exception as e:
        print("\nThanks for playing. I won't be able to remember you Hero.")
        print(e)

def load_hero():
    try:
        if os.path.isfile('hero.pydata'):
            file_object = open('hero.pydata', 'rb')
            hero = pickle.load(file_object)
            file_object.close()
        else:
            hero = Hero()
        return hero
    except Exception as e:
        print(e)
        return []


### MAIN PROGRAM ###
hero = load_hero()

rpgController = RPGController()
rpgController.SetLevel(hero.iCurrentLevel)

iMaxLevel = 10
choice = ''

display_title_bar()

print("\nWelcome Hero. Adventure Awaits.")

while True:
    choice = get_user_choice()

    display_title_bar()

    if choice == "Q" or choice == "q" or rpgController.GetLevel() >= iMaxLevel:
        quit()
        break

    elif choice == "L" or choice == "l":
        points = rpgController.Explore()
        if points > 0:
            print("You gain " + str(points) + " heroic points!")
            hero.iCurrentScore += points

    elif choice == "A" or choice == "a":
        rounds = rpgController.Battle()

        if rounds > 0:
            points = 10 - rounds

            if points < 0:
                points = 0

            hero.iCurrentScore += points

            print("You gain " + str(points) + " heroic points!")

    else:
        print("Invalid Entry!")

    if hero.iCurrentScore >= hero.iNextLevel:
        rpgController.SetLevel(rpgController.GetLevel() + 1)
        hero.iNextLevel = rpgController.GetLevel() * 10
        hero.iCurrentLevel = rpgController.GetLevel()

        print("Your wonderous experience has gained you a level! Level " + str(hero.iCurrentLevel))

if rpgController.GetLevel() >= iMaxLevel:
    print("")
    print("You WIN! Final score [" + str(hero.iCurrentScore) + "]")
