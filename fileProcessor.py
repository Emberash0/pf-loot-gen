def ReadTable(file_name: str, l_or_c: str = "l") -> list:
    file_name = "tables/" + file_name
    with open(file_name) as f:
        file_contents = f.read()
    #reads .csv into list of rows
    file_rows = file_contents.split("\n")[1:]
    if l_or_c == "l":#if l tag used, returns the list of rows
        return file_rows
    else:#otherwise, if "c" tag, transforms into list of columns
        result = []
        num_columns = len(file_rows[0].split(","))
        #creates a list of empty lists corresponding to each column
        for _ in range(num_columns):
            result.append([])
        #populates each column row by row
        for row in file_rows:
            if row == "":
                break
            file_row = [x.strip(' "') for x in row.split(',')]
            for column in range(num_columns):
                result[column].append(file_row[column])
        return result

#read text file to list
def ReadFile(file_name: str) -> list:
    file_name = "tables/" + file_name
    with open(file_name) as f:
        file_contents = f.read()
    file_list = file_contents.split(", ")
    return file_list

#extra script to generate the bestiary from the rows of the bestiary file
def ProcessCreatures(file_rows: list[str]) -> list[object]:
    from creatures import LookupCreature
    lookup_creatures = []
    for row in file_rows:
        if row == "":
            break
        row_list = row.split(",")
        for item in row_list:
            item = item.strip(' "')
        creature = LookupCreature(row_list[0], row_list[1], row_list[2], row_list[3], row_list[4], row_list[5:])
        lookup_creatures.append(creature)
    return lookup_creatures

