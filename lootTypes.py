from getLoot import GetGem, GetArt

#The most basic treasure object has a name and value
class TreasureObject:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"A {self.name} worth {self.value}"

#Coins objects have a total value, and number of copper, silver, gold and platinum pieces 
class CoinsObject(TreasureObject):
    def __init__(self, coins: list[int]):
        value = 0
        self.copper = coins[0]
        value += self.copper / 100.0
        self.silver = coins[1]
        value += self.silver / 10.0
        self.gold = coins[2]
        value += self.gold
        self.platinum = coins[3]
        value += self.platinum * 10
        self.value = value

    #Adding two coins objects adds each field together
    def __add__(self, coins2):
        if not isinstance(coins2, CoinsObject):
            raise TypeError("Cannot add coins to other type")
        self.value += coins2.value
        self.copper += coins2.copper
        self.silver += coins2.silver
        self.gold += coins2.gold
        self.platinum += coins2.platinum
        return self

    def __repr__(self):
        return f"""
------ Coins ------
Coins worth a total of {self.value} gp:\n
{self.platinum} pp
{self.gold} gp
{self.silver} sp
{self.copper} cp"""

#Gems Objects are a list of gems with a total value, along with a total potential value
#which is the increase in value gained from cutting any currently uncut gems
class GemsObject(TreasureObject):
    def __init__(self, gems: list):
        self.gems = gems
        self.value = 0
        self.potential_value = 0
        for gem in gems:
            self.value += gem.value
            if gem.worked:
                self.potential_value += gem.value
            else:
                self.potential_value += gem.value + gem.improvement

    #object method to randomly generate a number of gems of the same grade
    #uses GetGem from getLoot.py
    def GenerateGems(self, grade, quantity):
        for _ in range(quantity):
            new_gem = GetGem(grade)
            self.gems += [new_gem]
            self.value += new_gem.value
            if isinstance(new_gem, UnworkedGem):
                self.potential_value += new_gem.improvement + new_gem.value
            else:
                self.potential_value += new_gem.value

    #Adding GemsObjects results in adding the value and potential value fields, and concatenating the lists of gems.
    def __add__(self, gems2):
        if not isinstance(gems2, GemsObject):
            raise TypeError("Cannot add gems to other types")
        self.value += gems2.value
        self.potential_value += gems2.potential_value
        self.gems += gems2.gems
        return self

    def __repr__(self):
        result = f"""
\n------ Gems ------
A selection of gems worth {self.value} gp total.
        """
        if self.value != self.potential_value:
            result += f"""
If all uncut gems were cut with Craft skill, 
total value would be {self.potential_value} gp.
            """
        result += f"\nGems are:"
        for gem in self.gems:
            if isinstance(gem, UnworkedGem):
                result += f"\n{gem.name} worth {gem.value} gp (plus {gem.improvement} if cut with DC {gem.DC} Craft)"
            else:
                result += f"\n{gem.name} worth {gem.value} gp."
        return result

#The Gem objects that populate GemsObject. A cut gem is simple, it stores its name and value
#Also generates an "an" property which self-determines whether to refer to it as a [gem] or an [gem].
class WorkedGem(TreasureObject):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        vowels = ["a", "e", "i", "o", "u"]
        self.an = self.name[0].lower() in vowels

    def __repr__(self):
        if self.an:
            line = f"\nAn {self.name}, worth {self.value} gp.\n"
        else:
            line = f"\nA {self.name}, worth {self.value} gp.\n"
        return line

#Unworked gems are a subset of worked gems, and additionally have an improvement value 
# the amount the value would increase if cut, and a DC value, the Craft DC to cut the gem.
class UnworkedGem(WorkedGem):
    def __init__(self, name: str, value: int, improvement: int, craft_DC: int):
        super().__init__(name, value)
        self.improvement = improvement
        self.DC = craft_DC

    def __repr__(self):
        if self.an:
            line = f"\nAn {self.name}, worth {self.value} gp.\n"
        else:
            line = f"\nA {self.name}, worth {self.value} gp.\n"
        line += f"""
Can be cut with a DC{self.DC} Craft 
which increases the value by {self.improvement} gp\n
        """
        return line
        
#ArtsObjects are a list of artworks with a total value
class ArtsObject(TreasureObject):
    def __init__(self, arts: list):
        self.arts = arts
        self.value = 0
        for art in arts:
            self.value += art.value

    #object method to randomly generate a number of artworks of the same grade
    #uses GetArt from getLoot.py
    def GenerateArts(self, grade, quantity):
        for _ in range(quantity):
            new_art = GetArt(grade)
            self.arts += [new_art]
            self.value += new_art.value

    #Adding ArtsObjects results in adding the value fields, and concatenating the lists of arts.
    def __add__(self, arts2):
        if not isinstance(arts2, ArtsObject):
            raise TypeError("Cannot add arts to other types")
        self.value += arts2.value
        self.arts += arts2.arts
        return self

    def __repr__(self):
        result = f"""
\n------ Art ------
A selection of art pieces worth {self.value} gp total.
        """
        result += f"\nArtworks are:"
        for art in self.arts:
            result += f"\n{art.name} worth {art.value} gp."
        return result

#Art objects populate ArtsObjects. They are simple and have a name and value   
class Art(TreasureObject):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        vowels = ["a", "e", "i", "o", "u"]
        self.an = self.name[0].lower() in vowels

    def __repr__(self):
        if self.an:
            line = f"\nAn {self.name}, worth {self.value} gp.\n"
        else:
            line = f"\nA {self.name}, worth {self.value} gp.\n"
        return line

