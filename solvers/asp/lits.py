"""
lits.py

Solves a LITS puzzle, such as presented here:
https://www.puzzle-lits.com/

File format:
The first block describes the regions of the grid as specified in the
puzzle. Regions are labelled by any alphanumeric character (allowing for
at most 62 regions).

After the grid, include an empty line to begin the optional second block.
The lines that follow allow for comments (starting with a #).
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, print_chars_with_color_and_region
from solvers.common.regions import map_cells


class Chars(object):
    L = 'L'
    I = 'I'
    T = 'T'
    S = 'S'
    EMPTY = '.'
    UNKNOWN = '?'


char_mapping = {
    'tetr_l': 'L',
    'tetr_i': 'I',
    'tetr_t': 'T',
    'tetr_s': 'S',
}

char_colors = {
    Chars.L: Colors.RED,
    Chars.I: Colors.YELLOW,
    Chars.T: Colors.CYAN,
    Chars.S: Colors.MAGENTA,
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definition
% Define regions by number
% region(col, row, regionnum).
{% for row, col, regionnum in regions %}
region({{ col }}, {{ row }}, {{ regionnum }}).
{% endfor %}
"""


class Lits(Puzzle):
    """
    Class to handle LITS puzzles.
    """

    puzzletype = 'lits'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.settings = None
        self.rows = None
        self.cols = None
        self.regions = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = '1234567890' + 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        regions, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=[])
        self.regions = regions
        self.settings = settings

        # Extract values from the grid and settings
        self.rows = len(self.regions)
        self.cols = len(self.regions[0])

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        cells = map_cells(self.regions)
        renderer = Template(template, trim_blocks=True)
        return renderer.render(regions=cells).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        return [[Chars.UNKNOWN for _ in range(self.cols)] for _ in range(self.rows)]

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Process the model
        for entry in model:
            if entry.name == 'black':
                col, row, shape, _ = entry.arguments
                grid[row.number][col.number] = char_mapping[shape.name]
            elif entry.name == 'white':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.EMPTY

        # Print the grid
        if self.args.tabbed:
            print_chars_with_color(grid, char_colors, True)
        else:
            print_chars_with_color_and_region(grid, self.regions, char_colors)


if __name__ == '__main__':
    solver = Lits()
    solver.solve()
