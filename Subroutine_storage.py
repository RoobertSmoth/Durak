#Subroutine_storage

from tkinter import *
from Durak_cards import *
from queue import PriorityQueue
import time

def playtrue(player):
    player.play = True

#----------------------------------------------Subroutines about visuals

#Make into a photo - seen cards
def clearFrame(playerframe):
    # destroy all widgets from frame
    
    for widget in playerframe.winfo_children():
        widget.destroy()

def render_card(card, player):

    #Must be global in order for pictures to show
    global cardbase

    cardbase = PhotoImage(file = f"Durak\Durak_Images\Dcards\{card}.png") #Create card image
    cardbase = cardbase.subsample(8) #Size down image
    player.imagestoreref.append(cardbase) #Stores imageref so they are constantly referenced

    return cardbase #Returns the card to be outputted

#make into photo - hidden cards for opponents

def render_card_hidden(card, player):

    #Must be global in order for pictures to show
    global cardbase
    
    cardbase = PhotoImage(file = f"Durak\Durak_Images\Dcards\cardbackblue.png") #Creates cardback image
    cardbase = cardbase.subsample(8) #Downsizes image
    player.imagestoreref.append(cardbase) #Stores reference in imagestoreref to display constantly

    return cardbase #Returns card to be outputted


#Displays hidden cards as labels-----------------
        
def botdisplayaslabel(player,frame,counter):

    cardimage = render_card_hidden(player.cardstringstorage[counter], player) #Creates a displayable image
    cards = Label(frame, image = cardimage) #Label so that the player cannot click on it
 

    #Stacking:
    if counter%2 == 0:
        cards.grid(row=0, column=counter, pady=0, ipadx=0)
    else:
        cards.grid(row=1, column=counter-1, pady=0, ipadx=0)


def dealerdisplay(dealer,counter,cardtype):
    if cardtype == "attack":
        dealer.currentframecontents.append(dealer.attackcard) #Used when picking up
        dealer.currentattack.append(dealer.attackcard)
        cardimage = render_card(dealer.attackcard, dealer) #Creates a displayable image
        cards = Label(dealer.attackframe, image = cardimage) #Label so that the player cannot click on it
        if len(dealer.imagestorerefattack) > 0:
            counter = len(dealer.imagestorerefattack)
        
        cards.grid(row=0, column=counter, pady=0, ipadx=0)
        dealer.imagestorerefattack.append(cards)

    elif cardtype == "defend":
        dealer.currentframecontents.append(dealer.defendcard) #Used when picking up
        dealer.currentdefend.append(dealer.defendcard)
        cardimage = render_card(dealer.defendcard, dealer) #Creates a displayable image
        cards = Label(dealer.defendframe, image = cardimage) #Label so that the player cannot click on it
        if len(dealer.imagestorerefdefend) > 0:
            counter = len(dealer.imagestorerefdefend) #Places next to the occupied space

        cards.grid(row=1, column=counter, pady=0, ipadx=0)
        dealer.imagestorerefdefend.append(cards)
    else:
        print("Cardtype not stated error")
    
    if len(dealer.currentdefend) < len(dealer.currentattack) and len(dealer.currentdefend) != 0:
        cardbase = PhotoImage(file = f"Durak\Durak_Images\Dcards\cardbackblue.png") #Create card image
        cardbase = cardbase.subsample(8) #Size down image
        placeholdercard = Label(dealer.defendframe, image = cardbase)
        if len(dealer.imagestorerefdefend) > 0:
            counter = len(dealer.imagestorerefdefend) #Places next to the occupied space
        placeholdercard.grid(row=1, column=counter, pady=0, ipadx=0)
        amount = len(dealer.currentdefend)
        while amount < len(dealer.currentattack):
            placeholdercard.grid(row=1, column=amount, pady=0, ipadx=0)
            amount += 1

        cards = None
    

#displays the trump card on screen

def trump_display(deck,frame):

    global tcardimagevisual, tcards #t for trump, must be public for cards to show

    #Make trump card into readable string
    trumpcardstring = (deck.trumphand[0].value + deck.trumphand[0].suit)

    #render the card
    tcardimagevisual = PhotoImage(file = f"Durak\Durak_Images\Dcards\{trumpcardstring}.png") #Create image
    tcardimagevisual = tcardimagevisual.subsample(8) #Sizes the card down

    tcards = Label(frame, image = tcardimagevisual) #Label as it wont be pressed on
    tcards.pack()

#Make object into readable string            

def cardstring(player, counter):
    card = player.hand[counter]
    card = (card.value + card.suit) #Turns card object to string
    return card

def card_smaller(card):
    card = card.subsize(10)
    return card

def card_bigger(card):
    card = card.subsize(8)
    return card

def configure_colour(player, frame):

    if player.attack == True:
        frame.configure(background = "orangered1") #Red for attacker

    elif player.defend == True:
        frame.configure(background = "olivedrab3") #Green for defender
    else:
        frame.configure(background = "white") #White for bystander/secondary attacker

#----------------------------------------------Subroutines about gameplay


def round_transition(Player1, Player2, Player3, Player4, attacker, defender):
    winners = []

    #Finds who is still in
    playercycle(Player1,Player2,Player3,Player4) #Resets playercycle
    player_array = [Player1,Player2,Player3,Player4]
    for player in player_array:
        if attacker.name == player.name and defender.pickedup != False: #If the defender succeeded, they become the attacker.

            #Reset attacker back to a normal player
            attacker.attack = False
            attacker.play = False

            #Find new attacker
            attackerindex = player_array.index(player)
            if attackerindex == len(player_array):
                attacker = player_array[0]
            else:
                attacker = player_array[attackerindex+1]

            #Reset defender to a normal player
            defender.defend = False
            defender.play = False

            #Find new defender

            defenderindex = player_array.index(defender)
            if attackerindex == len(player_array):
                attacker = player_array[0]
            else:
                attacker = player_array[attackerindex+1]


        if player.win == True:
            player_array.pop(player_array.index(player))
        else:
            winners.append(player)
    

    

def returncardobjectattack(player):
    if player.attack == True:
        for i in range(0,len(player.cardstringstorage)):
            if Durak_Dealer.attackcard == player.cardstringstorage[i]:
                return player.hand[i]
    else:
        print("Error, no one is attacking")
    
    

#Cards must always be six if the deck is not empty

def six_cards(player, deck):

    if len(deck.cards) == 0: #if deck is empty
        print("Not enough cards") #Six cards cannot operate

    else:    #If deck isnt empty
        while len(player.hand) <= 5: #While player has 5 or less cards, draw.
            player.draw(deck)


#Finds the highest value of trumps out of the four players

def firstturn(val1, val2, val3, val4): #1-4 symbolising player 1-4
    valuearray = [val1, val2, val3, val4] #Into array

    #Let the first value be the highest for now
    Highestval = val1

    #Searches through array to find highest
    for value in valuearray:
        if Highestval < value:
            Highestval = value

    return Highestval 


def playercycle(player1, player2, player3, player4):
    global turn_cycle
    turn_cycle = [] #Each time subroutine is called, it will rewrite the turn cycle
    

    if player1.win == False:
        turn_cycle.append(player1.name)

    if player2.win == False:
        turn_cycle.append(player2.name)

    if player3.win == False:
        turn_cycle.append(player3.name)

    if player4.win == False and player4.name not in turn_cycle:
        turn_cycle.append(player4.name)
        
    print(turn_cycle)

def find_defender(attackingplayer, player1, player2, player3, player4):
    
    position = turn_cycle.index(attackingplayer.name)#Finds the position of the player in turn_cycle

    if position == (len(turn_cycle)-1): #Player 4 attacks, player 1 defends
        defender = turn_cycle[0]
    else:
        defender = turn_cycle[position+1] #Whoever is next to attacker defends
    
    if player1.name == defender: #If defender name matches player, player.defend is true
        player1.defend = True
        return player1
    
    if player2.name == defender:
        player2.defend = True
        return player2

    if player3.name == defender:
        player3.defend = True
        return player3
    
    if player4.name == defender:
        player4.defend = True
        return player4
    
def find_player(Player1, Player2, Player3, Player4, name):
    if name == Player1.name:
        return Player1
    elif name == Player2.name:
        return Player2
    elif name == Player3.name:
        return Player3
    elif name == Player4.name:
        return Player4
    else:
        print(name,"doesnt exist.")


def find_attacker(defendingplayer, player1, player2, player3, player4):
    
    position = turn_cycle.index(defendingplayer.name)#Finds the position of the player in turn_cycle

    if position == 0: #Player 1 defends, player 4 attacks
        attacker = turn_cycle[len(turn_cycle)-1]

    else:
        attacker = turn_cycle[position-1] #Whoever is behind defender attacks
    
    if player1.name == attacker: #If attacker name matches player, player.attack is true
        player1.attack = True
        return player1
    
    if player2.name == attacker:
        player2.attack = True
        return player2

    if player3.name == attacker:
        player3.attack = True
        return player3
    
    if player4.name == attacker:
        player4.attack = True
        return player4

def find_best_attack_option(player, deck):
    best_option_value = 15 #Higher value so it can get smaller
    best_option_string = "" #Resets the best card each time

    for cardindex in range(0, len(player.hand)):
        stringstoragecard = player.cardstringstorage[cardindex] #Find string of card

        if deck.trumpsuit not in stringstoragecard: #Best cards are lowest cards so no trumps
            suit = player.hand[cardindex].suit
            if best_option_value > Valuedictionary[stringstoragecard[0:-len(suit)]]:
                best_option_value = Valuedictionary[stringstoragecard[0:-len(suit)]]
                best_option_string = player.cardstringstorage[cardindex]
    
    return best_option_string

def find_best_defend_option(player, deck, attackcard):
    attack_value, attack_suit = player.findcardvalue(attackcard) #For comparisons
    best_option_value = 0 #Higher value so it can get smaller
    best_option_string = "" #Resets the best card each time
    comparison_value = 16 #Starts highest

    for cardindex in range(0, len(player.hand)):
        stringstoragecard = player.cardstringstorage[cardindex] #Find string of card
        best_option_value, best_option_suit = player.findcardvalue(stringstoragecard)
        if (best_option_value > attack_value and best_option_suit == attack_suit) or (best_option_suit == deck.trumpsuit and (attack_suit != deck.trumpsuit and best_option_value > attack_value)):
            if best_option_value > attack_value and best_option_value < comparison_value: #Try to find the smallest attack card
    
                best_option_string = player.cardstringstorage[cardindex]
        
        comparison_value = best_option_value
    
    player.bestoption = best_option_string
    if player.bestoption == "":
        return False
    else:
        return best_option_string
    




    
    
    


    






