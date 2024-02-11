import os
import time

import Grid
import BFS, DFS, Astar, Dijkstra
import Generator_labyrinthes, Generator_open_spaces, Generator_close_spaces

possible_cases = {
    "Indestructible wall": -1,
    "empty cell": 0,
    "wall": 1,
    "start": 2,
    "end": 3,
    "visited cell": 4,
    "path cell": 5,
    "current cell": 6
}

algoritms_to_test = {
    "BFS": BFS.solve,
    "DFS": DFS.solve,
    "Astar": Astar.solve,
    "Dijkstra": Dijkstra.solve
}

generator_to_use = {
    "labyrinthes": Generator_labyrinthes.create_maze,
    "open_spaces": Generator_open_spaces.create_open_space,
    "close_spaces": Generator_close_spaces.create_close_space
} # They all return a 2D array that we need to convert to a Grid object later

size_spaces = {
    "labyrinthes": {
        "simple": (30,30),
        "normal": (80,80),
        "hard": (150,150)
    },
    "open_spaces": {
        "simple": (30,30),
        "normal": (80,80),
        "hard": (150,150)
    },
    "close_spaces": {
        "simple": (30,30),
        "normal": (80,80),
        "hard": (150,150)
    }
}



def save_2D_array_to_file(array, file_name):
    with open(file_name, "w") as file:
        for line in array:
            for element in line:
                file.write(str(element))
            file.write("\n")

def import_2D_array_from_file(file_name):
    with open(file_name, "r") as file:
        array = []
        for line in file:
            array.append([int(char) for char in line if char != "\n"])
    return array

def generate_x_spaces(nb_spaces, size, generator_func, path_directory):
    for i in range(nb_spaces):
        space = generator_func(size[0], size[1])
        save_2D_array_to_file(space, path_directory + "space_" + str(i) + ".txt")
    return True
"""
path_directory = "saved_spaces/"

parameters = size_spaces["labyrinthes"]["simple"]
maze_to_save = generator_to_use["labyrinthes"](parameters[0], parameters[1], make_complex=False)
maze = Grid.Grid(maze_to_save, possible_cases)
maze.printGrid()

save_2D_array_to_file(maze_to_save, path_directory + "labyrinthes_simple.txt")

imported_maze = import_2D_array_from_file(path_directory + "labyrinthes_simple.txt")
maze = Grid.Grid(imported_maze, possible_cases)
maze.printGrid()

# Generate 10 simple labyrinthes
path_directory = "saved_spaces/"
generate_x_spaces(10, size_spaces["labyrinthes"]["simple"], generator_to_use["labyrinthes"], path_directory)
"""
"""
# Generate all the spaces
print("Generating all the spaces")
for space_type in generator_to_use:
    print("\tGenerating " + space_type + " spaces", end="")
    timer = time.time()
    for size in size_spaces[space_type]:
        path_directory = "saved_spaces/" + space_type + "/" + size + "/"

        #Check if the directory exists
        if not os.path.exists(path_directory):
            os.makedirs(path_directory)
        else:
            # If it exists, we remove all the files in it
            for file in os.listdir(path_directory):
                os.remove(path_directory + file)

        generate_x_spaces(nb_spaces, size_spaces[space_type][size], generator_to_use[space_type], path_directory)
    print(" in " + str(round(time.time() - timer,1)) + " seconds")

print("All the spaces have been generated and saved")
"""

def generate_all(generators_to_use, size_spaces, nb_spaces):
    print("Generating all the spaces")
    for space_type in generators_to_use:
        print("\tGenerating " + space_type + " spaces", end="")
        timer = time.time()
        for size in size_spaces[space_type]:
            path_directory = "saved_spaces/" + space_type + "/" + size + "/"

            #Check if the directory exists
            if not os.path.exists(path_directory):
                os.makedirs(path_directory)
            else:
                # If it exists, we remove all the files in it
                for file in os.listdir(path_directory):
                    os.remove(path_directory + file)

            generate_x_spaces(nb_spaces, size_spaces[space_type][size], generators_to_use[space_type], path_directory)
        print(" in " + str(round(time.time() - timer,1)) + " seconds")

    print("All the spaces have been generated and saved\n")

    return True


def get_stats_from_grid(mazeobj):
    nb_path_cells = 0
    nb_visited_cells = 0
    nb_total_usable_cells = 0

    for line in mazeobj.grid:
        for cell in line:
            if cell == mazeobj.possible_cases["path cell"]:
                nb_path_cells += 1
                nb_visited_cells += 1
                nb_total_usable_cells += 1
            elif cell == mazeobj.possible_cases["visited cell"]:
                nb_visited_cells += 1
                nb_total_usable_cells += 1
            elif cell == mazeobj.possible_cases["empty cell"]:
                nb_total_usable_cells += 1

    return nb_path_cells, nb_visited_cells, nb_total_usable_cells

def test_one_algorithm(algorithm, mazeobjoriginal):
    timer = time.time()
    mazeobj = mazeobjoriginal.copy()
    path, mazeobj = algorithm(mazeobj)

    nb_path_cells, nb_visited_cells, nb_total_usable_cells = get_stats_from_grid(mazeobj)
    timer = time.time() - timer

    return timer, nb_path_cells, nb_visited_cells, nb_total_usable_cells

def test_all(algorithms, mazeobjoriginal):
    results = {}
    for algorithm in algorithms:
        results[algorithm] = test_one_algorithm(algorithms[algorithm], mazeobjoriginal)
    return results



"""maze = import_2D_array_from_file("saved_spaces/close_spaces/hard/space_0.txt")
mazeobj = Grid.Grid(maze, possible_cases)
mazeobj.printGrid()"""

#print(test_all(algoritms_to_test, mazeobj))



def add_results_csv(results, file_name):
    # Result is a tuple with (category, difficulty, results)
    with open(file_name, "a") as file:
        for item in results:
            if type(item) == dict:
                # Don't care about the key, just the values
                for key in item:
                    values = item[key]
                    for value in values:
                        file.write(str(value) + ",")
            else:
                file.write(item + ",")
        file.write("\n")

"""
# Test all the algorithms in the folder (go through all the files)
base_folder = "saved_spaces\\"

# Get all directories in the base folder
categories_dirs = [f.path for f in os.scandir(base_folder) if f.is_dir()]

if os.path.exists("results.csv"):
    os.remove("results.csv")

with open("results.csv", "w") as file:
    file.write("Category,Difficulty,BFS Time,BFS Path cells,BFS Visited cells,BFS Total usable cells,DFS Time,DFS Path cells,DFS Visited cells,DFS Total usable cells,Astar Time,Astar Path cells,Astar Visited cells,Astar Total usable cells,Dijkstra Time,Dijkstra Path cells,Dijkstra Visited cells,Dijkstra Total usable cells\n")

print("Testing all the spaces")
all_timer = time.time()

for category_dir in categories_dirs:
    # Get difficulties
    difficulties_dir = [f.path for f in os.scandir(category_dir) if f.is_dir()]

    # Get the category name
    category = category_dir.split("\\")[-1]

    for difficulty_dir in difficulties_dir:
        # Get the difficulty name
        difficulty = difficulty_dir.split("\\")[-1]

        print(f"\tTesting {category} {difficulty}")

        # Get all the grids in the difficulty folder
        grids_files = [f.path for f in os.scandir(difficulty_dir) if f.is_file()]

        for grid_file in grids_files:
            # Get the grid
            grid = import_2D_array_from_file(grid_file)
            gridobj = Grid.Grid(grid, possible_cases)

            # Test all the algorithms
            results = test_all(algoritms_to_test, gridobj)

            # Save the results in a csv file
            add_results_csv((category, difficulty, results), "results.csv")

print("All the tests have been done in " + str(round(time.time() - all_timer, 1)) + " seconds")"""

def process_and_save_all_results(algoritms_to_test, possible_cases, base_folder="saved_spaces\\", save_file="results.csv"):
    if os.path.exists(save_file):
        os.remove(save_file)

    with open(save_file, "w") as file:
        file.write(
            "Category,Difficulty,BFS Time,BFS Path cells,BFS Visited cells,BFS Total usable cells,DFS Time,DFS Path cells,DFS Visited cells,DFS Total usable cells,Astar Time,Astar Path cells,Astar Visited cells,Astar Total usable cells,Dijkstra Time,Dijkstra Path cells,Dijkstra Visited cells,Dijkstra Total usable cells\n")

    categories_dirs = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    print("Testing all the spaces")
    all_timer = time.time()

    for category_dir in categories_dirs:
        # Get difficulties
        difficulties_dir = [f.path for f in os.scandir(category_dir) if f.is_dir()]

        # Get the category name
        category = category_dir.split("\\")[-1]

        for difficulty_dir in difficulties_dir:
            # Get the difficulty name
            difficulty = difficulty_dir.split("\\")[-1]

            print(f"\tTesting {category} {difficulty}")

            # Get all the grids in the difficulty folder
            grids_files = [f.path for f in os.scandir(difficulty_dir) if f.is_file()]

            for grid_file in grids_files:
                # Get the grid
                grid = import_2D_array_from_file(grid_file)
                gridobj = Grid.Grid(grid, possible_cases)

                # Test all the algorithms
                results = test_all(algoritms_to_test, gridobj)

                # Save the results in a csv file
                add_results_csv((category, difficulty, results), "results.csv")

    print("All the tests have been done in " + str(round(time.time() - all_timer, 1)) + " seconds")


nb_spaces = 10

#generate_all(generator_to_use, size_spaces, nb_spaces)

#process_and_save_all_results(algoritms_to_test, possible_cases, base_folder="saved_spaces\\", save_file="results.csv")

# PROCESS THE RESULTS
# Get the average values for each category and difficulty for each algorithm
counter = {
    "BFS": [],
    "DFS": [],
    "Astar": [],
    "Dijkstra": []
}
categories = ["labyrinthes", "open_spaces", "close_spaces"]
difficulties = ["simple", "normal", "hard"]

with open("backup_results.csv", "r") as file:
    for line in file:
        line = line.split(",")

        if line[0] == "Category":
            continue

        line = line[:-1] if line[-1] == "\n" else line
        category = line.pop(0)
        difficulty = line.pop(0)

        # Algorithm index is 0:4 (BFS), 4:8 (DFS), 8:12 (Astar), 12:16 (Dijkstra)
        for i in range(4):
            counter[list(algoritms_to_test.keys())[i]].append([category, difficulty, line[i*4:i*4+4]])

# Print dict
for key in counter:
    print(key)
    for item in counter[key]:
        print("\t",item)

    print(len(counter[key]))



def get_average(results):
    average = [0,0,0,0]
    for item in results:
        for i in range(4):
            average[i] += float(item[i])
    for i in range(4):
        average[i] /= len(results)
    return average


def get_stats(counter, choosed_algorithm, choosed_category, choosed_difficulty):
    results = []
    for item in counter[choosed_algorithm]:
        if item[0] == choosed_category and item[1] == choosed_difficulty:
            results.append(item[2])

    return get_average(results)

stats = get_stats(counter, "BFS", "labyrinthes", "simple")
print(stats)

def get_all_stats(counter, choosed_algorithm):
    stats = {}
    for category in categories:
        stats[category] = {}
        for difficulty in difficulties:
            stats[category][difficulty] = get_stats(counter, choosed_algorithm, category, difficulty)
    return stats

stats_BFS = get_all_stats(counter, "BFS")
stats_DFS = get_all_stats(counter, "DFS")
stats_Astar = get_all_stats(counter, "Astar")
stats_Dijkstra = get_all_stats(counter, "Dijkstra")

# Save all the stats in a csv file
with open("stats.csv", "w") as file:
    file.write("Category,Difficulty,BFS Time,BFS Path cells,BFS Visited cells,BFS Total usable cells,DFS Time,DFS Path cells,DFS Visited cells,DFS Total usable cells,Astar Time,Astar Path cells,Astar Visited cells,Astar Total usable cells,Dijkstra Time,Dijkstra Path cells,Dijkstra Visited cells,Dijkstra Total usable cells\n")

    for category in categories:
        for difficulty in difficulties:
            file.write(category + "," + difficulty + ",")
            for i in range(4):
                file.write(str(stats_BFS[category][difficulty][i]) + ",")
            for i in range(4):
                file.write(str(stats_DFS[category][difficulty][i]) + ",")
            for i in range(4):
                file.write(str(stats_Astar[category][difficulty][i]) + ",")
            for i in range(4):
                file.write(str(stats_Dijkstra[category][difficulty][i]) + ",")
            file.write("\n")


