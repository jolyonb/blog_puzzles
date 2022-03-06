"""
shikaku.py

Solves a shikaku puzzle, such as presented here:
https://www.puzzle-shikaku.com/

File format:
The first block describes the grid as specified in the puzzle.
Allowed characters include 0-9 for clues, and period (.) for unknown cells.
All lines in the grid must have the same length.
If any of the numbers are > 9, then the grid must be in either CSV or TSV format.

After the grid, you can include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #).
"""

from jinja2 import Template

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, print_chars_with_color_and_region


class Chars(object):
    EMPTY = '.'
    UNKNOWN = '?'


char_colors = {
    '1': Colors.CYAN,
    '2': Colors.CYAN,
    '3': Colors.CYAN,
    '4': Colors.CYAN,
    '5': Colors.CYAN,
    '6': Colors.CYAN,
    '7': Colors.CYAN,
    '8': Colors.CYAN,
    '9': Colors.CYAN,
    '0': Colors.CYAN,
}

template = """
% Puzzle Definition
% Define the grid size
#const rows={{ rows }}.
#const cols={{ cols }}.

% Numeric entries in the puzzle
% number(col, row, #).
{% for row, col, num in numbers %}
number({{ col }}, {{ row }}, {{ num }}).
{% endfor %}
"""


class Shikaku(Puzzle):
    """
    Class to handle Shikaku puzzles.
    """

    puzzletype = 'shikaku'
    
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
        self.maxnum = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        grid, settings = load_grid(filename, allowed_chars='0123456789.', allowed_settings=[], allowed_delimiters='\t,')
        self.grid = grid
        self.settings = settings

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.numbers = []
        self.maxnum = 0
        for row, line in enumerate(self.grid):
            for col, entry in enumerate(line):
                if entry.isnumeric():
                    self.numbers.append((row, col, entry))
                    if int(entry) > self.maxnum:
                        self.maxnum = int(entry)

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(rows=self.rows,
                               cols=self.cols,
                               numbers=self.numbers).strip()

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Construct the region grid
        regiongrid = [[Chars.UNKNOWN for _ in range(self.cols)] for _ in range(self.rows)]

        # Construct a mapping from (X,Y) to region number
        regionmap = {}
        for regionindex, (y, x, num) in enumerate(self.numbers):
            regionmap[(x, y)] = (regionindex, num)

        # Grab all the regions from the model
        for entry in model:
            if entry.name == 'region':
                col, row, numcol, numrow = entry.arguments
                regiongrid[row.number][col.number] = str(regionmap[(numcol.number, numrow.number)][0])

        if self.args.tabbed:
            # We're printing the regiongrid
            print('Reporting unique region identifiers for each cell')
            print_chars_with_color(regiongrid, tabbed=True)
        else:
            # We're pretty printing regions
            # Construct the number grid that we're going to print
            grid = [[Chars.UNKNOWN for _ in range(self.cols)] for _ in range(self.rows)]
            # Mark any known regions as EMPTY
            for row_idx, row in enumerate(regiongrid):
                for col_idx, cell in enumerate(row):
                    if cell != Chars.UNKNOWN:
                        grid[row_idx][col_idx] = Chars.EMPTY
            # Insert any numbers < 10.
            for y, x, num in self.numbers:
                if int(num) < 10:
                    grid[y][x] = str(num)
            # Print the grid with regions
            print_chars_with_color_and_region(grid, regiongrid, char_colors)


if __name__ == '__main__':
    solver = Shikaku()
    solver.solve()
