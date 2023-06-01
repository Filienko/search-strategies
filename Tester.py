from Board import Board
import sys

# Initiated the main python solving test program
if __name__ == '__main__':
    # In order to support File Redirection, of following format: Tester.py < input.txt, implement that command prompt
    input_lines = sys.stdin.readlines()

    # Proceed to input all of the lines listed among the inputted file as separate lines
    for line in input_lines:
        # Removes \n from current user string
        board = Board(line[:-1])
        board.initialize_game()
