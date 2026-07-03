from fileProcessor import ReadTable

def FindRow(item, file):
    for row in file:
        if row[0] == item:
            return file.index(row)
    raise ValueError(f"'{item}' is an invalid creature type")

class Encounter:
    def __init__(self, creatures: list):
        self.creatures = creatures
        total_xp = 0
        total_val = 0
        types = set()
        file = ReadTable("creature_treasure_types.csv")
        new_file = []
        for row in file:
            new_row = row.split(",")
            new_file.append(new_row)
        for creature in self.creatures:
            total_xp += creature.xp * creature.quantity
            total_val += creature.value * creature.quantity
            target_row = new_file[FindRow(creature.type, new_file)]
            type_string = target_row[1]
            if target_row[2] != "":
                print(f"Is {creature.name} {target_row[2]}? (Y/N)\n")
                match input().lower():
                    case "y":
                        type_string += target_row[3]
                    case default:
                        pass
            for type in type_string:
                types.add(type)
        self.xp = total_xp
        self.value = total_val
        self.types = types
        
    
    def __repr__(self):
        return f"An encounter worth {self.xp}XP rewarding treasure equal to {self.value} gp. Treasure is of the following types: {self.types}\n"

