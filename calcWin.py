import plotly
import plotly.graph_objs as go

numCards = 99
pColorUntap = 5 / numCards
pColorFixer = 4 / numCards
pGenericUntap = 2 / numCards
pDevotedDruid = 1 / numCards
pPlusPlus = 1 / numCards
pMana = 6 / numCards
pDraw = 7 / numCards

def CalcWin(cards):
    
    #calculate probability of having an untap combo
    pUntap = pColorUntap*cards * pColorFixer*cards
    pUntap += pGenericUntap*cards 
    pUntap += pDevotedDruid*cards * pPlusPlus*cards

    #infinite combo is having both mana and untap ability
    pCombo = pUntap * pMana*cards

    #winning is having infinite mana and reusable draw power
    pWin = pCombo * pDraw*cards
    return pWin

turn = 1 #assume we go second, just subtract a turn if going first
pWin = 0 #we can't win turn 0 or 1.

turns = [] #because range doesn't work?
turns.append(0)
pWins = []
pWins.append(CalcWin(7))
winStrs = []
winStrs.append("turn 0: " + str(pWins[0]))

while(pWin < 0.99): #arbitrary cutoff for "good enough"
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
        mode='markers+text',
#        mode='lines+markers+text',
#        text=winStrs,
        textposition='bottom right')],
    "layout": go.Layout(title="Probability of winning"),
}, auto_open=True)