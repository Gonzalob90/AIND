assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.

    We should use this function at the eliminate and only choice function, since in that
    functions we update the values of the dictionary. Also, we only update if the values are one digit.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def rep(xs):

    """
    Arg: a list of the values of any unit
    Output: the repeated value in a unit, in order to perform naked twins function.
    """

    a = []
    for i in xs:
        if (xs.count(i) == 2):
            a.append(i)
    if len(a)==0:
         values=[]
    else:
        values=a[0]
    return values

def diagonal(A,B):

    """
    Arg: Two lists, in this case rows and columns
    Output: A list with the boxes of the diagonals.
    """

    A_list = list(A)
    B_list = list(B)

    return [A_list[i]+B_list[i] for i in range(len(A_list))]



def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#Defining some variables

rows = 'ABCDEFGHI'
cols = '123456789'

#We inverted the order of columns to use it in the diagonal function
cols_inverted = sorted(list(cols),reverse=True)

diagonal1 = diagonal(rows,cols)
diagonal2 = diagonal(rows,cols_inverted)

boxes = cross(rows, cols)

row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + [diagonal1] + [diagonal2]

## dictionary where the key is the box, and the value is a list of the units where it belongs
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

## dictionary for peers
peers = dict((s, set(sum(units[s],[]))-set([s]))for s in boxes)



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # First we loop to get all the units.
    for unit in unitlist:
        twin_values_list=[]
        # Make a list of the values in that unit.
        twin_values_list=[values[box] for box in unit]
        # We find if there is any repeated value considered as naked twin
        twin_values = rep(twin_values_list)

        list_peers = []
        # If there are two boxes with the same two digits as values (naked twins) execute
        if len(twin_values)==2:
            # We make a list of all the peers in that unit which are different from the twin values
            list_peers = [box for box in unit if values[box] != twin_values]

        for twin_value in twin_values:
            # We eliminate the digits of the twin values from the peeers
            for box in list_peers :
                if twin_value in values[box]:
                    original3 = values
                    values[box]= values[box].replace(twin_value,'')
                    assign_value(original3, box, values[box])


    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
        ##chars list will be like, '4' or '123456789'
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):

    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            original1=values
            values[peer] = values[peer].replace(digit,'')
            assign_value(original1, peer, values[peer])

    return values


def only_choice(values):

    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                original2=values
                values[dplaces[0]] = digit
                assign_value(original2, dplaces[0], values[dplaces[0]])
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values_final = search(values)
    return values_final

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



