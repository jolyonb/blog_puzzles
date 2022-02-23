"""
yajilin.py

Solves a yajilin/arrow ring puzzle, such as presented here:
https://www.gmpuzzles.com/blog/tag/yajilin-2+classic/

File format:
The file format consists of three blocks.

The first block contains the grid and the corresponding numbers.
Allowed characters include 0-9 for clues, period (.) for white cells
and # for shaded cells. No directional information is included.
All lines in the grid must have the same length.

The first grid ends when there is a blank line.

The second block contains the grid again, this time with the directional
information. The second block must be exactly the same size as the first
block. All empty and excluded cells from the first block must also be
empty/excluded in the second block. The numbers from the first block are
replaced with the direction for that cell, using < (less than), > (greater
than), v (lower case vee) and ^ (caret).

After the second grid, you can include an empty line to begin the third block.
The lines that follow allow for comments (starting with a #) as well as
the following optional setting:
variant=???
The default variant is "default", with other options including "full-lane",
"one-off" and "closed-loop".
"""

from jinja2 import Template

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_2grids
from solvers.common.output import Colors, print_chars_with_color, loop_directions


class Chars(object):
    EMPTY = '.'
    BLACK = 'B'
    UNKNOWN = '?'
    EXCLUDED = '#'
    NUMBERS = '0123456789'


char_colors = {
    Chars.BLACK: Colors.RED,
    Chars.EMPTY: Colors.WHITE,
    Chars.EXCLUDED: Colors.WHITE,
}

template = """
% Puzzle Definition
#const rows={{ rows }}.
#const cols={{ columns }}.

% Number cells
% number(col, row, num, dir).  % Choose dir=n/s/e/w.
{% for row, col, num, dir in numbers %}
number({{ col }}, {{ row }}, {{ num }}, {{ dir }}).
{% endfor %}

{% if excluded|length %}
% Cells that are excluded from the puzzle grid
% excluded(col, row).
{% for row, col in excluded %}
excluded({{ col }}, {{ row }}).
{% endfor %}
{% endif %}
"""


class Yajilin(Puzzle):
    """
    Class to handle Yajilin puzzles.
    """

    @property
    def puzzletype(self) -> str:
        """Return the puzzle type for this class. Note that it will change if a variant is detected."""
        variants = {
            'default': 'yajilin',
            'one-off': 'yajilin_oneoff',
            'full-lane': 'yajilin_fulllane',
            'closed-loop': 'yajilin_closedloop',
        }
        return variants[self.variant]

    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.number_grid = None
        self.dir_grid = None
        self.settings = None
        self.rows = None
        self.columns = None
        self.numbers = None
        self.excluded = None
        self.variant = 'default'

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        base = Chars.EXCLUDED + Chars.EMPTY
        self.number_grid, self.dir_grid, settings = load_2grids(
            filename,
            allowed_chars1=base + Chars.NUMBERS,
            allowed_chars2=f'{base}<>^v',
            allowed_settings=['variant'],
        )

        self.settings = settings
        self.variant = settings.get('variant', 'default')

        # Extract values from the grid
        self.rows = len(self.number_grid)
        self.columns = len(self.number_grid[0])
        self.numbers = []
        self.excluded = []
        directions = {'<': 'w', '>': 'e', '^': 'n', 'v': 's'}
        for row, line in enumerate(self.number_grid):
            for col, char in enumerate(line):
                if char == Chars.EXCLUDED:
                    if self.dir_grid[row][col] != Chars.EXCLUDED:
                        raise ValueError(f'Disagreement between the two grids, row {row + 1} and col {col + 1}')
                    self.excluded.append((row, col))
                elif char in Chars.NUMBERS:
                    if self.dir_grid[row][col] not in '<>v^':
                        raise ValueError(f'Disagreement between the two grids, row {row + 1} and col {col + 1}')
                    self.numbers.append((row, col, char, directions[self.dir_grid[row][col]]))
                elif char == Chars.EMPTY:
                    if self.dir_grid[row][col] != Chars.EMPTY:
                        raise ValueError(f'Disagreement between the two grids, row {row + 1} and col {col + 1}')

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(rows=self.rows,
                               columns=self.columns,
                               numbers=self.numbers,
                               excluded=self.excluded).strip()

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = [['.' for _ in range(self.columns)] for _ in range(self.rows)]

        # Put in numbers and excluded spaces
        for row, col in self.excluded:
            grid[row][col] = '#'
        for row, col, num, dir in self.numbers:
            grid[row][col] = str(num)

        # Go and grab all the entries from the solution
        for entry in model:
            if entry.name == 'black':
                col, row = entry.arguments
                grid[row.number][col.number] = 'B'
            elif entry.name == 'loop':
                col, row, direction = entry.arguments
                grid[row.number][col.number] = loop_directions[direction.name]

        # Print the grid
        print_chars_with_color(grid, char_colors, False)

        if self.args.tabbed:
            print('Unable to print tabbed output, sorry!')

    def overlap_handler(self, model):
        """
        Function that is called whenever multiple solutions are found.
        """
        print('Unable to display overlaps, sorry...')
        return


if __name__ == '__main__':
    solver = Yajilin()
    solver.solve()
