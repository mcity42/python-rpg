#!/usr/bin/python3
"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

# Replace RPG starter project with this code when new instructions are live
import sys
import requests
from random import randint

API_URL = 'https://zenquotes.io/api/random/'

isPlay = True


def showInstructions():
    """Show the game instructions when called"""
    # print a main menu and the commands
    print('''
    RPG Game
    ========
    Commands:
      go [direction]
      get [item]
    ''')


def showStatus():
    """determine the current status of the player"""
    # print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    # print the current inventory
    print('Inventory : ' + str(inventory))
    # if there is an item(s)
    if "item" in rooms[currentRoom] and rooms[currentRoom]['item'] != []:
        item = rooms[currentRoom]['item']
        # check if the item is a list (multiple)
        if type(item) == list and item != []:
            itemList = item
            # print on same line as the items
            print("You see a few items:", end=" ")
            for i in item:
                # add 'and' between the items for readability
                it = " and ".join(itemList)
            print(it)
            checkForMonsters()
        else:
            print('You see a', rooms[currentRoom]['item'])
    endGame()
    print("---------------------------")


def checkForMonsters():
    if (currentRoom == "Kitchen" or currentRoom == "Garden"):
        if ("monster" in rooms[currentRoom]['item']) or ("giant" in rooms[currentRoom]['item']):
            #         # if monster is there - option to fight
            if isFighting == False and "monster" in rooms[currentRoom]['item']:
                fightOption()
                fightMonster()
        elif "giant" in rooms[currentRoom]['item'] and '50kg of gold and silver' in inventory:
            fightOption()
            endFight()


def fightOption():
    print("He's coming! Defeat him!!")


def endFight():
    print("An angry giant has been looking for this treasure!\nLuckily for you you're only 5 ft 7 and was able to search underneath the tractor!\n")
    print('Haha! You also found 4 bullets out on the seat!!')
    print("Defeat the giant so you can get the heck home!")
    fightMonster()


def giantChase():
    print('Look behind you he\'s coming in!')
    endFight()


def fightMonster():
    print('''
    RPG Game
Kill Your Attacker!!!
    ========
    Commands:
      punch 
      kick 
      shoot
    ''')
    if currentRoom == 'Kitchen':
        item = rooms[currentRoom]['item'][0]
    else:
        item = 'giant'
    # start player with 100 health
    user = 100
    cpu = 100

    bullets = 4
    if 'gun' in inventory and bullets > 0:
        print('Use your gun for more damage!')

    fight_move = ''
    isFighting = True
    while user > 0 and cpu > 0 and fight_move == '' and isFighting == True:
        fight_move = input('>')
        if fight_move == 'punch' and cpu > 0 and user > 0:
            event = randint(1, 20)
            if (event % 2 == 0):
                user -= 20
                fight_move = ''
                print("User:", user)
            else:
                print('Sick jab!')
                cpu -= 15
                fight_move = ''
                print(f"{item}\'s health:", cpu)
        elif fight_move == 'kick' and cpu > 0 and user > 0:
            eventKick = randint(1, 20)
            if (eventKick % 2 != 0):
                user -= 25
                fight_move = ''
                print('Almost! He caught you slipping!')
                print("User:", user)
            else:
                print('What a kick!')
                cpu -= 15
                fight_move = ''
                print(f"{item}\'s health:", cpu)

        elif (fight_move == 'shoot' and bullets > 0) and user > 0 and cpu > 0:
            eventShoot = randint(1, 20)
            if (eventShoot < 8):
                bullets -= 1
                print(f"Bad aim you missed! {bullets} bullets left!")
                fight_move = ''
            else:
                cpu -= 25
                bullets -= 1
                print(
                    f"Bullseye! The {item}\'s health dropped to {cpu}. {bullets} bullets left!")
                fight_move = ''
        elif fight_move == 'shoot' and bullets <= 0:
            print("You got nothing to shoot son! -5 health!")
            user -= 5
            fight_move = ''
        elif fight_move not in ['shoot', 'punch', 'kick']:
            user -= 20
            print('False moves will cost you! You\'ve been bitten')
            print('Your health is', user)
            fight_move = ''

    # if cpu character's health is zero
    if cpu <= 0:
        print(f"{item} defeated! Go get the cash!")
        # remove the monster/giant from room
        if item == 'giant':
            del rooms['Garden']['item'][0]
        else:
            del rooms[currentRoom]['item'][0]
        # end fight mode
        isFighting = False
        endGame()
        return None

    if user <= 0:
        print("Game Over. Try Again!")
        print('-----------------------')
        sys.exit()


def endGame():
    if ['key', '50kg of gold and silver', '$50,000', 'potion'] in inventory:
        print("Congrats!! You won the game!!!")
        sys.exit()


# an inventory, which is initially empty
inventory = ['gun']

# boolean for fight mode
isFighting = False


# a dictionary linking a room to other rooms
rooms = {

    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': 'key'
    },

    'Kitchen': {
        'north': 'Hall',
        'item': ['monster', 'cash'],
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'item': 'potion'
    },
    'Garden': {
        'north': 'Dining Room',
        'item': ['giant', 'treasure chest']
    }
}
# start the player in the Hall
currentRoom = 'Hall'

showInstructions()

# loop forever
while isPlay == True:

    if len(inventory) >= 5 and '50kg of gold and silver' in inventory:
        break

    showStatus()
    # get the player's next 'move'
    # .split() breaks it up into an list array
    # eg typing 'go east' would give the list:
    # ['go','east']
    move = ''
    while move == '':
        move = input('>')

    # split allows an items to have a space on them
    # get golden key is returned ["get", "golden key"]
        move = move.lower().split(" ", 1)

    # if they type 'go' first
    if move[0] == 'go':
        # check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            # set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
        # there is no door (link) to the new room
        else:
            print('You can\'t go that way!')

    # if they type 'get' first
    elif move[0] == 'get':
        # if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and move[1] != "giant" and move[1] != "monster":
            # add the item to their inventory
            inventory += [move[1]]
            # display a helpful message
            print(move[1] + ' got!')
            # delete the item from the room
            if (type(rooms[currentRoom]['item']) == str):
                del rooms[currentRoom]['item']
            elif(type(rooms[currentRoom]['item']) == list):
                index = rooms[currentRoom]['item'].index(move[1])
                del rooms[currentRoom]['item'][index]

            if move[1] == 'cash' and 'cash' in inventory:
                print("You just found $50,000! This should come in handy!")
                # replace 'cash' as $50k for user to see amount
                inventory.pop(-1)
                inventory += ['$50,000']
                endGame()

            if move[1] == 'treasure chest' and 'treasure chest' in inventory:
                use_key = input(
                    "Use the key [command--> 'use key']!!").lower()
                if use_key == 'use key' and 'treasure chest' in inventory:
                    inventory.pop(-1)
                    inventory += ['50kg of gold and silver']
                    print('Jackpot!!! The hidden gold was found!!')
                    showStatus()
                    giantChase()
                    endGame()

            if move[1] == 'potion':
                print('Use the \'use potion\' command to see what\'s in store!')

        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            print('Can\'t get ' + move[1] + '!')

    # if the user chooses to get potion and use it, magic genie appears
    # the quote given from genie is from the API get request
    elif move[0] == 'use' and 'potion' in inventory:
        if move[1] == 'potion' and isFighting == False:
            print('KABOWWW a blue magic genie just appeared in the room!')
            print('Use potion anytime you need some quick wisdom!')
            resp = requests.get(API_URL).json()
            quote = resp[0]['q']
            print("Genie:", end=' ')
            print(quote)
        elif isFighting == True:
            print("No time for that right now!")
    # if user uses the key in the garden
    elif move[0] == 'use' and move[1] == 'key' and 'treasure chest' in inventory:
        index = inventory.index('treasure chest')
        inventory.pop(index)
        inventory += ['50kg of gold and silver']
        print('Jackpot!!! The hidden gold was found!!')
        showStatus()
        giantChase()
        endGame()
    elif move[0] == 'use' and move[1] == 'key' and 'treasure chest' not in inventory:
        print("You need a key")

    else:
        print("Invalid command")
        move = ''
