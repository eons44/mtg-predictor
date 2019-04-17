#!/usr/bin/python3

from jsonParser import *

parser = JSONParser()

# parser.ParseMTGJSON("data/sampleCards.json")
parser.ParseCondensedJSON("data/sampleCards_condensed.json")
#parser.OutputTo("data/sampleCards_condensed.json")

#parser.ParseMTGJSON("data/allCards.json")
#parser.OutputTo("data/allCards_condensed.json")

# parser.ParseCondensedJSON("data/allCards_condensed.json")
# parser.UpdateCardQuality()
parser.TrimCards()
parser.PrintCards()
# parser.OutputTo("data/allCards_condensed.json")
#parser.OutputTo("data/allCards_trimmed.json")