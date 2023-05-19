def output(heuristicNumber, root, elapsed_time, open_, closed, goalState):
    # before returning, I can ouput the stuff the teacher wants

    # Output
    file = open("gbfs-" + str(heuristicNumber) + "sol-" + str(1) + ".txt", "w")

    rootString = ''.join([item for sublist in root.gameState.grid for item in sublist])
    file.write("--------------------------------------------------------------------------------\n")
    file.write('Inital board configuration: ' + rootString + "\n\n")
    for el in root.gameState.grid:
        file.write(''.join([str(item) for item in el]) + "\n")
    file.write("\n\n")

    print("testse", root.gameState.Cars["B"].fuel)
    carFuelString = ""
    for car in root.gameState.Cars:
        letter = car
        fuel = str(root.gameState.Cars[car].fuel)
        carFuelString += letter + ": " + fuel + " "
    file.write("Car fuel available: " + carFuelString + "\n")
    file.write("Runtime: " + str(round(elapsed_time, 5)) + "seconds\n")
    file.write("Search path length: " + str(len(open_ + closed)) + "\n")

    # YOU ARE HERE CHRISTIAN
    # print("goal", goalState.parentGrid_index)
    print(closed)
    solutionPathState = []
    solutionPathMove = []

    for el in closed:
        if goalState.parentGrid_index == el.index:
            solutionPathState.append(el)

    file.write("Solution path length: " + str(len(solutionPathState)) + "\n")
    file.write("Solution path:" + "answer\n")

    for el in solutionPathState:
        stateGridString = ''.join([item for sublist in el.grid for item in sublist])
        stateMoveString = "" #need to do the moves
        file.write(stateMoveString, stateGridString)


    file.write("\n\n")

    for el in closed[0].grid:
        file.write(''.join([str(item) for item in el]) + "\n")
    file.write("\n\n")

    file.close()

    