# Artificial-Intelligence-Term-Project

This project was crafted for Concordia Comp-472 (Artificial Intelligence), and was made alongside 2 other teammates. It aims at being able to solve the board game/puzzle game by the name of "Rush Hour". This game is set in a parking lot where cars have to move back and forth until enough is space is made for the ambulance car (a.k.a. red car) to see its way to the exit.

## Rules

- A car can occupy and move to any free space, be it that there is not another car blocking its way to it.

- Cars facing vertically can only move, up and down, along that column, and vice versa, cars facing horizontally can only move, right or left, along their row.

- Cars have a set amount of fuel (100 by default), and if it runs out, then they can't move any longer. Also, for every point on the grid that a car moves through, it loses 1 fuel.

- Once the **A** car makes its way to the exit, coordinate [3,6], then the "Rush Hour" grid is considered solved and the game finishes.  

## How to Run

To run this "Rush Hour" solver, if on Windows, you can go ahead and double click on "traffic_game_solver.exe", else, you'd to have python installed on your system and compile main.py. Once the executable is run, then puzzles.txt is read and the solutions are created in a new folder called "output". For brevity's sake, puzzles.txt only has 2 puzzles. If you want more, you can check out !puzzles.txt, inside of the folder "my_output" and copy some over to puzzles.txt, or better yet, copy over the entire file, to the root directory of the project, whilst making sure !puzzles.txt is renamed as puzzles.txt. This effectively replaces one text file with the other. **Warning!** Running all of the puzzles may take upwards of 1 hour, to finish executing.

## Methodology

### Set-up

- The puzzles can be found in either puzzles.txt or !puzzles.txt, where the letters represent different cars, and the dots represent empty spaces. Altough they are written out linearly, one must picture them as a 6x6 grid, where each 6 characters form a new row. To clear up any confusions, you can open up the text file "Puzzle #1 a_h1".txt, and compare the original grid to the first puzzle inside !puzzles.txt, and you should see how they are the same grid. Aside from the starting grid, some puzzles have extra letters and numbers attached to the right hand side. Those represent different starting fuels for the cars mentioned. I.e. if you look at puzzle #4, inside of !puzzles.txt, J car will now start with 0 fuel, making it completly immobile, whilst B car will start with 4 fuel in reserve. This is in contrast to the other cars which will all start with 100 fuel.

- In total, there will be 9 different solutions to each puzzle that will be computed. Each of these solutions differ in algorithms/variations in algorithms which will be explained in the section below.

- The output can also show as there not being a solution that has been found. This will be the case in either scenario where 50,000 different unique moves have been observed without finding the set that leads to the goal, or where all possible moves have been exhausted without reaching the goal.

### Algorithms

There are a 3 different algorithms used to find the set of moves that lead to the A car exiting the parking lot: Uniform Cost Search (ucs), Greedy Best First Search (gbfs) and A/A*. Gbfs and a/a* both use the same 4 different heuristics, making 8 different algorithmic variations of those two algorithms. Ucs tends to be the slowest of the 3, as it uses no heuristics in its calculations, whilst gbfs seems to be the fastest at spewing out its results. 

## Acknowledgments

I would like to acknowledge both of my teammates: Tariq Benmouh and Christian Jerjian, who helped me in creating this project. The original github link can be found here: https://github.com/Tariq-B/MiniProject2