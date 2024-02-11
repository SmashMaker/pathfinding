import Grid
import random
def solve(gridobjoriginal: Grid, step_by_step = False):

    gridobj = gridobjoriginal.copy()

    """
    if step_by_step:
        paths = []
    """

    start = gridobj.findCase("start")
    end = gridobj.findCase("end")

    current = start
    path = [current]

    # Get useless neighbors
    useless_neighbors = ["Indescructible wall", "visited cell", "path cell", "wall"]
    for key in useless_neighbors:
        useless_neighbors[useless_neighbors.index(key)] = gridobj.possible_cases[key]

    is_searching = True
    while is_searching:
        """
        # Store the path if needed
        if step_by_step:
            paths.append(path)
            paths[-1].append(current)
        """

        # Get neighbors coordinates and cases types
        neighbors_without_info = gridobj.getNeighbors(current[0], current[1])

        neighbors = [] # [x, y, case_type]
        for neighbor in neighbors_without_info:
            neighbors.append([neighbor[0], neighbor[1], gridobj.getCase(neighbor[0], neighbor[1])])

        # Check every neighbors
        possible_way = []
        for neighbor in neighbors:
            # If the neighbor is the end, we stop the search
            if neighbor[2] == gridobj.possible_cases["end"]:
                possible_way = [neighbor]
                is_searching = False
                break

            # If the neighbor is not useless, we add it to the possible way
            if not neighbor[2] in useless_neighbors:
                possible_way.append(neighbor)

        # Act depending on the number of possible way
        nb_possible_way = len(possible_way)

        # If there is no possible way, we go back
        if nb_possible_way == 0:
            gridobj.setCase(current[0], current[1], "visited cell")
            path.pop()

            if path == []:
                return None

            current = path[-1]
            gridobj.setCase(current[0], current[1], "current cell")

            continue

        # Pick a possible way (randomly if there is more than one)
        if nb_possible_way == 1:
            chosen_way = possible_way[0]
        else:
            chosen_way = random.choice(possible_way)

        # Walk to the next cell
        gridobj.setCase(current[0], current[1], "path cell")
        current = (chosen_way[0], chosen_way[1])
        path.append(current)
        gridobj.setCase(current[0], current[1], "current cell")
    return path


