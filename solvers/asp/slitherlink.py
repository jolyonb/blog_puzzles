"""
slitherlink.py

Solves a slitherlink/fences/loop/loop the loop puzzle, such as presented here:
https://www.puzzle-loop.com/

Capable of solving with sheep included and/or wolves excluded.

File format:
The first block describes the grid as specified in the puzzle.
Allowed characters include 0-4 for clues, period (.) for unknown cells,
S for sheep, W for wolves, and # for excluded cells (if you have a
non-rectangular grid). All lines in the grid must have the same length.

After the grid, you can include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #).
"""

from jinja2 import Template

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color_and_region


class Chars(object):
    SHEEP = 'S'
    WOLF = 'W'
    EMPTY = '.'
    UNKNOWN = '?'
    EXCLUDED = '#'
    NUMBERS = '01234'


char_colors = {
    Chars.SHEEP: Colors.YELLOW,
    Chars.WOLF: Colors.RED,
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definition
#const rows={{ rows }}.
#const cols={{ columns }}.

% Numeric entries in the puzzle
% clue(col, row, #).
{% for row, col, num in clues %}
clue({{ col }}, {{ row }}, {{ num }}).
{% endfor %}

{% if sheep|length %}
% Sheep in the puzzle
% sheep(col, row).
{% for row, col in sheep %}
sheep({{ col }}, {{ row }}).
{% endfor %}
inside(C, R) :- sheep(C, R).
{% endif %}

{% if wolves|length %}
% Wolves in the puzzle
% wolf(col, row).
{% for row, col in wolves %}
wolf({{ col }}, {{ row }}).
{% endfor %}
outside(C, R) :- wolf(C, R).
{% endif %}

{% if excluded|length %}
% Cells that are excluded from the puzzle grid
% excluded(col, row).
{% for row, col in excluded %}
excluded({{ col }}, {{ row }}).
{% endfor %}
{% endif %}
"""


class SlitherLink(Puzzle):
    """
    Class to handle SlitherLink puzzles.
    """

    puzzletype = 'slitherlink'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.grid = None
        self.settings = None
        self.rows = None
        self.columns = None
        self.clues = None
        self.wolves = None
        self.excluded = None
        self.sheep = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = Chars.WOLF + Chars.SHEEP + Chars.EXCLUDED + Chars.NUMBERS + Chars.EMPTY
        grid, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=[])
        self.grid = grid
        self.settings = settings

        # Extract values from the grid
        self.rows = len(self.grid)
        self.columns = len(self.grid[0])
        self.wolves = []
        self.sheep = []
        self.clues = []
        self.excluded = []
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == Chars.EXCLUDED:
                    self.excluded.append((row, col))
                elif char == Chars.WOLF:
                    self.wolves.append((row, col))
                elif char == Chars.SHEEP:
                    self.sheep.append((row, col))
                elif char in Chars.NUMBERS:
                    self.clues.append((row, col, char))

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(rows=self.rows,
                               columns=self.columns,
                               sheep=self.sheep,
                               wolves=self.wolves,
                               clues=self.clues,
                               excluded=self.excluded).strip()

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # We need an "inside" and an "outside" region map
        regions = [['#' for _ in range(self.columns)] for _ in range(self.rows)]
        # We also need the location of numbers/sheep/wolves/excluded entries
        grid = self.grid

        # Process the model
        for entry in model:
            if entry.name == 'inside':
                col, row = entry.arguments
                regions[row.number][col.number] = '.'
                
        if self.args.tabbed:
            print('Unable to produce tabbed output, sorry...')

        print_chars_with_color_and_region(grid, regions, char_colors, outside_region_char='#')

    def overlap_handler(self, model):
        """
        Function that is called whenever multiple solutions are found.
        """
        print('Unable to display overlaps, sorry...')
        return


if __name__ == '__main__':
    solver = SlitherLink()
    solver.solve()
