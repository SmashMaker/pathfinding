import Grid

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

def solve(gridobjoriginal: Grid, step_by_step=False):

    gridobj = gridobjoriginal.copy()

    start = gridobj.findCase("start")
    end = gridobj.findCase("end")

    current = start
    paths = [[current]]

    # Get useless neighbors (get their number)
    useless_neighbors = ["Indescructible wall", "visited cell", "path cell", "wall", "current cell", "start"]
    for key in useless_neighbors:
        useless_neighbors[useless_neighbors.index(key)] = gridobj.possible_cases[key]

    destroy_list = []

    is_searching = True
    while is_searching:
        # Destroy every path where there is no way
        if destroy_list:
            for i in sorted(destroy_list, reverse=True):
                paths.pop(i)
            destroy_list = []

        # Check every paths
        new_paths = []
        for index_path, path in enumerate(paths):
            current = path[-1]
            if current != start:
                gridobj.setCase(current[0], current[1], "visited cell")

            possible_way = get_neighbors_informations(gridobj, current, useless_neighbors)

            # Check if end
            for neighbor in possible_way:
                if neighbor[2] == gridobj.possible_cases["end"]:
                    is_searching = False
                    path.append((neighbor[0], neighbor[1]))
                    return path, gridobj

            if not is_searching:
                break

            # Act depending on the number of possible ways
            nb_possible_way = len(possible_way)

            # If there is no way, we add to the destroy list
            if nb_possible_way == 0:
                destroy_list.append(index_path)

            elif nb_possible_way >= 1:
                for i, way in enumerate(possible_way):
                    new_current = (way[0], way[1])

                    # If there is one way, we take a step
                    if i == 0:  # Continue the original path
                        path.append(new_current)
                        gridobj.setCase(new_current[0], new_current[1], "current cell")

                    # If there is more than one, we split for every way and take a step
                    else:  # Créez de nouveaux chemins pour les autres possibilités
                        # Add the new path (split)
                        new_path = list(
                            path[:-1])
                        new_path.append(new_current)
                        new_paths.append(new_path)
                        gridobj.setCase(new_current[0], new_current[1], "current cell")

        paths.extend(new_paths)

        # Break if there are no paths left to explore
        if not paths:
            return None, gridobj
