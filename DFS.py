import Grid
import random
import time

import test_maze
possible_cases = {
    "Indescructible wall": -1,
    "empty cell": 0,
    "wall": 1,
    "start": 2,
    "end": 3,
    "visited cell": 4,
    "path cell": 5,
    "current cell": 6
}


maze = Grid.Grid(test_maze.showcase_mazes, possible_cases)
current_position = maze.findCase("start")
path = [current_position]


# Get useless neighbors
useless_neighbors = ["Indescructible wall", "visited cell", "path cell", "wall"]
for key in useless_neighbors:
    useless_neighbors[useless_neighbors.index(key)] = possible_cases[key]
print(useless_neighbors)

is_searching = True
while is_searching :
    time.sleep(0.01)
    # Print the maze
    maze.printGrid()

    # Get neighbors coordinates and cases types
    neighbors_without_info = maze.getNeighbors(current_position[0], current_position[1])

    neighbors = [] # [x, y, case_type]
    for neighbor in neighbors_without_info:
        neighbors.append([neighbor[0], neighbor[1], maze.getCase(neighbor[0], neighbor[1])])


    possible_way = []
    # Check every neighbors
    for neighbor in neighbors:
        # If the neighbor is the end, we stop the search
        if neighbor[2] == possible_cases["end"]:
            print("End of the maze")
            possible_way = [neighbor]
            is_searching = False
            break

        # If the neighbor is not useless, we add it to the possible way
        if not neighbor[2] in useless_neighbors:
            possible_way.append(neighbor)


    # Act depending on the number of possible way
    nb_possible_way = len(possible_way)

    # If there is no possible way, we rollback to the previous cell
    if nb_possible_way == 0:
        # Set the current cell to visited cell
        maze.setCase(current_position[0], current_position[1], "visited cell")

        # Rollback to the last cell (path cell)
        # If there is no path cell, we stop the search
        if len(path) == 1:
            print("No way to the end of the maze")
            is_searching = False
            break
        path = path[:-1]
        current_position = path[-1]
        maze.setCase(current_position[0], current_position[1], "current cell")
        continue

    # Pick a possible way (randomly if there is more than one)
    if nb_possible_way == 1:
        chosen_way = possible_way[0]
    else:
        chosen_way = random.choice(possible_way)

    # Set the current cell to path cell
    maze.setCase(current_position[0], current_position[1], "path cell")
    path.append(chosen_way)

    # Set the chosen neighbor to current cell
    maze.setCase(chosen_way[0], chosen_way[1], "current cell")
    current_position = chosen_way

# Print the maze
    maze.printGrid()
    print("")
