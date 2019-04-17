from card import *
import re
import json

class JSONParser:
    def __init__(self):
        self.cards = []
        self.ignoredSets = ["UNH", "UST", "UNG"]

    def ParseMTGJSON(self, mtgjsonFile):
        jsonCards = json.load(open(mtgjsonFile, "r"))
        for c in jsonCards:
            cardInfo = jsonCards[c]

            if any(s in self.ignoredSets for s in cardInfo["printings"]):
                print("Ignoring", c, "- bad set")
                continue

            print("Processing", c)
            card = Card()
            card.name = c
            if "manaCost" not in cardInfo:
                card.cost = ManaCost()
            else:
                card.cost.FromString(cardInfo["manaCost"])
            if "text" in cardInfo:
                card.text = cardInfo["text"].splitlines()
            card.types = cardInfo["supertypes"]
            card.types += cardInfo["types"]
            card.types += cardInfo["subtypes"]
            if "power" in cardInfo:
                card.power = cardInfo["power"]
                #save on speed by not checking for toughness too
                card.toughness = cardInfo["toughness"]
            #card.DetermineQuality()
            self.cards.append(card)

    def UpdateCardQuality(self):
        for c in self.cards:
            c.DetermineQuality()

    def TrimCards(self):
        #Remove cards that had an error in quality (or aren't used at all)
        self.cards = [c for c in self.cards if c.quality != 0]
        
        #Remove reminder text and extraneous words
        for c in self.cards:
            text = []
            for t in c.text:
                line = re.sub("[\(].*?[\)]", "", t)
                line = line.replace("  "," ")
                line = line.replace(c.name, "THIS_CARD")
                line = line.strip()
                text.append(line)
            c.text = text

    def OutputTo(self, outFile):
        json.dump(self.cards, open(outFile, "w"), indent=4, default=Card.ToJSON)

    def ParseCondensedJSON(self, condensedFile):
        jsonCards = json.load(open(condensedFile, "r"))
        for c in jsonCards:
            card = Card()
            card.name = c["name"]
            card.cost.FromString(c["cost"])
            card.text = c["text"]
            card.types = c["types"]
            card.power = c["power"]
            card.toughness = c["toughness"]
            card.quality = c["quality"]
            self.cards.append(card)

    def PrintCards(self):
        print(json.dumps(self.cards, indent=2, default=Card.ToJSON))