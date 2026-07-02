from fileProcessor import ReadTable

def FindBinIndex(value, list):
    bin_found = False
    index = 0
    while not bin_found:
        check_val = int(list[index])
        if value == check_val:
            return index
        if value < check_val:
            return index - 1
        index += 1

class Encounter:
    def __init__(self, creatures: list):
        treasure_lookup = ReadTable("Treasure_by_XPTotal.csv", "c")
        xp_list = treasure_lookup[0]
        slow_list = treasure_lookup[1]
        medium_list = treasure_lookup[2]
        fast_list = treasure_lookup[3]
        self.creatures = creatures
        total_xp = 0
        for creature in self.creatures:
            total_xp += creature.xp
        self.xp = total_xp
        print("What pace is your campaign running with? (slow, medium, fast)\n")
        pace = input().lower()
        bin_index = FindBinIndex(self.xp, xp_list)
        match pace:
            case "slow":
                self.value = slow_list[bin_index]
            case "medium":
                self.value = medium_list[bin_index]
            case "fast":
                self.value = fast_list[bin_index]
            case default:
                print("Unexpected pace entry, assuming medium...")
                self.value = medium_list[bin_index]
    
    def __repr__(self):
        return f"An encounter worth {self.xp}XP rewarding treasure equal to {self.value} gp.\n"

