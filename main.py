import copy
import heuristic
import heapq
import time
import output

nbrOfStates = 0

nbrOfIterations = 0

inputList = []

customFuel_save = {}


# frontPos: Right most or bottom most
# backPos: left most or top most
class Vehicule:

    def __init__(self, fuel, backPos, frontPos, direction, length, isAmbulance, letter):
        self.fuel = fuel
        self.frontPos = frontPos
        self.backPos = backPos
        self.direction = direction
        self.length = length
        self.isAmbulance = isAmbulance
        self.letter = letter

    def __str__(self):
        string = "Car Name " + self.letter + ":\n" + "Position ranging from " + "".join(
            map(str, self.backPos)) + " to " + "".join(
            map(str, self.frontPos)) + " - facing " + self.direction + "y - has length of " + str(
            self.length) + " - Fuel level at (" + str(self.fuel) + ") - isAmbulance?(" + str(
            self.isAmbulance) + ").\n\n"

        self.fuel = int(self.fuel)
        self.length = int(self.length)
        self.isAmbulance = bool(self.isAmbulance)

        return string


# once you create a state, change the value of the h you want
class State:
    # 6x6 matrix filled with "."
    grid = [["." for j in range(6)] for i in range(6)]

    parentGrid_index = None
    index = 0

    # all cars in a Dictionary (hashmap)
    Cars = {}

    algo = ""

    h1 = 0
    h2 = 0
    h3 = 0
    h4 = 0

    g = 0  # pathcost

    moveDir = ""
    moveCount = 0
    moveLetter = ""

    def __init__(self, grid, Cars, index, parentGrid_index, g, h1, h2, h3, h4, moveDir="", moveCount=0, moveLetter=""):

        self.grid = grid
        self.Cars = Cars
        self.index = index
        self.parentGrid_index = parentGrid_index
        self.g = g
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.moveDir = moveDir
        self.moveCount = moveCount
        self.moveLetter = moveLetter

    def __str__(self):

        string = "State #" + str(self.index) + "\n\n\n"

        self.index = int(str(self.index))

        for x in range(6):
            for y in self.grid[x]:
                string += y + " "

            string += "\n"

        string += "\n\n\n"

        return string

    def __lt__(self, other):

        if self.algo == "gbfs_h1":
            return self.h1 < other.h1
        if self.algo == "gbfs_h2":
            return self.h2 < other.h2
        if self.algo == "gbfs_h3":
            return self.h3 < other.h3
        if self.algo == "gbfs_h4":
            return self.h4 < other.h4

        if self.algo == "a_h1":
            return (self.h1 + self.g) < (other.h1 + other.g)
        if self.algo == "a_h2":
            return (self.h2 + self.g) < (other.h2 + other.g)
        if self.algo == "a_h3":
            return (self.h3 + self.g) < (other.h3 + other.g)
        if self.algo == "a_h4":
            return (self.h4 + self.g) < (other.h4 + other.g)

        if self.algo == "ucs":
            return self.g < other.g


    def __le__(self, other):

        if self.algo == "gbfs_h1":
            return self.h1 <= other.h1
        if self.algo == "gbfs_h2":
            return self.h2 <= other.h2
        if self.algo == "gbfs_h3":
            return self.h3 <= other.h3
        if self.algo == "gbfs_h4":
            return self.h4 <= other.h4

        if self.algo == "a_h1":
            return (self.h1 + self.g) <= (other.h1 + other.g)
        if self.algo == "a_h2":
            return (self.h2 + self.g) <= (other.h2 + other.g)
        if self.algo == "a_h3":
            return (self.h3 + self.g) <= (other.h3 + other.g)
        if self.algo == "a_h4":
            return (self.h4 + self.g) <= (other.h4 + other.g)

        if self.algo == "ucs":
            return self.g <= other.g

    def __eq__(self, other):

        return self.grid == other.grid

    def copy_constructor(self, other):

        self.grid = copy.deepcopy(other.grid)
        self.Cars = copy.deepcopy(other.Cars)

        self.index = other.index
        self.parentGrid_index = other.parentGrid_index
        self.g = other.g
        self.h1 = other.h1
        self.h2 = other.h2
        self.h3 = other.h3
        self.h4 = other.h4
        self.algo = other.algo
        self.moveDir = other.moveDir
        self.moveCount = other.moveCount
        self.moveLetter = other.moveLetter


class ParkingLot:

    #game state defined as state, but does not initialize object
    gameState = State

    def reset(self, grid=[[]], Cars={}, index=0, parentGrid_index=None, g=0, h1=0, h2=0, h3=0, h4=0, moveDir="", moveCount=0, moveLetter=""):

        self.gameState.grid = copy.deepcopy(grid)

        self.reset_Cars(self.gameState.grid)

        self.gameState.index = index
        self.gameState.parentGrid_index = parentGrid_index
        self.gameState.g = g
        self.gameState.h1 = h1
        self.gameState.h2 = h2
        self.gameState.h3 = h3
        self.gameState.h4 = h4
        self.gameState.moveDir = moveDir
        self.gameState.moveCount = moveCount
        self.gameState.moveLetter = moveLetter

    def reset_Cars(self, grid):

        global customFuel_save

        self.gameState.Cars.clear()

        carChar = ""
        posTrackS = [0, 0]  # start
        posTrackE = [0, 0]  # end
        size = 0
        ambulanceCheck = False

        delete = False

        for i in range(6): #For horizontal cars

            carChar = ""

            for j in range(6):

                if grid[i][j] != ".":

                    if carChar == grid[i][j]:
                        size += 1
                        posTrackE = [i + 1, j + 1]

                    else:

                        if carChar == "":
                            carChar = grid[i][j]
                            size = 1
                            posTrackS = [i + 1, j + 1]
                            posTrackE = [i + 1, j + 1]
                            if carChar == "A":
                                ambulanceCheck = True

                        else:

                            if size > 1:
                                self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Horizontal", size, ambulanceCheck, carChar)})

                            carChar = grid[i][j]
                            size = 1
                            posTrackS = [i + 1, j + 1]
                            posTrackE = [i + 1, j + 1]
                            if carChar == "A":
                                ambulanceCheck = True
                            else:
                                ambulanceCheck = False

                if j == 5 and carChar not in self.gameState.Cars and size > 1:

                    if i == 2 and grid[i][j] != ".":

                        delete = True
                        carChar = ""
                        size = 0

                    else:

                        self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Horizontal", size, ambulanceCheck, carChar)})

                if delete:

                    for k in range(6):

                        if self.gameState.grid[2][k] == grid[i][j]:
                            self.gameState.grid[2][k] = "."

                    delete = False

        carChar = ""
        posTrackS = [0, 0]
        posTrackE = [0, 0]
        size = 0
        ambulanceCheck = False

        for i in range(6): #For vertical cars

            carChar = ""

            for j in range(6):

                if self.gameState.grid[j][i] != ".":

                    if carChar == self.gameState.grid[j][i]:
                        size += 1
                        posTrackE = [j + 1, i + 1]

                        if j == 5 and carChar not in self.gameState.Cars and size > 1:
                            self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Vertical",
                                                                          size, ambulanceCheck, carChar)})

                    else:

                        if carChar == "":
                            carChar = self.gameState.grid[j][i]
                            size = 1
                            posTrackS = [j + 1, i + 1]
                            posTrackE = [j + 1, i + 1]
                            if carChar == "A":
                                ambulanceCheck = True

                        else:

                            if size > 1:
                                self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Vertical", size, ambulanceCheck, carChar)})

                            carChar = self.gameState.grid[j][i]
                            size = 1
                            posTrackS = [j + 1, i + 1]
                            posTrackE = [j + 1, i + 1]
                            if carChar == "A":
                                ambulanceCheck = True
                            else:
                                ambulanceCheck = False

                if j == 5 and carChar not in self.gameState.Cars and size > 1:
                    self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Vertical", size, ambulanceCheck, carChar)})


        for k, v in customFuel_save.items():
            self.gameState.Cars[k].fuel = v



    def __str__(self):

        string = "GRID: \n\n"

        for x in range(6):
            for y in self.gameState.grid[x]:
                string += y + " "

            string += "\n"

        string += "\n\n\n"

        for key, car in self.gameState.Cars.items():
            string += car.__str__()

        return string

    def gridInit(self):

        global inputList
        global nbrOfStates
        global customFuel_save

        nbrOfStates += 1
        customFuel_save.clear()

        string = inputList.pop(0).split()

        self.gameState.grid = [["." for j in range(6)] for i in range(6)]
        self.gameState.Cars = {}

        for x in string:

            # Initialize all cars and grid of the original game state
            if len(x) == 36:

                char = 0

                carChar = ""
                posTrackS = [0, 0]  # start
                posTrackE = [0, 0]  # end
                size = 0
                ambulanceCheck = False

                delete = False

                # for each space in the grid, either fill it up with a car, or keep it empty
                for i in range(6):
                    carChar = ""
                    for j in range(6):

                        # space contains a car
                        if x[char] != ".":

                            if carChar == x[char]:
                                size += 1
                                posTrackE = [i + 1, j + 1]

                            else:

                                if carChar == "":
                                    carChar = x[char]
                                    size = 1
                                    posTrackS = [i + 1, j + 1]
                                    posTrackE = [i + 1, j + 1]
                                    if carChar == "A":
                                        ambulanceCheck = True

                                else:

                                    if size > 1:
                                        self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE,
                                                                                      "Horizontal", size,
                                                                                      ambulanceCheck, carChar)})

                                    carChar = x[char]
                                    size = 1
                                    posTrackS = [i + 1, j + 1]
                                    posTrackE = [i + 1, j + 1]
                                    if carChar == "A":
                                        ambulanceCheck = True
                                    else:
                                        ambulanceCheck = False

                            self.gameState.grid[i][j] = x[char]

                        if j == 5 and carChar not in self.gameState.Cars and size > 1:

                            if i == 2 and x[char] != ".":

                                delete = True
                                carChar = ""
                                size = 0

                            else:

                                self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Horizontal",
                                                                              size, ambulanceCheck, carChar)})

                        if delete:

                            for k in range(6):

                                if self.gameState.grid[2][k] == x[char]:
                                    self.gameState.grid[2][k] = "."

                            delete = False

                        char += 1

                carChar = ""
                posTrackS = [0, 0]
                posTrackE = [0, 0]
                size = 0
                ambulanceCheck = False

                for i in range(6):

                    carChar = ""

                    for j in range(6):

                        if self.gameState.grid[j][i] != ".":

                            if carChar == self.gameState.grid[j][i]:
                                size += 1
                                posTrackE = [j + 1, i + 1]

                                if j == 5 and carChar not in self.gameState.Cars and size > 1:
                                    self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Vertical",
                                                                                  size, ambulanceCheck, carChar)})

                            else:

                                if carChar == "":
                                    carChar = self.gameState.grid[j][i]
                                    size = 1
                                    posTrackS = [j + 1, i + 1]
                                    posTrackE = [j + 1, i + 1]
                                    if carChar == "A":
                                        ambulanceCheck = True

                                else:

                                    if size > 1:
                                        self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE,
                                                                                      "Vertical", size, ambulanceCheck,
                                                                                      carChar)})

                                    carChar = self.gameState.grid[j][i]
                                    size = 1
                                    posTrackS = [j + 1, i + 1]
                                    posTrackE = [j + 1, i + 1]
                                    if carChar == "A":
                                        ambulanceCheck = True
                                    else:
                                        ambulanceCheck = False

                        if j == 5 and carChar not in self.gameState.Cars and size > 1:
                            self.gameState.Cars.update({carChar: Vehicule(100, posTrackS, posTrackE, "Vertical", size,
                                                                          ambulanceCheck, carChar)})

            # Apply custom fuel to correct car. ex J0 -> car J has 0 fuel
            else:

                customFuel_save[x[0]] = int(x[1:])
                self.gameState.Cars[x[0]].fuel = int(x[1:])


def readInput():
    f = open("puzzles.txt", "r")

    global inputList

    global nbrOfIterations

    nbrOfIterations = 1

    for line in f:
        if line.startswith("#") or line.startswith('\n'):
            continue
        inputList.append(line)
        # nbrOfIterations += 1


def PossibleMoves(lot):
    carChecked = []
    listOfStates = []
    global nbrOfStates

    for i in range(6): #First for loop checks for horizontal moves
        left_moveCount = 0
        right_moveCount = 0
        carBuffer = ""

        for j in range(6):
            if lot.gameState.grid[i][j] == ".":
                left_moveCount += 1
                if carBuffer != "":
                    right_moveCount += 1
                    new_grid = copy.deepcopy(lot.gameState.grid)
                    new_cars = copy.deepcopy(lot.gameState.Cars)
                    old_backPos = copy.deepcopy(new_cars[carBuffer].backPos)
                    new_cars[carBuffer].backPos[1] += right_moveCount
                    new_cars[carBuffer].frontPos[1] += right_moveCount
                    new_cars[carBuffer].fuel -= right_moveCount

                    nbrOfStates += 1

                    charBuffer = "."

                    if new_cars[carBuffer].frontPos[0] == 3 and new_cars[carBuffer].frontPos[1] == 6:

                        for k in range(new_cars[carBuffer].frontPos[1] - old_backPos[1] + 1):

                            new_grid[i][k + old_backPos[1] - 1] = charBuffer

                        del new_cars[carBuffer]

                    else:

                        for k in range(new_cars[carBuffer].frontPos[1] - old_backPos[1] + 1):

                            if k == right_moveCount:
                                charBuffer = carBuffer

                            new_grid[i][k+old_backPos[1] - 1] = charBuffer

                    listOfStates.append(State(new_grid, new_cars, nbrOfStates-1, lot.gameState.index, lot.gameState.g+1, 0, 0, 0, 0, "right", right_moveCount, carBuffer)) #Creates a new State for a possible right move



            if lot.gameState.grid[i][j] != "." and lot.gameState.grid[i][j] not in carChecked:

                car = lot.gameState.Cars[lot.gameState.grid[i][j]]
                carBuffer = car.letter
                carChecked.append(carBuffer)
                right_moveCount = 0

                if car.direction == "Vertical" or car.fuel == 0:

                    left_moveCount = 0
                    carBuffer = ""

                    continue

                for k in range(left_moveCount):

                    new_grid = copy.deepcopy(lot.gameState.grid)
                    new_cars = copy.deepcopy(lot.gameState.Cars)

                    old_FrontPos = copy.deepcopy(new_cars[carBuffer].frontPos)

                    new_cars[carBuffer].backPos[1] -= left_moveCount
                    new_cars[carBuffer].frontPos[1] -= left_moveCount
                    new_cars[carBuffer].fuel -= left_moveCount

                    nbrOfStates += 1

                    charBuffer = carBuffer

                    for l in range(old_FrontPos[1] - new_cars[carBuffer].backPos[1] + 1):

                        if l == new_cars[carBuffer].length:
                            charBuffer = "."

                        new_grid[i][l + new_cars[carBuffer].backPos[1] - 1] = charBuffer

                    listOfStates.append(State(new_grid, new_cars, nbrOfStates-1, lot.gameState.index, lot.gameState.g+1, 0, 0, 0, 0, "left", left_moveCount, carBuffer)) #Creates a new State for a possible left move
                    left_moveCount -= 1

            if lot.gameState.grid[i][j] != "." and lot.gameState.grid[i][j] != carBuffer:

                left_moveCount = 0
                carBuffer = ""

    carChecked = []

    for i in range(6): #Second for loop checks for Vertical moves

        left_moveCount = 0
        right_moveCount = 0
        carBuffer = ""

        j_ = 5

        for j in range(6):

            if lot.gameState.grid[j_][i] == ".":
                left_moveCount += 1
                if carBuffer != "":

                    right_moveCount += 1
                    new_grid = copy.deepcopy(lot.gameState.grid)
                    new_cars = copy.deepcopy(lot.gameState.Cars)

                    old_frontPos = copy.deepcopy(new_cars[carBuffer].frontPos)

                    new_cars[carBuffer].backPos[0] -= right_moveCount
                    new_cars[carBuffer].frontPos[0] -= right_moveCount
                    new_cars[carBuffer].fuel -= right_moveCount

                    nbrOfStates += 1

                    charBuffer = "."

                    for k in range(old_frontPos[0] - new_cars[carBuffer].backPos[0] + 1):

                        if k == right_moveCount:
                            charBuffer = carBuffer

                        new_grid[old_frontPos[0] - k - 1][i] = charBuffer

                    listOfStates.append(State(new_grid, new_cars, nbrOfStates-1, lot.gameState.index, lot.gameState.g+1, 0, 0, 0, 0, "up", right_moveCount, carBuffer )) #Creates a State for an upwards move



            if lot.gameState.grid[j_][i] != "." and lot.gameState.grid[j_][i] not in carChecked:

                car = lot.gameState.Cars[lot.gameState.grid[j_][i]]
                carBuffer = car.letter
                carChecked.append(carBuffer)
                right_moveCount = 0

                if car.direction == "Horizontal" or car.fuel == 0:

                    left_moveCount = 0
                    carBuffer = ""

                    j_ -= 1

                    continue

                for k in range(left_moveCount):

                    new_grid = copy.deepcopy(lot.gameState.grid)
                    new_cars = copy.deepcopy(lot.gameState.Cars)

                    old_backPos = copy.deepcopy(new_cars[carBuffer].backPos)

                    new_cars[carBuffer].backPos[0] += left_moveCount
                    new_cars[carBuffer].frontPos[0] += left_moveCount
                    new_cars[carBuffer].fuel -= left_moveCount

                    nbrOfStates += 1

                    charBuffer = carBuffer

                    for l in range(new_cars[carBuffer].frontPos[0] - old_backPos[0] + 1):

                        if l == new_cars[carBuffer].length:
                            charBuffer = "."

                        new_grid[new_cars[carBuffer].frontPos[0] - l - 1][i] = charBuffer

                    listOfStates.append(State(new_grid, new_cars, nbrOfStates-1, lot.gameState.index, lot.gameState.g+1, 0, 0, 0, 0, "down", left_moveCount, carBuffer)) #Creates a State for a downwards move
                    left_moveCount -= 1

            if lot.gameState.grid[j_][i] != "." and lot.gameState.grid[j_][i] != carBuffer:

                left_moveCount = 0
                carBuffer = ""

            j_ -= 1

    return listOfStates

def mainLoop():
    # input

    readInput()
    global nbrOfStates

    # mainloop
    obj_og = ParkingLot()

    for i in range(nbrOfIterations):

        nbrOfStates = 0

        obj_og.gridInit()

        temp_Grid = copy.deepcopy(obj_og.gameState.grid)

        print("ORIGINAL" + str(obj_og))

        #Greedy Best First Search - All 4 heuristics

        firstSearch = gbfs(obj_og, 1) #heuristic 1

        print("Time Taken gbfs_h1: ")
        print(firstSearch[3])
        print(firstSearch[0])

        obj_og.reset(temp_Grid)
        nbrOfStates = 0
        firstSearch = gbfs(obj_og, 2) #heuristic 2

        print("Time Taken gbfs_h2: ")
        print(firstSearch[3])
        print(firstSearch[0])


        obj_og.reset(temp_Grid)
        nbrOfStates = 0
        firstSearch = gbfs(obj_og, 3) #heuristic 3

        print("Time Taken gbfs_h3: ")
        print(firstSearch[3])
        print(firstSearch[0])

        obj_og.reset(temp_Grid)
        nbrOfStates = 0

        firstSearch = gbfs(obj_og, 4) #heuristic 4

        print("Time Taken gbfs_h4: ")
        print(firstSearch[3])
        print(firstSearch[0])

        #A/A* algo - All 4 heuristics

        obj_og.reset(temp_Grid)
        nbrOfStates = 0
        firstSearch = a(obj_og, 1) #heuristic 1

        print("Time Taken a_h1: ")
        print(firstSearch[3])
        print(firstSearch[0])

        obj_og.reset(temp_Grid)
        nbrOfStates = 0
        firstSearch = a(obj_og, 2) #heuristic 2

        print("Time Taken a_h2: ")
        print(firstSearch[3])
        print(firstSearch[0])


        obj_og.reset(temp_Grid)
        nbrOfStates = 0
        firstSearch = a(obj_og, 3) #heuristic 3

        print("Time Taken a_h3: ")
        print(firstSearch[3])
        print(firstSearch[0])

        obj_og.reset(temp_Grid)
        nbrOfStates = 0

        firstSearch = a(obj_og, 4) #heuristic 4

        print("Time Taken a_h4: ")
        print(firstSearch[3])
        print(firstSearch[0])

        #Uniform Cost Search Algo

        obj_og.reset(temp_Grid)
        nbrOfStates = 0

        firstSearch = ucs(obj_og)

        print("Time Taken UCS: ")
        print(firstSearch[3])
        print(firstSearch[0])



def a(lot, heuristicNumber):
    # start timer
    start_time = time.time()
    root = lot
    goalState = 0

    closed = []  # create a closed list
    open_ = []  # ascending order PQ

    endSuffering = False

    # Will always return a heuristic value
    if heuristicNumber == 1:
        lot.gameState.h1 = heuristic.h1(lot.gameState)
    elif heuristicNumber == 2:
        lot.gameState.h2 = heuristic.h2(lot.gameState)
    elif heuristicNumber == 3:
        lot.gameState.h3 = heuristic.h3(lot.gameState)
    elif heuristicNumber == 4:
        lot.gameState.h4 = heuristic.h4(lot.gameState)

    heapq.heapify(open_)

    heapq.heappush(open_, lot.gameState)  # current state is opened

    # while Open isn't empty
    while open_:

        lot.gameState.copy_constructor(lot.gameState, heapq.heappop(open_))  # Lowest heuristic state, but there could be more.

        closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4, lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))  # update closed, goal not reached

        children = PossibleMoves(lot)  # get children

        # loop through children of current game state
        for child in children:

            # check if children in open or closed

            if child in closed or child in open_:
                continue  # skip, coz already in closed or open

            if "A" not in child.Cars:
                goalState = child

                lot.gameState.copy_constructor(lot.gameState, child)

                closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4, lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))

                endSuffering = True

                break  # REACHED GOAL, exit loop, current is the goal state!

            # print(child)

            # add children in open
            if heuristicNumber == 1:
                child.h1 = heuristic.h1(child)
                child.algo = "a_h1"
            elif heuristicNumber == 2:
                child.h2 = heuristic.h2(child)
                child.algo = "a_h2"
            elif heuristicNumber == 3:
                child.h3 = heuristic.h3(child)
                child.algo = "a_h3"
            elif heuristicNumber == 4:
                child.h4 = heuristic.h4(child)
                child.algo = "a_h4"

            heapq.heappush(open_, child)

        if endSuffering or nbrOfStates > 50000:
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    # output.output(heuristicNumber, root, elapsed_time, open_, closed, goalState)

    return [lot, closed, open_, elapsed_time]


def gbfs(lot, heuristicNumber):
    # start timer
    start_time = time.time()
    root = lot
    goalState = 0

    closed = []  # create a closed list
    open_ = []  # ascending order PQ

    endSuffering = False


    # Will always return a heuristic value
    if heuristicNumber == 1:
        lot.gameState.h1 = heuristic.h1(lot.gameState)
    elif heuristicNumber == 2:
        lot.gameState.h2 = heuristic.h2(lot.gameState)
    elif heuristicNumber == 3:
        lot.gameState.h3 = heuristic.h3(lot.gameState)
    elif heuristicNumber == 4:
        lot.gameState.h4 = heuristic.h4(lot.gameState)

    heapq.heapify(open_)

    heapq.heappush(open_, lot.gameState) # current state is opened

    k = 0

    # while Open isn't empty
    while open_:

        lot.gameState.copy_constructor(lot.gameState, heapq.heappop(open_)) # Lowest heuristic state, but there could be more.

        closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4,lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))  # update closed, goal not reached

        children = PossibleMoves(lot)  # get children

        # loop through children of current game state
        for child in children:

            # check if children in open or closed

            if child in closed or child in open_:
                continue  # skip, coz already in closed or open

            if "A" not in child.Cars:
                goalState = child

                lot.gameState.copy_constructor(lot.gameState, child)

                closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4,lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))

                endSuffering = True

                break  # REACHED GOAL, exit loop, current is the goal state!

            # print(child)

            # add children in open
            if heuristicNumber == 1:
                child.h1 = heuristic.h1(child)
                child.algo = "gbfs_h1"
            elif heuristicNumber == 2:
                child.h2 = heuristic.h2(child)
                child.algo = "gbfs_h2"
            elif heuristicNumber == 3:
                child.h3 = heuristic.h3(child)
                child.algo = "gbfs_h3"
            elif heuristicNumber == 4:
                child.h4 = heuristic.h4(child)
                child.algo = "gbfs_h4"

            heapq.heappush(open_, child)

        if endSuffering or nbrOfStates > 50000:
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    # output.output(heuristicNumber, root, elapsed_time, open_, closed, goalState)

    return [lot, closed, open_, elapsed_time]

def ucs(lot):
    # start timer
    start_time = time.time()
    root = lot
    goalState = 0

    closed = []  # create a closed list
    open_ = []  # ascending order PQ

    endSuffering = False

    heapq.heapify(open_)

    heapq.heappush(open_, lot.gameState) # current state is opened

    # while Open isn't empty
    while open_:

        lot.gameState.copy_constructor(lot.gameState, heapq.heappop(open_)) # Lowest cost 

        closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4, lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))  # update closed, goal not reached

        children = PossibleMoves(lot)  # get children

        # loop through children of current game state
        for child in children:

            # check if children in open or closed

            if child in closed or child in open_:
                continue  # skip, because it's already in closed or open

            if "A" not in child.Cars:
                goalState = child

                lot.gameState.copy_constructor(lot.gameState, child)

                closed.append(State(copy.deepcopy(lot.gameState.grid), copy.deepcopy(lot.gameState.Cars), lot.gameState.index, lot.gameState.parentGrid_index, lot.gameState.g, lot.gameState.h1, lot.gameState.h2, lot.gameState.h3, lot.gameState.h4, lot.gameState.moveDir, lot.gameState.moveCount, lot.gameState.moveLetter))

                endSuffering = True

                break  # REACHED GOAL, exit loop, current is the goal state!


            child.algo = "ucs"

            heapq.heappush(open_, child)

        if endSuffering or nbrOfStates > 50000:
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    # output.output(heuristicNumber, root, elapsed_time, open_, closed, goalState)

    return [lot, closed, open_, elapsed_time]




mainLoop()


