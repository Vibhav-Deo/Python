from stackfrontier import StackFrontier
from node import Node

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Multiple starting points found, please ensure there is only 1 starting point")

        if contents.count("B") != 1:
            raise Exception("Multiple end points found, please ensure there is only 1 end point")

        contents = contents.splitlines()

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []

        for row in range(self.height):
            wall_tracker = []
            for column in range(self.width):
                try:
                    if contents[row][column] == "A":
                        self.start = (row, column)
                        wall_tracker.append(False)
                    elif contents[row][column] == "B":
                        self.goal = (row, column)
                        wall_tracker.append(False)
                    elif contents[row][column] == " ":
                        wall_tracker.append(False)
                    else:
                        wall_tracker.append(True)
                except IndexError:
                    wall_tracker.append(False)
            self.walls.append(wall_tracker)

        self.solution = None

    def print(self):
        result = self.solution[1] if self.solution is not None and len(self.solution) > 1 else None
        print()
        for rowindex, row in enumerate(self.walls):
            for columnindex, column in enumerate(row):
                if column:
                    print("|__|", end="")
                elif (rowindex, columnindex) == self.start:
                    print("START", end="")
                elif (rowindex, columnindex) == self.goal:
                    print("FINISH", end="")
                elif result is not None and (rowindex, columnindex) in result:
                    print("->", end="")
                else:
                    print("PATH", end="")
            print()
        print()

    def calculate_neighbours(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = [];
        for action, (row, col) in candidates:
            if 0 <= row < self.height and 0<= col < self.width and not self.walls[row][col]:
                result.append((action, (row, col)))
        
        return result

    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)

        frontier = StackFrontier()
        frontier.add(start)
        self.explored = set()

        while True:

            if frontier.is_empty():
                raise Exception("No solution exists")
            
            node = frontier.remove()
            self.num_explored +=1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.calculate_neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for rowindex, row in enumerate(self.walls):
            for columnindex, column in enumerate(row):

                               # Walls
                if column:
                    fill = (40, 40, 40)

                # Start
                elif (rowindex, columnindex) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (rowindex, columnindex) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (rowindex, columnindex) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (rowindex, columnindex) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(columnindex * cell_size + cell_border, rowindex * cell_size + cell_border),
                      ((columnindex + 1) * cell_size - cell_border, (rowindex + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)
