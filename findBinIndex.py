from dice import dice

#From a list of bin start values, returns the bin index that the value is within
def FindBinIndex(value, list):
    index = 0 #Initialises with 0 index

    #Runs until functions returns (bin found) or final bin reached (must be this one!)
    while index < len(list):
        #grabs bin value from current index
        check_val = int(list[index])
        #if value is same as bin start value, we must be in the current bin
        if value == check_val:
            result = index
            #In some tables, two adjacent bins have different outcomes, but identical bin values
            #If we are here, we must be at the lower of the two (if present) so check whether the next bin has the same start
            if index == len(list) - 1:
                return result
            check_next = int(list[result + 1])
            if check_val == check_next:
                #if so, pick one at random
                result += dice(2) - 1
            return result
        #if value is less than current bin start, we know the previous bin holds the value
        if value < check_val:
            result = index - 1
            #However, if there were two bins of the same start point, we have found the latter
            #So check it against the one before...
            check_previous = int(list[result])
            check_val = int(list[result - 1])
            #And if true, choose one at random
            if check_val == check_previous:
                result -= dice(2) - 1
            return result
        result = index
        index += 1
    return result