import numpy as np
import subprocess
from Point import Point

def export_board(board):
    output_string = ""
    for row in board:
        output_string += ' '.join(str(x) for x in row) + '\n'
    with open('gameboard.txt', 'w') as output_file:
        output_file.write(output_string)

def import_board(filename):
    grid = list()
    with open(filename, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            row = [int(x) for x in line.split()]
            grid.append(row)
    grid = np.asarray(grid)
    return grid

def read_matches_from_file():
    matches = []
    with open('solution.txt', 'r') as input_file:
        header = input_file.readline()
        count, score, evaluations = header.split(',')
        for line in input_file:
            line = line.strip()
            parts = line.split('->')
            start_x, start_y = parts[0].split(',')
            end_x, end_y = parts[1].split(',')
            matches.append((Point(int(start_x), int(start_y)), Point(int(end_x), int(end_y))))
    return (score, matches, evaluations)

def execute_c_solver():
    subprocess.call('./solver')