#!/usr/bin/python3
"""Driving a simple game framework with
   a dictionary object | Alta3 Research"""

# Replace RPG starter project with this code when new instructions are live


from random import randint


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
    if "item" in rooms[currentRoom]:
        item = rooms[currentRoom]['item']
        # check if the item is a list (multiple)
        if type(item) == list:
            itemList = item
            # print on same line as the items
            print("You see a few items:", end=" ")
            for i in itemList:
                # add 'and' between the items for readability
                it = " and ".join(itemList)
            print(it)
            # THIS WORKS BUT WHERE????????
            if currentRoom == "Kitchen":
                #     # if monster is there - option to fight
                if "monster" in rooms[currentRoom]['item']:
                    fightOption()
        else:
            print('You see a ' + rooms[currentRoom]['item'])
    print("---------------------------")


def fightOption():
    print("The Monster is coming!")
    fight_or_flee = input(
        "Choose '1' to fight for cash or 'go north' to run out the room!")
    if fight_or_flee == "1":
        fightMonster()
    # elif fight_or_flee == "go north":
    #     move = fight_or_flee
    # else:
    #     print(
    #         f"You took too long and got bitten your health is now {currentHealth}!!")


def fightMonster():
    print('''
    RPG Game
 Slay The Monster!!!
    ========
    Commands:
      punch 
      kick 
    ''')

    # start player with 100 health
    currentHealth = 100
    cpuHealth = 100
    fight_move = ''
    while currentHealth != 0 and cpuHealth != 0 and fight_move == '':
        fight_move = input('>')
        if fight_move == 'punch':
            event = randint(1, 20)
            if (event % 2 == 0):
                currentHealth -= 20
                fight_move = ''
                print("User:", currentHealth)
            else:
                cpuHealth -= 20
                fight_move = ''
                print("cpu:", cpuHealth)

        if fight_move == 'kick':
            eventKick = randint(1, 20)
            if (eventKick % 2 != 0):
                currentHealth -= 10
                fight_move = ''
                print("User:", currentHealth)
            else:
                cpuHealth -= 10
                fight_move = ''
                print("cpu:", cpuHealth)


# an inventory, which is initially empty
inventory = []

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
        'north': 'Dining Room'
    }
}
# start the player in the Hall
currentRoom = 'Hall'


showInstructions()

# loop forever
while True:
    showStatus()

# THIS WORKS BUT WHERE????????
    # if currentRoom == "Kitchen":
    #     # if monster is there - option to fight
    #     if "monster" in rooms[currentRoom]['item']:
    #         fightOption()

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
    if move[0] == 'get':
        # if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
            # add the item to their inventory
            inventory += [move[1]]
            # display a helpful message
            print(move[1] + ' got!')
            # delete the item from the room
            del rooms[currentRoom]['item']
        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            print('Can\'t get ' + move[1] + '!')


# MAYBE NOT NEEDED
    # # if user move is 2 AND monster is in that room, exit
    # if move[0] == '2' and "monster" in rooms[currentRoom]['item']:
    #     now_move = 'north'
    #     currentRoom = rooms[currentRoom][now_move]


# TODO
# add description of items with print
# potion leads to api call to grab random gun then a prompt for a 2nd but it costs
# 2nd battle at garden?
# choose moves of punch or kick for combat with monster, also theres $ in the room
# make 2 items(add cash) in a room by changing it to a list --- **DONE**
# check either by size or using 'in' that inventory has it AND the user is in garden to open a chess with key and WIN game
