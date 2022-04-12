#!/usr/bin/python3
"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

# Replace RPG starter project with this code when new instructions are live

import requests
from random import randint

API_URL = 'https://zenquotes.io/api/random/'


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
            print('You see a ', rooms[currentRoom]['item'])
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
    print("Defeat the giant so you can get the heck home!")
    fightMonster()


def giantChase():
    print("TODO if use key in another room")


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
    item = rooms[currentRoom]['item'][0]
    # start player with 100 health
    currentHealth = 100
    cpuHealth = 100
    cpu = cpuHealth
    user = currentHealth

    if 'gun' in inventory:
        bullets = 12
        print('Use your gun for more damage!')

    fight_move = ''
    isFighting = True
    while user > 0 and cpu > 0 and fight_move == '' and isFighting == True:
        fight_move = input('>')
        if fight_move == 'punch' and cpu > 0 and user > 0:
            event = randint(1, 20)
            if (event % 2 == 0):
                user -= 10
                fight_move = ''
                print("User:", user)
            else:
                cpu -= 25
                fight_move = ''
                print("cpu:", cpu)

        elif fight_move == 'kick' and cpu > 0 and user > 0:
            eventKick = randint(1, 20)
            if (eventKick % 2 != 0):
                currentHealth -= 10
                fight_move = ''
                print("User:", user)
            else:
                cpuHealth -= 25
                fight_move = ''
                print("cpu:", cpu)

        elif (fight_move == 'shoot' and 'gun' in inventory) and user > 0 and cpu > 0:
            eventShoot = randint(1, 20)
            if (eventShoot < 4):
                print("Bad aim you missed!")
                bullets -= 1
                fight_move = ''
            else:
                cpu -= 45
                print(
                    f"Bullseye! The {item}\'s health dropped to {user}. {bullets} bullets left!")
                fight_move = ''
        elif fight_move == 'shoot' and 'gun' not in inventory:
            print("You don't have a gun son!")
            fight_move = ''

    # if cpu character's health is zero
    if cpu <= 0:
        print("Monster Defeated! You can now get the cash!")
        # remove the monster/giant from room
        del rooms[currentRoom]['item'][0]
        # end fight mode
        isFighting = False
        return None

    if user <= 0:
        # Ascii art link
        print("Game Over")
        lives -= 1
        isFighting = False
        return None


# an inventory, which is initially empty
inventory = ['gun']

# boolean for fight mode
isFighting = False

# lives
lives = 2


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
while True and lives > 0:

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

            if move[1] == 'treasure chest' and 'treasure chest' in inventory:
                use_key = input("Use the Key!! ").strip().lower()
                if use_key == 'use key' and 'key' in inventory:
                    inventory.pop(-1)
                    # replace 'cash' as $50k for user to see amount
                    inventory += ['50kg of gold and silver']
                    showStatus()
                    endFight()
                else:
                    print("You need a key")
            if move[1] == 'potion':
                print('Use the \'use potion\' command to see what\'s in store!')

        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            print('Can\'t get ' + move[1] + '!')

    # if the user chooses to get potion
    elif move[0] == 'use' and 'potion' in inventory:
        if move[1] == 'potion':
            # either API request from genie
            # add commentary for genie
            resp = requests.get(API_URL).json()
            quote = resp[0]['q']
            # use cash here somehow for weapons
            # remove it from inventory
            # weapon for monster? if use randomly someone comes?
            print(quote)

    # if user uses the key in the garden
    elif move[0] == 'use' and move[1] == 'key' and 'treasure chest' in inventory:
        print("TODO2")
        use_key = input("Use the Key!! ").strip().lower()
        if use_key == 'use key' and 'key' in inventory:
            # inventory.pop(-1)  remove index of chest
            # replace 'cash' as $50k for user to see amount
            inventory += ['50kg of gold and silver']
            showStatus()
            giantChase()

        # another monster comes to fight for rest of cash and the treasure
        # gun takes more health down of monster
        # end the game and print ascii art here IF inventory has all things
        # need the rest of the cash to get home
        # remove item short words po ke etc

    else:
        print("Invalid command")
        move = ''
