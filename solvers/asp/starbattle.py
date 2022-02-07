"""
starbattle.py

Solves a Star Battle puzzle, such as presented here:
https://www.puzzle-star-battle.com/

File format:
The first block describes the regions of the grid as specified in the
puzzle. Regions are labelled by any alphanumeric character (allowing for
at most 62 regions). Note that the grid must be square.

After the grid, include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #) as well as
the following required setting:
star_rating=number
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, print_chars_with_color_and_region
from solvers.common.regions import map_cells

class Chars(object):
    STAR = '*'
    EMPTY = '.'
    UNKNOWN = '?'

char_colors = {
    Chars.STAR: Colors.RED,
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definition
#const size={{ size }}.  % Number of rows/columns/regions
#const starcount={{ star_rating }}.  % Number of stars per row/column/region

% Define regions by number
% r(col, row, regionnum).
{% for row, col, regionnum in regions %}
r({{ col }}, {{ row }}, {{ regionnum }}).
{% endfor %}
"""


class StarBattle(Puzzle):
    """
    Class to handle Star Battle puzzles.
    """

    puzzletype = 'starbattle'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.settings = None
        self.size = None
        self.regions = None
        self.star_rating = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = '1234567890' + 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        regions, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=['star_rating'])
        self.regions = regions
        self.settings = settings
        if 'star_rating' not in settings:
            raise ValueError('The star_rating setting is missing from the puzzle definition.')
        self.star_rating = settings['star_rating']

        # Extract values from the grid and settings
        rows = len(self.regions)
        cols = len(self.regions[0])
        if rows != cols:
            raise ValueError('Non-square grid provided!')
        self.size = rows

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        cells = map_cells(self.regions)
        renderer = Template(template, trim_blocks=True)
        return renderer.render(size=self.size,
                               star_rating=self.star_rating,
                               regions=cells).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        return [[Chars.UNKNOWN for _ in range(self.size)] for _ in range(self.size)]

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Process the model
        for entry in model:
            if entry.name == 'star':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.STAR
            elif entry.name == 'empty':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.EMPTY
                
        # Print the grid
        if self.args.tabbed:
            print_chars_with_color(grid, char_colors, self.args.tabbed)
        else:
            print_chars_with_color_and_region(grid, self.regions, char_colors)

    def overlap_handler(self, model):
        """
        Function that is called whenever multiple solutions are found.
        """
        self.solution_handler(model)


if __name__ == '__main__':
    solver = StarBattle()
    solver.solve()
