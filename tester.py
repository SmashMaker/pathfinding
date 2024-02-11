import Grid
import BFS,DFS,Astar,Dijkstra
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


"""
Test algorithms with all the test_maze
Organized in 3 levels (simple, normal, hard)
"""
mazes = {
    "Simple": test_maze.simple_mazes,
    "Normal": test_maze.normal_mazes,
    "Hard": test_maze.hard_mazes,
    "Impossible": test_maze.impossible_mazes,
    "Complex" : test_maze.complex_mazes
}

algoritms_to_test = {
    "BFS": BFS.solve,
    "DFS": DFS.solve,
    "Astar": Astar.solve,
    "Dijkstra": Dijkstra.solve
}

print("Testing mazes")

for algoritm in algoritms_to_test:
    print(f"\nTesting {algoritm} : ")
    all_passed = True

    for level in mazes:
        passed = True

        for key in mazes[level].keys():
            # Load the maze
            grid = mazes[level][key]["grid"]
            path = mazes[level][key]["way"]

            mazeobj = Grid.Grid(grid, possible_cases)

            # Run the algoritm
            result = algoritms_to_test[algoritm](mazeobj)

            # Check if the result is correct
            if result != path:
                print(key,result, path)
                passed = False
                all_passed = False

        if passed:
            print(f"\t{level} : Passed")
        else:
            print(f"\t{level} : Failed")

    if all_passed:
        print(f"✅ {algoritm} passed ✅")
    else:
        print(f"❌ {algoritm} failed at least one test ❌")