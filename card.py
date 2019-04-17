from common import *
import re

class ManaCost:
    def __init__(self):
        self.black=0
        self.blue=0
        self.green=0
        self.red=0
        self.white=0
        self.colorless=0
        self.generic=0

    def GetCMC(self):
        return (
            self.black +
            self.blue + 
            self.green + 
            self.red + 
            self.white +
            self.colorless +
            self.generic
        )

    def FromString(self, string):
        self.black = string.count('{B}')
        self.blue = string.count('{U}')
        self.green = string.count('{G}')
        self.red = string.count('{R}')
        self.white = string.count('{W}')
        self.colorless = string.count('{C}')
        genericMana = re.findall(r'\d+', string)
        if (len(genericMana)):
            self.generic = genericMana[0]
        else:
            self.generic = 0

    def ToString(self):
        ret = ""
        if (self.generic):
            ret += '{' + str(self.generic) + '}'
        for b in range(self.black):
            ret += '{B}'
        for u in range(self.blue):
            ret += '{U}'
        for g in range(self.green):
            ret += '{G}'
        for r in range(self.red):
            ret += '{R}'
        for w in range(self.white):
            ret += '{W}'
        for c in range(self.colorless):
            ret += '{C}'
        return ret

class Card:
    def __init__(self):
        self.name = "INVALID"
        self.cost = ManaCost()
        self.text = []
        self.types = [] #includes subtypes and supertypes
        self.power = 0
        self.toughness = 0
        self.quality = 0

    #The quality or value that a card has is determined by the number of
    #   decks it is used in, according to edhrec.
    #This value may fluctuate dramatically, based on market forces;
    #   therefore, this will be the metric we will try to predict.
    def DetermineQuality(self):
        #this is pretty hacky. What we're doing is downloading the webpage
        #   for *this card from edhrec,
        #   then identifying the line that has the deck count in it, which is
        #   something like: <div class="nwdesc ellipsis">48 decks</div>,
        #   then using grep to extract the numeric value from the line,
        #   which we then assign to self.quality.
        edhrecName = self.name
        edhrecName = edhrecName.replace(",", "")
        edhrecName = edhrecName.replace("'", "")
        edhrecName = edhrecName.replace("!", "")
        edhrecName = edhrecName.replace('&', "")
        edhrecName = edhrecName.replace("  ", "-")
        edhrecName = edhrecName.replace(" ", "-")
        edhrecName = edhrecName.lower()
        print("Getting EDHRec rank for", self.name, "(", edhrecName, ")")

        commandStr = "curl -s https://www.edhrec.com/cards/"
        commandStr += edhrecName
        commandStr += " | grep nwdesc | grep -Eo '[0-9]{1,}'"
        quality = ExecuteCommand(commandStr)
        if (len(quality)):
            self.quality = int(quality)
        else:
            self.quality = 0

    def ToJSON(card):
        if isinstance(card, Card):
            return {
                'name': card.name,
                'cost': card.cost.ToString(),
                'text': card.text,
                'types': card.types,
                'power': card.power,
                'toughness': card.toughness,
                'quality': card.quality
            }
        raise TypeError(str(card) + ' is not JSON serializable')