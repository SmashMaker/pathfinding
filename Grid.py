class Grid:
    def __init__(self, grid, possible_cases):

        self.grid = grid.copy()

        # Check if array is 2D
        if not self.checkIfGridIs2D():
            raise Exception("Grid must be a 2D array")

        self.height = len(self.grid)
        self.width= len(self.grid[0])
        self.possible_cases = possible_cases

        # All check
        self.checkForInit()


    # All checks in the init function
    def checkForInit(self):

        checktoDo = [
            # [function, error message]
            [self.checkIfGridIs2D, "Grid must be a 2D array"],
            [self.checkIfGridIsRectangle, "Grid must be a rectangle"],
            [self.checkIfGridContainPossibleCases, "Grid must contain possible cases"]
        ]

        checktoReturn = True
        errortoReturn = ""

        for check in checktoDo:
            if not check[0]():
                checktoReturn = False
                errortoReturn += check[1] + "\n"

        if not checktoReturn:
            raise Exception(errortoReturn)

        return checktoReturn

    def checkIfGridIsRectangle(self):
        return all(len(x) == self.width for x in self.grid)

    def checkIfGridContainPossibleCases(self):
        temp_grid = [item for sublist in self.grid for item in sublist]
        return all(x in self.possible_cases.values() for x in temp_grid)

    def checkIfGridIs2D(self):
        return all(isinstance(x, list) for x in self.grid)

    def printGrid(self, grid_to_print=None):

        if grid_to_print is None:
            grid_to_print = self.grid


        number_to_emoji = {
            -1: "🟫",
            0: "⬜",
            1: "⬛",
            2: "🟢",
            3: "🔴",
            4: "🟠",
            5: "🟡",
            6: "🟣"
        }

        for line in grid_to_print:
            print("".join([number_to_emoji[x] for x in line]))

    def getCase(self, x, y):
        return self.grid[y][x]

    def setCase(self, x, y, casetoset):
        if not isinstance(casetoset, int):
            casetoset = self.possible_cases[casetoset]
        self.grid[y][x] = casetoset

    def findCase(self, casetofind):
        if not isinstance(casetofind, int):
            casetofind = self.possible_cases[casetofind]

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == casetofind:
                    return [x, y]

        return None

    def printGridWithPath(self, path):
        copy_grid = [x.copy() for x in self.grid]
        for location in path:
            copy_grid[location[1]][location[0]] = self.possible_cases["path cell"]
        self.printGrid(copy_grid)
