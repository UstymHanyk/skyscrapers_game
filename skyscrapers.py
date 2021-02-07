def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    file = open(path, "r")
    gm_board = [line.strip() for line in file.readlines()]

    return gm_board



def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible
    looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if input_line[0] == "*":
        return True
    pivot = int(input_line[0])
    visibility = 1  # visibility
    prev_num = int(input_line[1])  # standard item for comparison

    for number in input_line[2:-1]:

        if int(number) > prev_num:
            visibility += 1
            prev_num = int(number)
        else:
            continue

    return visibility == pivot

def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if '?' in row:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        for element in row[1:-1]:
            if element == "*":
                pass
            else:
                if row[1:-1].count(element) > 1:
                    return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        if left_to_right_check(row,1) and left_to_right_check(row[::-1],1):
            pass
        else:
            return False
    return True


def rotate(matrix):
    """
    Rotate a nxn matrix.
    Source: https://www.tutorialspoint.com/rotate-matrix-in-python
    >>> rotate([[1,5,7],[9,6,3],[2,1,3]])
    [[2, 9, 1], [1, 6, 5], [3, 3, 7]]
    """
    temp_matrix = []
    column = len(matrix) - 1
    for column in range(len(matrix)):
        temp = []
        for row in range(len(matrix) - 1, -1, -1):
            temp.append(matrix[row][column])
        temp_matrix.append(temp)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = temp_matrix[i][j]
    return matrix

def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    temp_board = [list(row) for row in board]
    rotated_board = rotate(temp_board)
    # Use already existing functions to check for rule compliance
    return check_horizontal_visibility(rotated_board) and check_uniqueness_in_rows(rotated_board)


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    gm_board = read_input(input_path)
    return check_not_finished_board(gm_board) and \
           check_uniqueness_in_rows(gm_board) and \
           check_horizontal_visibility(gm_board) and check_columns(gm_board)


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
