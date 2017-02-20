# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We use constraint propagation to check peers of all the items in a sudoku matrix to see if any of their same row or same column peers have the same value as the original box (and the value of each naked twin should have only a length of 2). Constraint propagation is used to apply a specific condition until a solution is achieved, or the problem set cannot be narrowed down anymore. By narrowing down to either the same row or column, we are able to solely look at the same row or same column to eliminate any values from that row / column which cannot contain the values of the naked twins (since each of the naked twins will one of those two values). 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We add the two sudoku diagonals to the unitlist as additional constraits to the original sudoku solver. This ensures that everytime we use eliminate and only_choice, the diagonals are now part of the peers so that we can verify that 1-9 shows up exactly once on the diagonals in addition to all the other conditions for regular sudoku. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.