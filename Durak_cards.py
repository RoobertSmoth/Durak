#Durak cards

#import libraries

import random
from tkinter import *
import time

#Value dictionary:
Valuedictionary = {"ace" : 14,"K" : 13,
                   "Q" : 12, "B" : 11,
                   "ten" : 10, "nine" : 9,
                   "eight" : 8, "seven" : 7,
                   "six" : 6, "five" : 5,
                   "four" : 4, "three" : 3,
                   "two" : 2}

#Takes the values of cards and creates a numerical value for them
#Used in calculating the highest trump.




#Card class
class Card(object):  #Capital to distinguish
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        print(self.value + self.suit)


#Deck class

class Deck(object):
    def __init__(self):
        self.cards = [] #creates array which is a deck of cards
        self.build
        self.gentrump
        self.trumphand = []
        self.trumpsuit = ""

    def build(self):
        for s in ["spades","clubs","diamonds","hearts"]: #Array of suits,s = suits
            for v in ["six","seven","eight","nine","ten","ace","B","Q","K"]: #6 and above cards are used
                self.cards.append(Card(s,v)) #adds card object to list

    def show(self):
        for c in self.cards: # very every card in cards, show it| c = cards
            c.show()

    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            rand = random.randint(0,i)
            self.cards[i], self.cards[rand] = self.cards[rand], self.cards[i] #swaps cards 
               

    def drawcard(self):
        return self.cards.pop() #returns card at the top of cards list
    
    def gentrump(self):
        self.trumphand.append(self.drawcard())
        self.trumpsuit = self.trumphand[0].suit

    


#Player Class

class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.cardstringstorage=[] #used to store pyimages
        self.imagestoreref=[] #used in render_card
        self.attack = False #Whose go it is at the moment to attack
        self.defend = False #Who is defending
        self.highestval = 0 #Used in calculating the highest trump card a user has
        self.win = False #If win is True, they are excluded from player cycle
        self.play = False
        self.bestoption = ""
        self.frame = ""
        self.player1doneplaying = False
        self.pickedup = False
        self.secondaryattack = False


    def draw(self, deck):
        self.hand.append(deck.drawcard())
        return self

    def showhand(self):
        for card in self.hand:
            card.show()

    def discard(self):
        return self.hand.pop()
    
    def clearall(self):
        self.cardstringstorage.clear()
        self.imagestoreref.clear()
        self.hand.clear()

    def findhighesttrump(self, deck):

        for card in self.cardstringstorage:
            if deck.trumpsuit in card:
                if self.highestval < Valuedictionary[card[0:-len(deck.trumpsuit)]]:
                    self.highestval = Valuedictionary[card[0:-len(deck.trumpsuit)]]
        return self.highestval   

    def findcardvalue(self, card):
        value_array = ["one","two","three","four","five","six","seven","eight","nine","ten","B","Q","K","ace"]
        for value in value_array:
            if value in card:
                cardvalue = Valuedictionary[value]
                suit = card[len(value):len(card)]
        return cardvalue, suit
                

    def attack_action(self, card, cardframename, dealerframe):
        attack_card = card #Store attack card seperately
        index = self.cardstringstorage.index(card) #Find index to remove all card references

        self.hand.pop(index) #Removes from hand
        self.cardstringstorage.pop(index) #Removes from string storage
        #self.imagestoreref.clear() #Prepare to regenerate hand


        cardframename.destroy() #Destroys the image
        #add in a function that allows me to play cards of the same value
        self.play = False #Stops the player from spamming clicks

        
        return attack_card
    
    def pickuppossibility(self, attacksuit, attackvalue, trumpsuit):
        failurepossibility = 0 #Resets failure possibility
        cardabletobeplaced = 0

        for card in self.cardstringstorage:

            defendvalue, defendsuit = self.findcardvalue(card)

            if (defendvalue > attackvalue and defendsuit == attacksuit) or (defendsuit == trumpsuit and attacksuit != trumpsuit):
                cardabletobeplaced += 1 #if there is a card that fits the criteria, they can play so no failure
            else:
                failurepossibility += 1 #if failurepossibility reaches hand length, failure is at its highest

        if failurepossibility == len(self.cardstringstorage): #They have no choice to pick up
            print("Must pick up")
            self.play = False
            return True
        elif cardabletobeplaced <len(self.cardstringstorage) and failurepossibility > 0: #Optional to pick up
            print("Picking up is optional.")
            return False
        elif cardabletobeplaced == len(self.cardstringstorage): #They can play how they like and shouldnt pick up ideally
            print("All cards can be played. Not recommended to pick up.")
            return True
        else:
            print("Unknown how you got here")
        
        

        

    def defend_action(self, card, cardframename, attackcard, trumpsuit):
        #attackingcard, trumpsuit
        value_array = ["one","two","three","four","five","six","seven","eight","nine","ten","B","Q","K","ace"]
        
        attackvalue, attacksuit = self.findcardvalue(attackcard)
        defendvalue, defendsuit = self.findcardvalue(card)

        self.pickuppossibility(attacksuit,attackvalue,trumpsuit)

        if (defendvalue > attackvalue and defendsuit == attacksuit) or (defendsuit == trumpsuit and attacksuit != trumpsuit):

            defend_card = card #Store defend card seperately
            

            #Hand/display maintenance:
            index = self.cardstringstorage.index(card) #Find index to remove all card references
            self.hand.pop(index) #Removes from hand
            self.cardstringstorage.pop(index) #Removes from string storage
            self.imagestoreref.clear() #Prepare to regenerate hand
            cardframename.destroy() #Destroys the image
            self.play = False #Stops the player from spamming clicks
            return defend_card
        else:
            print(card,"cannot beat",attackcard)
    
    def attack_again(self, dealer):
        canattackagain = False
        fullroundcards = []
        playablecards = []

        for card in dealer.defendcardround:
            fullroundcards.append(card)
        for card in dealer.attackcardround:
            fullroundcards.append(card)
        
        for attackcard in self.cardstringstorage: #Every attacking card must be compared
            attackvalue, attacksuit = self.findcardvalue(attackcard)

            for a in range(0, len(fullroundcards)):

                defendvalue, defendsuit = self.findcardvalue(fullroundcards[a])

                if attackvalue == defendvalue and attackcard != fullroundcards[a] and attackcard not in playablecards:
                    canattackagain = True
                    playablecards.append(attackcard)
        return canattackagain, playablecards
                
         




#Bot class

class Bot(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.imagestore = []
        self.gencardback
    
    def gencardback(self):
        for card in self.hand:
            self.imagestore.clear()
            self.imagestore.append("cardbackblue")

    def attack_action_bot(self, card, cardframename): #maybe remove bot to override superclass attack
        attack_card = card #Store attack card seperately
        index = self.cardstringstorage.index(card) #Find index to remove all card references

        self.hand.pop(index) #Removes from hand
        self.cardstringstorage.pop(index) #Removes from string storage
        
        
        # self.play = False #Stops the player from spamming clicks
        return attack_card
        
        #Returns to be outputted
    

    def defend_action_bot(self, card, cardframename, attackcard, trumpsuit):
        
        #attackingcard, trumpsuit
        value_array = ["one","two","three","four","five","six","seven","eight","nine","ten","B","Q","K","ace"]
        
        attackvalue, attacksuit = self.findcardvalue(attackcard)
        defendvalue, defendsuit = self.findcardvalue(card)

        self.pickuppossibility(attacksuit,attackvalue,trumpsuit)

        if (defendvalue > attackvalue and defendsuit == attacksuit) or (defendsuit == trumpsuit and attacksuit != trumpsuit):

            defend_card = card #Store defend card seperately
            

            #Hand/display maintenance:
            index = self.cardstringstorage.index(card) #Find index to remove all card references
            self.hand.pop(index) #Removes from hand
            self.cardstringstorage.pop(index) #Removes from string storage
            self.imagestoreref.clear() #Prepare to regenerate hand

            self.play = False #Stops the player from spamming clicks
            return defend_card
        
        else:
            print(card,"cannot beat",attackcard)

        
    def pickup_bot(self, dealer):
        self.pickedup = True
        for card in dealer.currentframecontents: #First need to add cards to hand
            cardvalue, cardsuit = self.findcardvalue(card)
            cardvalue = card[0:-(len(cardsuit))]
            card = Card(cardsuit,cardvalue)
            self.hand.append(card)

        dealer.currentframecontents.clear()
        self.cardstringstorage.clear()
        self.imagestoreref.clear()

        self.play = False

    def think(self):
        waitThreshold = random.randint(1,3)
        botTimerWait = time.time()
        while time.time() - botTimerWait <= waitThreshold:
            continue


            

class Dealer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.attackcardround = []
        self.defendcardround = []
        self.attackcard = ""
        self.defendcard = ""
        self.gamehistory = []
        self.allowedvalues = []
        self.currentframecontents = []
        self.currentattack = []
        self.currentdefend = []
        self.imagestorerefdefend = []
        self.imagestorerefattack = []
        self.attackframe = None
        self.defendframe = None


Player1 = Player("Lara") #First player

Player2 = Bot("Liz")

Player3 = Bot("Gabi")

Player4 = Bot("Alice")

Durak_Dealer = Dealer("Durak Dealer") #Helps display attacking and defending cards

