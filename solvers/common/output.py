"""
output.py

Contains definitions for outputting results to a terminal.
"""

from typing import List, Dict, Union


class Colors:
    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    RESET = '\u001b[0m'


def print_chars_with_color(chars: Union[List[str], List[List[str]]],
                           colors: Dict[str, str] = None,
                           tabbed: bool = False):
    """
    Take in a list of strings. Print them a single character at a time, using the colors dict to color
    individual characters. If tabbed is True, ignores colors and outputs a tab between each character.
    """
    endchar = '\t' if tabbed else ''
    for row in chars:
        for char in row:
            if not tabbed and char in colors:
                print(colors[char], end='')
        
            print(char, end=endchar)
        
            # Reset colors
            if not tabbed:
                print(Colors.RESET, end='')
        print()
