import sys

from maze import Maze


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
m.solve()
m.output("maze.png", show_explored=True)