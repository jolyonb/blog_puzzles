"""
hashi.py

Solves a hashi puzzle, such as presented here:
https://www.puzzle-bridges.com/

File format:
The first block describes the grid as specified in the puzzle.
Allowed characters include 1-8 for islands and period (.) for empty cells.
All lines in the grid must have the same length.

After the grid, you can include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #) as well as
the following optional setting:
max_bridges=#
The default for this setting is 2.
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, buffer_grid

char_colors = {
    '1': Colors.YELLOW,
    '2': Colors.BLUE,
    '3': Colors.GREEN,
    '4': Colors.RED,
    '5': Colors.MAGENTA,
    '6': Colors.WHITE,
    '7': Colors.CYAN,
}

template = """
% Puzzle Definition
#const max_bridges={{ max_bridges }}.

% Islands
% island(col, row, #).
{% for row, col, num in islands %}
island({{ col }}, {{ row }}, {{ num }}).
{% endfor %}
"""


class Hashi(Puzzle):
    """
    Class to handle Hashi puzzles.
    """

    puzzletype = 'hashi'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.grid = None
        self.settings = None
        self.rows = None
        self.cols = None
        self.islands = None
        self.max_bridges = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        grid, settings = load_grid(filename, allowed_chars='12345678.', allowed_settings=['max_bridges'])
        self.grid = grid
        self.settings = settings

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.max_bridges = int(self.settings.get('max_bridges', 2))
        self.islands = []
        for row, line in enumerate(self.grid):
            self.islands.extend(
                (row, col, char)
                for col, char in enumerate(line)
                if char in '12345678'
            )

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(max_bridges=self.max_bridges,
                               islands=self.islands).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]

        # Fill in the island numbers
        for row, col, num in self.islands:
            grid[row][col] = str(num)

        return grid

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Make the grid bigger to make room for bridges to go in
        grid = buffer_grid(grid)

        # Go through and enter all the bridges
        for entry in model:
            if entry.name == 'connection':
                c1, r1, c2, r2, bridges = entry.arguments
                c1 = c1.number
                c2 = c2.number
                r1 = r1.number
                r2 = r2.number
                bridges = bridges.number
                if c1 == c2:
                    # Bridges going down
                    if bridges == 1:
                        char = '│'
                    elif bridges == 2:
                        char = '║'
                    else:
                        char = str(bridges)

                    startrow = 2 * r1 + 2
                    endrow = 2 * r2
                    col = 2 * c1 + 1

                    for idx in range(startrow, endrow + 1):
                        grid[idx][col] = char
                else:
                    # r1 == r2
                    # Bridges going across
                    # Bridges going down
                    if bridges == 1:
                        char = '─'
                    elif bridges == 2:
                        char = '═'
                    else:
                        char = str(bridges)

                    startcol = 2 * c1 + 2
                    endcol = 2 * c2
                    row = 2 * r1 + 1

                    for idx in range(startcol, endcol + 1):
                        grid[row][idx] = char

        print_chars_with_color(grid, colors=char_colors)


if __name__ == '__main__':
    solver = Hashi()
    solver.solve()
