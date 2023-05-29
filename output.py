import os

moves = ""
counter = 0
def recursionMoves(state, closed):

    global moves
    global counter

    if state.parentGrid_index is not None:

        recursionMoves(closed[state.parentGrid_index], closed)

    if state.parentGrid_index is None:

        return None

    counter += 1

    if state.moveCount == 1:

        moves += "Move #" + str(counter) + ": Car " + state.moveLetter + " moved " + str(state.moveCount) + " time in the " + state.moveDir + " direction.\n\n"

    else :

        moves += "Move #" + str(counter) + ": Car " + state.moveLetter + " moved " + str(state.moveCount) + " times in the " + state.moveDir + " direction.\n\n"







puzzlenbr = 1
def out(lot, root, elapsed_time, open_, closed, isgreaterthan50k):

    global puzzlenbr

    if not os.path.isdir("output"):

        os.mkdir("output")

    if isgreaterthan50k and "A" in lot.gameState.Cars:

        file = open("output\\Puzzle #" + str(puzzlenbr) + " " + lot.gameState.algo + "--SOLUTION NOT FOUND.txt", "w")

        if lot.gameState.algo == "ucs":

            puzzlenbr += 1

        text = "Your Solution has not been found after an excess of 50000 different gamestates have been reached in trying to find it!\n\n Sorry!"

        file.write(text)

        return

    if not open_ and "A" in lot.gameState.Cars:

        file = open("output\\Puzzle #" + str(puzzlenbr) + " " + lot.gameState.algo + "--SOLUTION NOT FOUND.txt", "w")

        if lot.gameState.algo == "ucs":

            puzzlenbr += 1

        text = "Your Solution has not been found after all possible moves have been exhausted in trying to find it!\n\n Sorry!"

        file.write(text)

        return


    file = open("output\\Puzzle #" + str(puzzlenbr) + " " + lot.gameState.algo + ".txt", "w")

    if lot.gameState.algo == "ucs":

        puzzlenbr += 1

    text = "Orignal Puzzle GRID:\n\n" + str(root)

    text += "Moves that led to solution:\n\n"

    recursionMoves(lot.gameState, closed)

    global moves, counter

    text += moves + "\n"

    moves = ""
    counter = 0

    text += "Time Taken for " + lot.gameState.algo + ": " + str(elapsed_time) + "s\n\n"

    text += str(lot)

    file.write(text)

    