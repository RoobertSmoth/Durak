#Main code

from tkinter import *
import random
from Durak_cards import *
from Subroutine_storage import *
import time 


root = Tk()

#------------------------------------------------------------

#Set up window

root.geometry("2000x1500") #Sets window dimensions
root.attributes('-fullscreen', True) #Opens in fullscreen

durak_icon = PhotoImage(file = r"Durak\Durak_Images\durakfirebird.png") #Create bird picture
root.iconphoto(True, durak_icon) #Sets the icon to the bird
root.title("Durak") #Names the window "Durak"

background = PhotoImage(file = r"Durak\Durak_Images\russianlandscape.png") #Create landscape picture
Backgroundimg = Label(root, image = background) #Set background as landscape
Backgroundimg.place(x = 0, y = 0) #Place in the middle of the window

#Fullscreen exit - double esc button

def exit(event):
    if root.attributes('-fullscreen') == False: #If user presses esc twice they can quit whole program
        root.destroy()
    else:
        root.attributes('-fullscreen', False) #If user presses esc once they exit fullscreen
root.bind('<Escape>', exit )

#Set up deck and players

Round_deck = Deck() #Instantiate class as deck

#-------------------------------------------------------------------------

def findplayerframe(player):
    if player == Player1:
        return player1_frame
    elif player == Player2:
        return player2_frame
    elif player == Player3:
        return player3_frame
    elif player == Player4:
        return player4_frame
    
def resetround(defender, attacker):

    try:
        pickup_button.destroy()
    except:
        print("No button to destroy")

    print("resetting round")
    player_array = [Player1, Player2, Player3, Player4] #Might need to change once players start winning
    for player in player_array:
        if player.win == True:
            pass
        else:
            for player in player_array:
                player.play = False
                player.defend = False
                player.attack = False
            defenderindex = player_array.index(defender)

            #Stops them from playing
            defender.play = False
            defender.defend = False
            attacker.play = False
            attacker.defend = False

            #Find new attackers/defenders

            if defender.pickedup == True:
                if defenderindex == (len(player_array) -1):
                    attacker = player_array[0]
                else:
                    attacker = player_array[defenderindex+1] #If the player picked up, it skips their go
            else:
                attacker = defender #The defender gets to attack now.

            attackerindex = player_array.index(attacker)

            if attackerindex == (len(player_array)-1):
                defender = player_array[0]
            else:
                defender = player_array[attackerindex + 1]

            print("new attacker",attacker.name)
            attacker.attack = True
            print("new defender", defender.name)
            defender.defend = True


            configure_colour(Player1, player1_frame)
            configure_colour(Player2, player2_frame)
            configure_colour(Player3, player3_frame)
            configure_colour(Player4, player4_frame)

            round()
    

            

def pickup(player, dealer):
    player.pickedup = True
    for card in dealer.currentframecontents: #First need to add cards to hand
        cardvalue, cardsuit = player.findcardvalue(card)
        cardvalue = card[0:-(len(cardsuit))]
        card = Card(cardsuit,cardvalue)
        player.hand.append(card)

    clearFrame(dealer.attackframe) #Clear the dealers frame
    clearFrame(dealer.defendframe)

    dealer.currentframecontents.clear()
    player.cardstringstorage.clear()
    player.imagestoreref.clear()

    for i in range(0, len(player.hand)): #Rerenders the cards
            player.cardstringstorage.append(cardstring(Player1, i))
            displayasbutton(player,player.frame,i)

    player.play = False
    pickup_button.destroy()
    attacker = find_attacker(Player1, Player1, Player2, Player3, Player4)
    resetround(player, attacker)

def createpickupbutton(player, buttonframe, dealer):

    pickup_button = Button(buttonframe, text="Pick up", command = lambda: pickup(player, dealer))
    pickup_button.grid(row=1, column=1, padx=20, pady=20, ipadx=20)

    
    return pickup_button


def defender_true():
    #Set defender's play to TRUE so they can retaliate
        if Player1.defend == True:
            playtrue(Player1)
            return Player1
        elif Player2.defend == True:
            playtrue(Player2)
            return Player2
        elif Player3.defend == True:
            playtrue(Player3)
            return Player3
        elif Player4.defend == True:
            playtrue(Player4)
            return Player4
        else:
            print("Error: No one's defend is true.")

def play_check(playerframe, player, cardframename, card): #If the player clicks on the cards, it will automatically check if they can move
   
    if player.attack == True and player.play == True and len(Durak_Dealer.imagestorerefattack) < 6: #If when clicked and attack is true, the card will place itself in one of the free slots

        global pickup_button

        try:
            pickup_button.destroy()
        except:
            print("No button to destroy")
            
        #Maintenance
        Durak_Dealer.attackcard = "" #Resets the variable
        clearFrame(playerframe) #Clears all cards in the hand

        Durak_Dealer.attackcard = player.attack_action(card, cardframename, Durak_Dealer.attackframe) #Saves attacking card for reference
        Durak_Dealer.attackcardround.append(Durak_Dealer.attackcard)

        dealerdisplay(Durak_Dealer,0,"attack") #Displays the attacking card in playing area

        for i in range(0, len(player.cardstringstorage)): #Rerenders the cards
            displayasbutton(player,playerframe,i)


        for card in Durak_Dealer.attackcardround:
            Durak_Dealer.gamehistory.append(card) #Creates a log of game history

        defender = find_defender(Player1, Player1, Player2, Player3, Player4) #Finds defender, not assuming Player 2 is still in
        defender.play = True #defender can now move
        placeholdercounter = 0 #Will be changed in bot_playcheck
        defender.frame = findplayerframe(defender) #Cahnges the frame
        print("Bot to be playchecked =", defender.name)
      
        bot_playcheck(defender.frame, defender, defender.bestoption, defender.imagestoreref[placeholdercounter], None) 

        

    elif player.defend == True and player.play == True: #If when clicked and defend is true, the card will place itself to defend in one of the free slots
        #maintenance
        Durak_Dealer.defendcard = ""

        if Durak_Dealer.currentdefend != 0:
            wantedattackindex = len(Durak_Dealer.currentdefend)
        
        if Durak_Dealer.currentattack.index(Durak_Dealer.attackcard) != wantedattackindex:
            Durak_Dealer.attackcard = Durak_Dealer.currentattack[wantedattackindex]



        
        defendcard = player.defend_action(card, cardframename, Durak_Dealer.attackcard,Round_deck.trumpsuit)

        if card == defendcard:
    
            Durak_Dealer.defendcard = defendcard #Saves defending card
            Durak_Dealer.defendcardround.append(Durak_Dealer.defendcard)

            dealerdisplay(Durak_Dealer,0,"defend")
            clearFrame(playerframe) 

            for i in range(0, len(player.cardstringstorage)): #Rerenders the cards
                displayasbutton(player,playerframe,i)

            for card in Durak_Dealer.defendcardround:
                Durak_Dealer.gamehistory.append(card)

        attacker = find_attacker(player, Player1, Player2, Player3, Player4)
        attackagain, playablecards = attacker.attack_again(Durak_Dealer)

        if attackagain == True:
            print(attacker.name, "can attack with these cards:", playablecards) #Displays what they can play

            
            counter = random.randint(0,(len(playablecards)-1)) 

            attacker.bestoption = playablecards[counter]
            bestcardcounter = attacker.cardstringstorage.index(attacker.bestoption)
            if attacker == Player1:
                pass
            else:
                print("Bot to be playchecked =", attacker.name)
            
                bot_playcheck(attacker.frame, attacker, attacker.bestoption, attacker.imagestoreref[bestcardcounter], None)
                player.think()

        else:

            print(attacker.name, "cannot attack again")
            
            # Secondary attackers

            for player in [Player1, Player2, Player3, Player4]:
                defender = find_defender(attacker, Player1, Player2, Player3, Player4)
                if attacker != player and defender != player:
                    secondaryattacker = player
                    attackagain, playablecards = secondaryattacker.attack_again(Durak_Dealer)
                
                    if attackagain == True:
                        print("Secondary attacker", secondaryattacker.name, "can attack with these cards:", playablecards) #Displays what they can play


                        if len(playablecards) == 1:
                            counter = 0
                    
                        else:
                             counter = random.randint(0,len(playablecards)-1)

                        secondaryattacker.bestoption = playablecards[counter]
                     
                        bestcardcounter = secondaryattacker.cardstringstorage.index(secondaryattacker.bestoption)
                        secondaryattacker.play = False
                        secondaryattacker.attack = False
                        if len(Durak_Dealer.currentattack) <6:
                            secondaryattacker.play = True
                            secondaryattacker.attack = True
                            if secondaryattacker == Player1:
                                pass
                            else:
                                print("Bot to be playchecked =", secondaryattacker.name)
                               
                                bot_playcheck(secondaryattacker.frame, secondaryattacker, secondaryattacker.bestoption, secondaryattacker.imagestoreref[bestcardcounter], defender)
                        secondaryattacker.play = False
                        secondaryattacker.attack = False


                    else:
                        print(secondaryattacker.name,"cannot play either")

    



    else: #If when clicked and they cant move, will print out a message
        print("Not your go yet")

def bot_playcheck(playerframe, player,card, cardframename, defender):

    if player.attack == True and player.play == True and len(Durak_Dealer.imagestorerefattack) < 6: #If when clicked and attack is true, the card will place itself in one of the free slots
        #Maintenance
        Durak_Dealer.attackcard = ""#Resets the variable
        clearFrame(playerframe)
       
        Durak_Dealer.attackcard = player.attack_action_bot(card, player.cardstringstorage[player.cardstringstorage.index(player.bestoption)])#Saves attacking card

        Durak_Dealer.attackcardround.append(Durak_Dealer.attackcard) #Used to calculate if players can play again

        #The code below is the code for displaying in the middle
        dealerdisplay(Durak_Dealer,0,"attack") #Displays attacking card

        for i in range(0, len(player.cardstringstorage)): #Rerenders the cards
            botdisplayaslabel(player,playerframe,i)
        

        for card in Durak_Dealer.attackcardround: 
            Durak_Dealer.gamehistory.append(card) #Creates log of game history

        if defender == None:
            defender = find_defender(player, Player1, Player2, Player3, Player4) #Finds defender so they can respond
        
        defender.play = True
        if defender == Player1:

            global pickup_button
            pickup_button = createpickupbutton(defender, durak_frame, Durak_Dealer)
        else:
            
            bot_playcheck(defender.frame, defender,defender.bestoption, 0, defender)

        
    


    elif player.defend == True and player.play == True: #If when clicked and defend is true, the card will place itself to defend in one of the free slots

    
        #Maintenance
        Durak_Dealer.defendcard = ""
        
        find_best_defend_option(player, Round_deck, Durak_Dealer.attackcard)

        if player.bestoption == False or player.bestoption == "":
            print(player.name, "cannot play, they must pick up.")
        
            print(player.name,"is picking up...")
            player.pickup_bot(Durak_Dealer)
            clearFrame(Durak_Dealer.attackframe) #Clear the dealers frame
            clearFrame(Durak_Dealer.defendframe)

            for i in range(0, len(player.hand)): #Rerenders the cards
                player.cardstringstorage.append(cardstring(player, i))
                botdisplayaslabel(player,player.frame,i)



        else:
            bestcardcounter = player.cardstringstorage.index(player.bestoption)
            cardframename = player.imagestoreref[bestcardcounter]

            Durak_Dealer.defendcard = player.defend_action_bot(player.bestoption, cardframename, Durak_Dealer.attackcard,Round_deck.trumpsuit) #Saves defending card
            Durak_Dealer.defendcardround.append(Durak_Dealer.defendcard)
            dealerdisplay(Durak_Dealer,0,"defend")
            clearFrame(playerframe) 

            for i in range(0, len(player.cardstringstorage)): #Rerenders the cards
                botdisplayaslabel(player,playerframe,i)

            for card in Durak_Dealer.defendcardround:
                Durak_Dealer.gamehistory.append(card)
            
            player.play = False #Waits for their go again

            # Sends a message for attacker to attack again

            attacker = find_attacker(player, Player1, Player2, Player3, Player4)

            attackagain, playablecards = attacker.attack_again(Durak_Dealer) #Finds what cards they can attack with

            if attackagain == True:

                print(attacker.name, "can attack with these cards:", playablecards) #Displays what they can play

                if len(playablecards) == 1:
                    counter = 0
                    
                else:

                    counter = random.randint(0,len(playablecards)-1)
                    
                attacker.bestoption = playablecards[counter]
                bestcardcounter = attacker.cardstringstorage.index(attacker.bestoption)

                if attacker == Player1:
                    attacker.play = True
                else:
                    attacker.play = True
                    attacker.attack = True
                    bot_playcheck(attacker.frame, attacker, attacker.bestoption, attacker.imagestoreref[bestcardcounter], defender)

            else:
                print(attacker.name, "cannot attack again")
            

                
                # Secondary attackers

                for player in [Player1, Player2, Player3, Player4]:
                    defender = find_defender(attacker, Player1, Player2, Player3, Player4)
                    
                    if attacker != player and defender != player:
                        secondaryattacker = player
                        attackagain, playablecards = secondaryattacker.attack_again(Durak_Dealer)
                    
                        if attackagain == True:
                            print("Secondary attacker", secondaryattacker.name, "can attack with these cards:", playablecards) #Displays what they can play


                            if len(playablecards) == 1:
                                counter = 0
                        
                            else:
                                    counter = random.randint(0,len(playablecards)-1)

                            secondaryattacker.bestoption = playablecards[counter]
                    
                            bestcardcounter = secondaryattacker.cardstringstorage.index(secondaryattacker.bestoption)
                            secondaryattacker.play = False
                            secondaryattacker.attack = False
                            if len(Durak_Dealer.currentattack) <6:
                                secondaryattacker.play = True
                                secondaryattacker.attack = True
                                if secondaryattacker == Player1:
                                    pass
                                else:
                                    print("Bot to be playchecked =", secondaryattacker.name)
                                    bot_playcheck(secondaryattacker.frame, secondaryattacker, secondaryattacker.bestoption, secondaryattacker.imagestoreref[bestcardcounter], defender)
                            secondaryattacker.play = False
                            secondaryattacker.attack = False


                        else:
                            print(secondaryattacker.name,"cannot play either")

    else: #If when clicked and they cant move, will print out a message
        print("Bot error")

    # waitThreshold = random.randint(1,3)
    # botTimerWait = time.time()
    # while time.time() - botTimerWait <= waitThreshold:
    #     continue

    


#Displays user cards-------------------------

def displayasbutton(player,frame,counter):

    cardimage = render_card(player.cardstringstorage[counter], player) #Creates displayable image
    cards = Button(frame, image = cardimage, command = lambda: play_check(frame, Player1, cards, player.cardstringstorage[counter])) #Makes it a button, playcheck will automatically place it down

    #No stacking:
    #cards.grid(row=0, column=counter, pady=10, ipadx=10)

    #Stacking:

    if counter%2 == 0:
        cards.grid(row=0, column=counter, pady=10, ipadx=10)
    else:
        cards.grid(row=1, column=counter-1, pady=10, ipadx=10)

#------------------------------------------------------------

#Begin subroutine - 
def round():

    if Player1.attack == True:
        Player1.play = True
   
        pass
        
    elif Player2.attack == True:
        Player2.bestoption = find_best_attack_option(Player2, Round_deck)
        print(Player2.name, Player2.bestoption)
        bestcardcounter = Player2.cardstringstorage.index(Player2.bestoption)
        Player2.play = True
        bot_playcheck(player2_frame, Player2, Player2.bestoption, Player2.cardstringstorage[bestcardcounter], None)
        # attacker = Player2
        # escapeif = True
    
    elif Player3.attack == True:

        Player3.bestoption = find_best_attack_option(Player3, Round_deck)
        print(Player3.name, Player3.bestoption)
        bestcardcounter = Player3.cardstringstorage.index(Player3.bestoption)
        Player3.play = True
        bot_playcheck(player3_frame, Player3, Player3.bestoption, Player3.cardstringstorage[bestcardcounter], None)

        # attacker = Player3
        # escapeif = True

    elif Player4.attack == True:

        Player4.bestoption = find_best_attack_option(Player4, Round_deck)
        print(Player4.name, Player4.bestoption)
        bestcardcounter = Player4.cardstringstorage.index(Player4.bestoption)
        Player4.play = True
        bot_playcheck(player4_frame, Player4, Player4.bestoption, Player4.cardstringstorage[bestcardcounter], None)

        attacker = Player4
        # escapeif = True
        
    else:
        print("Error: No one is attacking")
   
        
    


def begin():
    #Start every match by:

    Round_deck.build() #Deck is built
    Round_deck.shuffle() #Deck is shuffled
    Round_deck.gentrump() #Trump generated

    playercycle(Player1, Player2, Player3, Player4) #Writes who is still in the game
    trump_display(Round_deck, trump_hand) #Trump is displayed on the screen

    six_cards(Player1, Round_deck) #Each player picks up 6 cards
    six_cards(Player2, Round_deck)
    six_cards(Player3, Round_deck)
    six_cards(Player4, Round_deck)

    for i in range (0,6): #Must be 6 otherwise 5 cards display.

        #Append string to hand
        Player1.cardstringstorage.append(cardstring(Player1, i))
        Player2.cardstringstorage.append(cardstring(Player2, i))
        Player3.cardstringstorage.append(cardstring(Player3, i))
        Player4.cardstringstorage.append(cardstring(Player4, i))

        #Display on screen - button as the player will need to click on them
        displayasbutton(Player1,player1_frame,i)

        #Make the bot's cards secret - labels as the player cant click on them
        botdisplayaslabel(Player2,player2_frame,i)
        botdisplayaslabel(Player3,player3_frame,i)
        botdisplayaslabel(Player4,player4_frame,i)
    
    deck_hand.configure(text = len(Round_deck.cards)) #Shows how many cards are left

    #Finds the value of the highest trump to see who starts
    Player1.findhighesttrump(Round_deck)
    Player2.findhighesttrump(Round_deck)
    Player3.findhighesttrump(Round_deck)
    Player4.findhighesttrump(Round_deck)

    highestvalue = firstturn(Player1.highestval,Player2.highestval,Player3.highestval,Player4.highestval)

    #Checks who has the highest value, meaning they start as they have the highest trump
    #Once highest value is calculated, now we need to know who has it, not very efficient though

    if Player1.highestval == highestvalue: #Player 1 attacks
        Player1.attack = True
        Player1.play = True
        find_defender(Player1, Player1, Player2, Player3, Player4) #Find out who defends
 
    elif Player2.highestval == highestvalue: #Player 2 attacks
        Player2.attack = True 
        Player2.play = True
        find_defender(Player2, Player1, Player2, Player3, Player4) #Find out who defends

    elif Player3.highestval == highestvalue: #Player 3 attacks
        Player3.attack = True
        Player3.play = True
        find_defender(Player3, Player1, Player2, Player3, Player4) #Find out who defends

    elif Player4.highestval == highestvalue: #Player 4 attacks
        Player4.attack = True
        Player4.play = True
        find_defender(Player4, Player1, Player2, Player3, Player4) #Find out who defends
    
    #Red=attack, green=defend, white=bystander/secondary defender
    configure_colour(Player1, player1_frame)
    configure_colour(Player2, player2_frame)
    configure_colour(Player3, player3_frame)
    configure_colour(Player4, player4_frame)

    start_button.destroy()#Get rid of begin button as its already used.
    round()

def render_into_play():
    pass


#Sets up placing area
durak_frame = Frame(root,  bg = "#594E3E")
durak_frame.pack(pady=20)

#Sets up each players' placing area
player1_frame = LabelFrame(durak_frame, text = Player1.name, bd = 0)
player1_frame.grid(row=3, column=1, padx=20, pady=20, ipadx=20)
Player1.frame = player1_frame

player2_frame = LabelFrame(durak_frame, text = Player2.name, bd = 0)
player2_frame.grid(row=0, column=0, padx=20, pady=20, ipadx=20)
Player2.frame = player2_frame

player3_frame = LabelFrame(durak_frame, text = Player3.name, bd = 0)
player3_frame.grid(row=0, column=1, padx=20, pady=20, ipadx=20)
Player3.frame = player3_frame

player4_frame = LabelFrame(durak_frame, text = Player4.name, bd = 0)
player4_frame.grid(row=0, column=2, padx=20, pady=20, ipadx=20)
Player4.frame = player4_frame



#put placing area in frame
  
player1_hand = LabelFrame(player1_frame, bd=0)
player1_hand.grid(row=0, column = 0, pady=20)

player1_grid = Frame(player1_frame)
player1_grid.columnconfigure(0,weight=1)


    #Player2
player2_hand = LabelFrame(player2_frame, bd=0)
player2_hand.grid(row=0, column = 0, pady=20)

player2_grid = Frame(player2_frame)
player2_grid.columnconfigure(0,weight=1)

    #Player3
player3_hand = LabelFrame(player3_frame, bd=0)
player3_hand.grid(row=0, column = 0, pady=20)

player3_grid = Frame(player3_frame)
player3_grid.columnconfigure(0,weight=1)

 #Player4
player4_hand = LabelFrame(player4_frame, bd=0)
player4_hand.grid(row=0, column = 0, pady=20)

player4_grid = Frame(player4_frame)
player4_grid.columnconfigure(0,weight=1)


#Deck displayer

deck_frame = LabelFrame(durak_frame, text = "Deck:", bd = 0)
deck_frame.grid(row=2, column=0, padx=20, pady=20, ipadx=20)

deck_hand = Label(deck_frame, text = "")
deck_hand.pack(pady=20)

#Playing area displayer

play_frame = LabelFrame(durak_frame, text = "", bd = 0, background = "#594E3E")
play_frame.grid(row=2, column=1,)

#Placing areas
attack_frame = Label(play_frame, text = "Attack Playing Area", background = "maroon")
attack_frame.pack()
Durak_Dealer.attackframe = attack_frame

defend_frame = Label(play_frame, text = "Defend Playing Area", background = "darkolivegreen")
defend_frame.pack()
Durak_Dealer.defendframe = defend_frame

#trump displayer

trump_frame = LabelFrame(durak_frame, text = "Trump:", bd = 0)
trump_frame.grid(row=2, column=2, padx=20, pady=20, ipadx=20)

trump_hand = Label(trump_frame, text = "")
trump_hand.pack(pady=20)

#create a couple of buttons

#starts the game
start_button = Button(durak_frame, text="Begin", command = begin)
start_button.grid(row=1, column=1, padx=20, pady=20, ipadx=20)

#trump displayer


root.mainloop()