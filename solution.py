assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    same_value_peers = []

    # find all peers that have the same x and y coordinates and also the same value (twins)
    for location, value in values.items():
        for peer in peers[location]:
            # values should match and the value of the box should only have two values
            if values[location] == values[peer] and len(values[location]) == 2:
                same_value_peers.append((location, peer))
            
    # loop through all the possible naked twins pairs
    for location_a, location_b in same_value_peers:
        
        # this list will contain all the peers on either the same row / col as the naked twins
        possible_peers = []
        
        # if both twins are on the same row, lets look only at that row
        if location_a[0] == location_b[0]:
            # set of all the possible row values - our twins
            possible_peers = set([location_a[0] + str(i) for i in cols]) - set([location_a,location_b])
        
        # if both twins are on the same column, lets look only at that column
        elif location_a[1] == location_b[1]:
            # set of all the possible columns - our twins
            possible_peers = set([str(i) + location_a[1] for i in rows]) - set([location_a,location_b])       
        
        # for all possible row / columns, update the digit of the peers by removing the naked twins values
        for peer in possible_peers:
            for digit in values[location_a]:
                # only remove the digit from a peer if is found and the peer has > 2 digits
                if digit in values[peer] and len(values[peer]) > 2 :
                    assign_value(values, peer, values[peer].replace(digit, ''))
    
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [x+y for x in A for y in B]


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# modifications to allow for diagonal sudoku by including the two diagonal arrays to the unit list 
diagonal_units = [[(rows[index] + cols[index]) for index in range(len(rows))]]
diagonal_units_reverse = [[(rows[(len(rows)-1)-index] + cols[index]) for index in range(len(rows))]]

unitlist = column_units + row_units + square_units + diagonal_units_reverse + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    values = []
    possible_values = "123456789"
    for c in grid:
        if c == '.':
            values.append(possible_values)
        else:
            values.append(c)
    assert len(grid) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass

def eliminate(values):
    for grid_position, value in values.items():
        if len(value) == 1:
            peers_list = peers[grid_position]
            for peer in peers_list:
                assign_value(values, peer, values[peer].replace(value,''))
    return values

def only_choice(values):
    digits = "123456789"
    for unit in unitlist:
        for digit in digits:
            digit_places = [box for box in unit if digit in values[box]]
            if len(digit_places) == 1:
                assign_value(values, digit_places[0], digit)
        
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminated_values = eliminate(values)
        
        # Use the Only Choice Strategy
        values = only_choice(eliminated_values)
        
        # Using naked twins
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if not values:
        return False
    if all(len(item) == 1 for item in values.values()):
        return values
        
    # Choose one of the unfilled squares with the fewest possibilities
    _ , grid_location = min((len(values[item]), item) for item in boxes if len(values[item]) > 1)
  
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[grid_location]:
        new_board = values.copy()
        new_board[grid_location] = value
        attempt = search(new_board)
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
    return search(grid_values(grid))
    

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
