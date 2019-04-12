import plotly
import plotly.graph_objs as go

numCards = 99
nColorUntap = 5
nColorFixer = 4
nGenericUntap = 2
nDevotedDruid = 1
nPlusPlus = 1
nMana = 6
nDraw = 7

#calculate probability of drawing without replacement
def ProbabilityOfDrawing(numOfCard, totalCards, cardsDrawn):
    ret = 1.0
    #print("calculating probability of ", numOfCard, " in ", cardsDrawn, " draws")
    for c in range(0, cardsDrawn):
        inc =  (totalCards - c - numOfCard) / (totalCards - c)
        ret *= inc
    return 1.0 - ret

def CalcWin(cards):

    #determine the probability of getting each type of card
    pColorUntap = ProbabilityOfDrawing(nColorUntap, numCards, cards)
    pColorFixer = ProbabilityOfDrawing(nColorFixer, numCards, cards)
    pGenericUntap = ProbabilityOfDrawing(nGenericUntap, numCards, cards)
    pDevotedDruid = ProbabilityOfDrawing(nDevotedDruid, numCards, cards)
    pPlusPlus = ProbabilityOfDrawing(nPlusPlus, numCards, cards)
    pMana = ProbabilityOfDrawing(nMana, numCards, cards)
    pDraw = ProbabilityOfDrawing(nDraw, numCards, cards)
    print("probability of draw is ", pDraw)
    
    #calculate probability of having an untap combo
    pNotUntap = 1.0 - pColorUntap * pColorFixer
    pNotUntap *= 1.0 - pGenericUntap
    pNotUntap *= 1.0 - pDevotedDruid * pPlusPlus
    pUntap = 1.0 - pNotUntap

    #infinite combo is having both mana and untap ability
    pCombo = pUntap * pMana

    #winning is having infinite mana and reusable draw power
    pWin = pCombo * pDraw

    print("probability of untap is ", pUntap)
    print("probability of mana is ", pMana)
    return pWin

turn = 1 #assume we go second, just subtract a turn if going first
pWin = 0 #we can't win turn 0 or 1.

turns = [] #because range doesn't work?
turns.append(0)
pWins = []
pWins.append(CalcWin(7))
winStrs = []
winStrs.append("turn 0: " + str(pWins[0]))

while(pWin < 1.0): #arbitrary cutoff for "good enough"
    cards = 7+turn
    pWin = CalcWin(cards)
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
