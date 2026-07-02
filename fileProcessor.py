def ReadTable(file_name: str, l_or_c: str = "l") -> list:
    file_name = "tables/" + file_name
    with open(file_name) as f:
        file_contents = f.read()
    file_rows = file_contents.split("\n")[1:]
    if l_or_c == "l":
        return file_rows
    else:
        result = []
        num_columns = len(file_rows[0].split(","))
        for i in range(num_columns):
            column = []
            for j in range(len(file_rows)):
                file_row = file_rows[j].split(",")
                if file_row == [""]:
                    break
                column.append(file_row[i])
            result.append(column)
        return result

def ReadFile(file_name: str) -> list:
    file_name = "tables/" + file_name
    with open(file_name) as f:
        file_contents = f.read()
    file_list = file_contents.split(", ")
    return file_list

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

