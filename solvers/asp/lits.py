"""
lits.py

Solves a LITS puzzle, such as presented here:
https://www.puzzle-lits.com/

File format:
The first block describes the regions of the grid as specified in the
puzzle. Regions are labelled by any alphanumeric character (allowing for
at most 62 regions).

After the grid, include an empty line to begin the optional second block.
The lines that follow allow for comments (starting with a #), as well as
the following optional settings:
letters=LITS
reflections=True/False
The letters setting allows you to choose which letters can be used.
The reflections setting specifies if you want to allow reflections or not.
With reflections=True, you can choose from L, I, T, S.
With reflections=False, you can also add in J and Z.
Reflections defaults to True.
Letters defaults to all available letters (LITS or LITSJZ as appropriate).
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.asp.shapes import get_clingo_definitions
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, print_chars_with_color_and_region
from solvers.common.regions import map_cells


class Chars(object):
    L = 'L'
    I = 'I'
    T = 'T'
    S = 'S'
    J = 'J'
    Z = 'Z'
    EMPTY = '.'
    UNKNOWN = '?'


char_colors = {
    Chars.L: Colors.RED,
    Chars.I: Colors.YELLOW,
    Chars.T: Colors.CYAN,
    Chars.S: Colors.MAGENTA,
    Chars.J: Colors.BLUE,
    Chars.Z: Colors.GREEN,
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definition
% Define regions by number
% region(col, row, regionnum).
{% for row, col, regionnum in regions %}
region({{ col }}, {{ row }}, {{ regionnum }}).
{% endfor %}

% Shape definitions
{{ shape_defs }}
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
        self.reflections = None
        self.letters = None
        self.rows = None
        self.cols = None
        self.regions = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = '1234567890' + 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        regions, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=['reflections', 'letters'])
        self.regions = regions
        self.settings = settings
        self.reflections = settings.get('reflections', True)
        # Convert reflections from a string to a boolean
        if isinstance(self.reflections, str):
            self.reflections = self.reflections.lower() in ['1', 'true', 't', 'y', 'yes']
        default = 'LITS' if self.reflections else 'LITSJZ'
        self.letters = settings.get('letters', default).upper()
        self.letters = ''.join(sorted(list(set(self.letters))))  # Remove any duplicates

        # Extract values from the grid and settings
        self.rows = len(self.regions)
        self.cols = len(self.regions[0])

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        cells = map_cells(self.regions)
        shape_defs = get_clingo_definitions(self.letters, self.reflections, category='tetr')
        renderer = Template(template, trim_blocks=True)
        return renderer.render(regions=cells, shape_defs=shape_defs).strip()

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
                grid[row.number][col.number] = shape.name.upper()
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
