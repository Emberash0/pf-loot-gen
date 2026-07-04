from random import randint
import Generate as Generate

class LootObject:
    def __init__(self, typeset: set, budget: int):
        options = list(typeset)
        while budget > 0 and len(options) > 0:
            if "H" in options or "I" in options:
                print("Were the creature(s) guarding a lair or hoard? (lair/hoard/n)")
                match input().lower():
                    case "lair":
                        self.treasure_type = "H"
                        options.remove("H")
                    case "hoard":
                        self.treasure_type = "I"
                        options.remove("I")
                    case default:
                        options.remove("I")
                        options.remove("H")
                        num_options = len(options) - 1
                        self.treasure_type = options[randint(0, num_options)]
            else:
                num_options = len(options) - 1
                self.treasure_type = options[randint(0, num_options)]
            match self.treasure_type:
                case "A":
                    options.remove("A")
                    self.coins = Generate.A(budget)
                    budget -= self.coins.value
                case "B":
                    self.coins, self.gems = Generate.B()
                case "C":
                    self.art = Generate.C()
                case "D":
                    self.coins, self.potions, self.scrolls, self.wands = Generate.D()
                case "E":
                    self.armour, self.weapons = Generate.E()
                case "F":
                    (
                        self.coins, 
                        self.potions, 
                        self.armour, 
                        self.shields, 
                        self.weapons, 
                        self.wondrous, 
                        self.rings
                    ) = Generate.F()
                case "G":
                    (
                        self.coins,
                        self.potions,
                        self.scrolls,
                        self.wands,
                        self.wondrous, 
                        self.rings, 
                        self.rods,
                        self.staves, 
                        self.weapons
                    ) = Generate.G()
                case "H":
                    (
                        self.coins,
                        self.weapons,
                        self.potions, 
                        self.scrolls,
                        self.gems,
                        self.wands,
                        self.armour,
                        self.weapons,
                        self.rings,
                        self.wondrous, 
                        self.rods,
                        self.staves
                    ) = Generate.H()
                case "I":
                    (
                        self.coins,
                        self.armour, 
                        self.wands,
                        self.art,
                        self.gems,
                        self.weapons, 
                        self.wondrous,
                        self.scrolls,
                        self.rings,
                        self.potions,
                        self.rods,
                        self.staves,
                    ) = Generate.I()
