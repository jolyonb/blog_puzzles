"""
starbattle_shapeless.py

Solves the shapeless variant of a Star Battle puzzle, such as presented here:
https://www.puzzle-star-battle.com/

File format:
The first block describes a square grid containing periods and hashes. A hash
indicates an excluded square, while a period indicates a possible star location.

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
    EXCLUDED = '#'
    EMPTY = '.'
    UNKNOWN = '?'


char_colors = {
    Chars.STAR: Colors.RED,
    Chars.EMPTY: Colors.WHITE,
    Chars.EXCLUDED: Colors.WHITE,
}

template = """
% Puzzle Definition
#const size={{ size }}.  % Number of rows/columns/regions
#const starcount={{ star_rating }}.  % Number of stars per row/column/region

{% if stars|length %}
% Stars in the puzzle
% star(col, row).
{% for row, col in stars %}
star({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

% Specify which cells are excluded
% excluded(col, row).
{% for row, col in excluded %}
excluded({{ col }}, {{ row }}).
{% endfor %}
"""


class StarBattleShapeless(Puzzle):
    """
    Class to handle shapeless Star Battle puzzles.
    """

    puzzletype = 'starbattle_shapeless'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.settings = None
        self.size = None
        self.grid = None
        self.star_rating = None
        self.excluded = None
        self.stars = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = Chars.STAR + Chars.EMPTY + Chars.EXCLUDED
        grid, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=['star_rating'])
        self.grid = grid
        self.settings = settings
        if 'star_rating' not in settings:
            raise ValueError('The star_rating setting is missing from the puzzle definition.')
        self.star_rating = settings['star_rating']

        # Extract values from the grid and settings
        rows = len(self.grid)
        cols = len(self.grid[0])
        if rows != cols:
            raise ValueError('Non-square grid provided!')
        self.size = rows
        self.excluded = []
        self.stars = []
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == Chars.EXCLUDED:
                    self.excluded.append((row, col))
                elif char == Chars.STAR:
                    self.stars.append((row, col))

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(size=self.size,
                               star_rating=self.star_rating,
                               stars=self.stars,
                               excluded=self.excluded).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        grid = [[Chars.UNKNOWN for _ in range(self.size)] for _ in range(self.size)]

        # Insert excluded cells
        for row, col in self.excluded:
            grid[row][col] = '#'

        return grid

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
        print_chars_with_color(grid, char_colors, self.args.tabbed)


if __name__ == '__main__':
    solver = StarBattleShapeless()
    solver.solve()
