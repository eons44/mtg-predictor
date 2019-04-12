import plotly
import plotly.graph_objs as go
import json
import argparse

descriptionStr = "CalcWin is a script designed to calculate the probability of having all pieces necessary for a winning combo in a Magic the Gathering deck. This does not account for opponent interaction and therefore does not give the probability of actually winning."

parser = argparse.ArgumentParser(description=descriptionStr)
parser.add_argument('-d','--deck', type=str, metavar='mydeck.json', help='deck file, in json format.', dest='deck', required=True)

args = parser.parse_args()

class Deck:

    class Combo:

        class Option:

            class Piece:
                def __init__(self):
                    self.name = "INVALID"
                    self.numCards = 0

            def __init__(self):
                self.name = "INVALID"
                self.pieces = []

        def __init__(self):
            self.name = "INVALID"
            self.options = []

    def __init__(self):
        self.name = "INVALID"
        self.totalCards = 0
        self.requiredCombos = []

    #parse json deck data
    def Parse(self, deck):
        self.name = deck['name']
        self.totalCards = deck['cards_in_deck']
        for c in deck['required_combos']:
            combo = self.Combo()
            combo.name = c['name']
            for o in c['possible_options']:
                option = self.Combo.Option()
                option.name = o['name']
                for p in o['pieces']:
                    piece = self.Combo.Option.Piece()
                    piece.name = p['name']
                    piece.numCards = p['num_cards']
                    option.pieces.append(piece)
                combo.options.append(option)
            self.requiredCombos.append(combo)

    def Print(self):
        print(self.name)
        print("Total cards: ", self.totalCards)
        print("Required combos:")
        for c in self.requiredCombos:
            print(" ", c.name)
            print("    Possible options:")
            for o in c.options:
                print("     ", o.name)
                print("        Pieces:")
                for p in o.pieces:
                    print("         ", p.name, ":", p.numCards, "cards")

    #calculate probability of drawing without replacement
    def ProbabilityOfDrawing(self, numOfCard, cardsDrawn):
        ret = 1.0
        #print("calculating probability of ", numOfCard, " in ", cardsDrawn, " draws")
        for c in range(0, cardsDrawn):
            inc =  (self.totalCards - c - numOfCard) / (self.totalCards - c)
            ret *= inc
        return 1.0 - ret

    def CalcWin(self, cardsDrawn):

        pWin = 1.0
        for c in self.requiredCombos:
            pNotCombo = 1.0
            for o in c.options:
                pAllPieces = 1.0
                for p in o.pieces:
                    #probability of getting all pieces
                    pAllPieces *= self.ProbabilityOfDrawing(p.numCards, cardsDrawn)
                #probability of not getting the combo is 
                #the probability of not getting all pieces for the option
                #and probability of not getting any other option
                pNotCombo *= 1.0 - pAllPieces
            
            pCombo = 1.0 - pNotCombo
            print ("probability of", c.name, "is", pCombo)

            #probability of winning is the probability of having this combo
            #and all other combos
            pWin *= pCombo
        return pWin

deck = Deck()
with open(args.deck) as deckFile:  
    deck.Parse(json.load(deckFile))
deck.Print()


turn = 1 #assume we go second, just subtract a turn if going first
pWin = 0 #we can't win turn 0 or 1.

turns = [] #because range doesn't work?
turns.append(0)
pWins = []
pWins.append(deck.CalcWin(7))
winStrs = []
winStrs.append("turn 0: " + str(pWins[0]))

while(pWin < 1.0): #arbitrary cutoff for "good enough"
    cards = 7+turn
    pWin = deck.CalcWin(cards)
    winStr = "Turn" + str(turn) + " : " + str(pWin)
    print(winStr)
    turns.append(turn)
    pWins.append(pWin)
    winStrs.append(winStr)
    turn = turn+1

plotly.offline.plot({
    "data": [go.Scatter(
        x=turns,
        y=pWins,
        mode='lines+markers',
#        mode='lines+markers+text',
#        text=winStrs,
        textposition='bottom right')],
    "layout": go.Layout(title="Probability of having winning combo"),
}, auto_open=False)
