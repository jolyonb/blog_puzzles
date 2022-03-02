"""
shapes.py

Contains routines to help construct clingo shape definitions for polyomino puzzles.

All shapes generated have an anchor point at (0,0) that is included in the shape.

Shape definitions are of the form:
shape(shape_name, orientation, x, y)

Coordinates are (x, y) with (0, 0) being top left, y going down, x going right.
(0, 0)  (1, 0) ...
(0, 1)  (1, 1) ...
...

The present implementation assumes shapes can always be rotated.
"""

from typing import Tuple, List, Dict, Union

# All definitions are of the form "Name": ['Orientation', [(X,Y)]]
# Definitions allowing for reflections
tetrominos_free = {
    'L': ['L', [(0, 0), (0, 1), (0, 2), (1, 2)]],
    'I': ['Vertical', [(0, 0), (0, 1), (0, 2), (0, 3)]],
    'T': ['T', [(0, 0), (1, 0), (-1, 0), (0, 1)]],
    'S': ['S', [(0, 0), (0, 1), (1, 0), (-1, 1)]],
    'O': ['O', [(0, 0), (0, 1), (1, 0), (1, 1)]],
}

# Definitions not allowing for reflections
tetrominos_1sided = {
    **tetrominos_free,
    'J': ['J', [(0, 0), (0, 1), (0, 2), (-1, 2)]],
    'Z': ['Z', [(0, 0), (0, 1), (-1, 0), (1, 1)]],
}

pentominos_free = {
    'pent_F': ['F', [(0, 0), (1, 0), (0, 1), (-1, 1), (0, 2)]],
    'pent_I': ['Vertical', [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],
    'pent_L': ['L', [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)]],
    'pent_N': ['Z', [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)]],
    'pent_P': ['P', [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2)]],
    'pent_T': ['T', [(0, 0), (1, 0), (-1, 0), (0, 1), (0, 2)]],
    'pent_U': ['U', [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)]],
    'pent_V': ['L', [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]],
    'pent_W': ['steps_down_right', [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]],
    'pent_X': ['Plus', [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]],
    'pent_Y': ['crook_left', [(0, 0), (0, 1), (0, 2), (0, 3), (-1, 1)]],
    'pent_Z': ['Z', [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]],
}

pentominos_1sided = {
    **pentominos_free,
    'pent_Fr': ['Fr', [(0, 0), (-1, 0), (0, 1), (1, 1), (0, 2)]],          # Reflection of F
    'pent_J': ['J', [(0, 0), (0, 1), (0, 2), (0, 3), (-1, 3)]],            # Reflection of L
    'pent_Nr': ['S', [(0, 0), (-1, 0), (-1, 1), (-2, 1), (-3, 1)]],        # Reflection of N
    'pent_Q': ['Q', [(0, 0), (0, 1), (-1, 0), (-1, 1), (0, 2)]],           # Reflection of P
    'pent_Yr': ['crook_right', [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)]],  # Reflection of Y
    'pent_S': ['S', [(0, 0), (-1, 0), (-1, 1), (-1, 2), (-2, 2)]],         # Reflection of Z
}


def rotate(stencil: List[Tuple[int, int]], rotation_type) -> List[Tuple[int, int]]:
    """
    Takes in a shape stencil and rotates it by the given rotation (none, cw, ccw or 180).
    Returns the canonically-ordered result.
    """
    if rotation_type == 'none':
        result = stencil
    elif rotation_type == 'cw':
        result = [(-y, x) for (x, y) in stencil]
    elif rotation_type == 'ccw':
        result = [(y, -x) for (x, y) in stencil]
    elif rotation_type == '180':
        result = [(-x, -y) for (x, y) in stencil]
    else:
        raise ValueError(f'Bad rotation type: {rotation_type}')
    return canonical_order(result)


def reflect(stencil: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Takes in a shape stencil and reflects it across the X axis.
    Returns the canonically-ordered result.
    """
    return canonical_order([(-x, y) for (x, y) in stencil])


def canonical_order(stencil: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Return the given shape stencil in a canonical form:
    * The top row is 0
    * The leftmost cell in the top row is at (0, 0)
    * Included cells are in sorted order (top rows first, columns left to right)
    This allows stencils to be checked for duplicates using simple equality.
    """
    # Shift rows
    yoffset = min(y for x, y in stencil)
    newstencil = [(x, y - yoffset) for (x, y) in stencil]
    # Shift columns
    xoffset = min(x for x, y in newstencil if y == 0)
    newstencil = [(x - xoffset, y) for (x, y) in newstencil]
    # Sort cells
    newstencil = sorted(newstencil, key=lambda item: (item[1], item[0]))
    return newstencil


def generate_versions(stencil: List[Tuple[int, int]],
                      standard_orientation: str,
                      reflections: bool) -> Dict[str, List[Tuple[int, int]]]:
    """
    Generates all rotation stencils from the provided stencil, including the original.
    Returns a dictionary mapping orientation names to stencils.
    Duplicate stencils are not generated.
    If reflections is True, then they are also generated. Orientation naming priority is given to rotations.
    """
    def namer(rotation, reflected: bool = False):
        base = standard_orientation
        if reflected:
            base += '_r'
        if rotation == 'none':
            return base
        elif base == 'Vertical' and rotation in ('cw', 'ccw'):
            return 'Horizontal'
        else:
            return f'{base}_{rotation}'

    results = {}
    stencils_seen = []

    # Note that we do none in here also in order to ensure that the results are canonicalized
    for rot in ['none', 'cw', 'ccw', '180']:
        rotated = rotate(stencil, rot)
        if tuple(rotated) not in stencils_seen:
            results[namer(rot)] = rotated
            stencils_seen.append(tuple(rotated))

    if reflections:
        r_stencil = reflect(stencil)
        for rot in ['none', 'cw', 'ccw', '180']:
            rotated = rotate(r_stencil, rot)
            if tuple(rotated) not in stencils_seen:
                results[namer(rot, reflected=True)] = rotated
                stencils_seen.append(tuple(rotated))

    return results


def print_shape(stencil: List[Tuple[int, int]]):
    """
    Helper function that prints a shape.
    """
    minrow = min(y for x, y in stencil)
    maxrow = max(y for x, y in stencil)
    mincol = min(x for x, y in stencil)
    maxcol = max(x for x, y in stencil)
    cols = maxcol - mincol + 1
    rows = maxrow - minrow + 1

    c_array = [[' ' for _ in range(cols)] for _ in range(rows)]
    for x, y in stencil:
        c_array[y - minrow][x - mincol] = '#'

    for line in c_array:
        print(''.join(line))


def clingo_shape(name: str, orientation: str, stencil: List[Tuple[int, int]]) -> str:
    """
    Generates the clingo shape definition for a given name, orientation and stencil,
    returning the result as a single line.
    """
    entries = [f'shape({name},{orientation},{x},{y}).' for x, y in stencil]
    combined = ' '.join(entries)
    return combined.lower()


def get_clingo_definitions(letters: Union[str, List[str]], reflections: bool, category: str):
    """
    Generates the clingo shape definitions for the given letters, returning the results
    as a string.
    If reflections is True, uses free pieces and includes reflections.
    Otherwise, uses one-sided pieces.
    Possible categories are "tetr" for tetrominoes and "pent" for pentominoes.
    """
    if category == 'tetr':
        pieces = tetrominos_free if reflections else tetrominos_1sided
    elif category == 'pent':
        pieces = pentominos_free if reflections else pentominos_1sided
    else:
        raise ValueError(f'Bad category "{category}", was expecting "tetr" or "pent".')
    entries = []
    for name in letters:
        fullname = name if category == 'tetr' else f'pent_{name}'
        orig_orientation, orig_stencil = pieces[fullname]
        versions = generate_versions(orig_stencil, orig_orientation, reflections=reflections)
        entries.extend(
            clingo_shape(fullname, orientation, stencil)
            for orientation, stencil in versions.items()
        )
    return '\n'.join(entries)


if __name__ == '__main__':
    # # Test code to output various rotations/reflections of a given shape
    # shape = 'pent_Yr'
    # orig_orientation, orig_stencil = pentominos_1sided[shape]
    # versions = generate_versions(orig_stencil, orig_orientation, reflections=False)
    # for orientation, stencil in versions.items():
    #     print(f'{shape}, {orientation} orientation')
    #     print(clingo_shape(shape, orientation, stencil))
    #     print_shape(stencil)
    #     print()

    # Test code to generate clingo definitions
    print(get_clingo_definitions('LITSO', reflections=True, category='tetr'))
