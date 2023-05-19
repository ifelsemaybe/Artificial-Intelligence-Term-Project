#nbr of blocking vehicule from ambulance to exit
def h1(state):
    blockedCars = 0
    ambulanceCar = state.Cars["A"]

    x = ambulanceCar.frontPos[0]-1
    y = ambulanceCar.frontPos[1]-1

    currentVehiculeName = "A"
    if(ambulanceCar.direction == "Horizontal"):
        while y < 6:
            if(state.grid[x][y] == "."): #if its a ".", just increase i and
                y += 1
                continue
            else: #if there's a car
                if(currentVehiculeName == state.grid[x][y]): #same car
                    y += 1
                    continue
                else: #new car
                    blockedCars = blockedCars + 1 #increase nbr blocked
                    currentVehiculeName = state.grid[x][y]
            y += 1

    i=y-1
    while i < 5:

        if not state.grid[x-1][i+1] == ".":  # if next element is NOT ".", check if vehiculeName is the same
            if currentVehiculeName == state.grid[x - 1][i]:# same car
                continue
            else:  # new car
                blockedCars += 1  # increase nbr blocked
                currentVehiculeName = state.grid[x-1][i+1]

        i += 1
    return blockedCars

#count blocked position
def h2(state):
    blockedPosition = 0
    ambulanceCar = state.Cars["A"]
    x = ambulanceCar.frontPos[0]-1
    y = ambulanceCar.frontPos[1]-1

    if(ambulanceCar.direction == "Horizontal"):

        while y < 6:
            if(state.grid[x][y] != "." and state.grid[x][y] != "A"): #if there's a car
                blockedPosition = blockedPosition + 1 #increase nbr blocked position
            y += 1
    #should never happen
    else: #its vertical
        i=1
        while y < 6:
            if(not(state.grid[y+i][x] == ".")): #if its a ".", just increase i and
                blockedPosition = blockedPosition + 1
            i = i+1
    return blockedPosition

#constant of 5
def h3(state):
    return (h1(state) * 5)

#distance between ambulance and the goal
def h4(state):

    ambulanceCar = state.Cars["A"]
    y = ambulanceCar.frontPos[1]

    return (6-y)