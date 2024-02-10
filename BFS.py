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

def get_neighbors_informations(maze, current, useless_neighbors):
    # Get raw neighbors
    neighbors_without_info = maze.getNeighbors(current[0], current[1])

    # Get neighbors coordinates and cases types
    neighbors_with_uselees = [] # [x, y, case_type]
    for neighbor in neighbors_without_info:
        neighbors_with_uselees.append([neighbor[0], neighbor[1], maze.getCase(neighbor[0], neighbor[1])])

    # Remove useless neighbors
    neighbors = []
    for neighbor in neighbors_with_uselees:
        if not neighbor[2] in useless_neighbors:
            neighbors.append(neighbor)

    # [x, y, case_type]
    return neighbors

maze = Grid.Grid(test_maze.normal_mazes["normal_maze_1"]["grid"], possible_cases)
start = maze.findCase("start")
end = maze.findCase("end")

current = start
paths = [[current]]

# Get useless neighbors (get their number)
useless_neighbors = ["Indescructible wall", "visited cell", "path cell", "wall", "current cell","start"]
for key in useless_neighbors:
    useless_neighbors[useless_neighbors.index(key)] = maze.possible_cases[key]

destroy_list = []

is_searching = True
while is_searching:
    maze.printGrid()
    if destroy_list:
        for i in sorted(destroy_list, reverse=True):
            paths.pop(i)
        destroy_list = []

    new_paths = []
    for index_path, path in enumerate(paths):
        current = path[-1]
        # Avant de chercher de nouveaux voisins, marquez la cellule courante comme visitée s'il s'agit pas de la cellule de départ
        if current != start:
            maze.setCase(current[0], current[1], "visited cell")

        possible_way = get_neighbors_informations(maze, current, useless_neighbors)

        # Check if end
        for neighbor in possible_way:
            if neighbor[2] == maze.possible_cases["end"]:
                is_searching = False
                path.append((neighbor[0], neighbor[1]))
                print("Path to the end found!")
                break

        if not is_searching:
            break

        nb_possible_way = len(possible_way)
        if nb_possible_way == 0:
            destroy_list.append(index_path)
        elif nb_possible_way >= 1:
            for i, way in enumerate(possible_way):
                new_current = (way[0], way[1])
                if i == 0:  # Continue the original path
                    path.append(new_current)
                    # Marquez seulement la nouvelle cellule courante
                    maze.setCase(new_current[0], new_current[1], "current cell")
                else:  # Créez de nouveaux chemins pour les autres possibilités
                    new_path = list(
                        path[:-1])  # Excluez la cellule courante actuelle qui est déjà marquée comme visitée
                    new_path.append(new_current)
                    new_paths.append(new_path)
                    maze.setCase(new_current[0], new_current[1], "current cell")

    paths.extend(new_paths)  # Ajoutez les nouveaux chemins à la liste principale des chemins

    # Break if there are no paths left to explore
    if not paths:
        print("No path to the end exists.")
        break
