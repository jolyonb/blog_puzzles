"""
hitori.py

Solves a hitori puzzle, such as presented here:
https://www.puzzle-hitori.com/

File format:
The first block describes the grid as specified in the puzzle.
If there are numbers above 9, the grid must be either comma- or tab-delimited.
Each cell in the grid must have a number in it.
All lines in the grid must have the same length.

After the grid, you can include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #).
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color

char_colors = {
    '#': Colors.RED,
}

template = """
% Puzzle Definition
% Numeric entries in the puzzle
% number(col, row, #).
{% for row, col, num in numbers %}
number({{ col }}, {{ row }}, {{ num }}).
{% endfor %}
"""


class Hitori(Puzzle):
    """
    Class to handle Hitori puzzles.
    """

    puzzletype = 'hitori'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.grid = None
        self.settings = None
        self.rows = None
        self.cols = None
        self.numbers = None
        self.max_num = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        grid, settings = load_grid(filename, allowed_chars='0123456789', allowed_settings=[], allowed_delimiters='\t,')
        self.grid = grid
        self.settings = settings

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.numbers = []
        self.max_num = -1
        for row, line in enumerate(self.grid):
            for col, num in enumerate(line):
                intnum = int(num)
                if intnum < 1:
                    raise ValueError(f'Bag grid entry in row {row+1}, column {col+1}: "{num}"')
                self.numbers.append((row, col, intnum))
                if intnum > self.max_num:
                    self.max_num = intnum

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(numbers=self.numbers).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]

        # Fill in the numbers if there will be room to print them!
        if self.args.tabbed or self.max_num <= 9:
            for row, col, num in self.numbers:
                grid[row][col] = str(num)

        return grid

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Grab the black squares from the solution
        for entry in model:
            if entry.name == 'black':
                col, row = entry.arguments
                grid[row.number][col.number] = '#'
                
        # Print the grid
        print_chars_with_color(grid, char_colors, self.args.tabbed)


if __name__ == '__main__':
    solver = Hitori()
    solver.solve()
