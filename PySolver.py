import numpy as np
from Point import Point

def solve_horizontal(board):
    score = 0
    matches = []
    for row_num in range(len(board)):
        row = board[row_num]
        for i in range(len(row)):
            element = row[i]
            if element != 0:
                j = i + 1
                run = [element]
                while sum(run) < 10 and j < 17:
                    if row[j] != 0:
                        run.append(row[j])
                    j += 1
                if sum(run) == 10:
                    score += len(run)
                    row[i] = 0
                    matches.append((Point(i, row_num), Point(j, row_num)))
                    for val in range(i + 1, j):
                        row[val] = 0
    return (score, matches)

def solve_vertical(board):
    grid_width = len(board[0])
    grid_height = len(board)
    score = 0
    matches = []
    for j in range(grid_width):
        for i in range(grid_height):
            element = board[i][j]
            if element != 0:
                k = i + 1
                run = [element]
                while sum(run) < 10 and k < 10:
                    if board[k][j] != 0:
                        run.append(board[k][j])
                    k += 1
                if sum(run) == 10:
                    score += len(run)
                    board[i][j] = 0
                    matches.append((Point(j, i), Point(j, k)))
                    for val in range(i + 1, k):
                        board[val][j] = 0
    return (score, matches)

def solve_diagonal(board, destructive = True):
    grid_width = len(board[0])
    grid_height = len(board)
    score = 0
    matches = []
    for j in range(grid_width):
        for i in range(grid_height):
            for x in range(j, grid_width):
                for y in range(i, grid_height):
                    if np.sum(board[i:y, j:x]) == 10:
                        score += np.count_nonzero(board[i:y, j:x])
                        if destructive:
                            board[i:y, j:x] = 0
                        matches.append((Point(j, i), Point(x, y)))
    return (score, matches)

def generate_diagonal_matches(board):
    score = 0
    matches = []
    while True:
        d_score, d_matches = solve_diagonal(board)
        if d_score == 0:
            break
        matches.extend(d_matches)
        score += d_score
    return (score, matches)

def generate_matches(board):
    score = 0
    matches = []
    while True:
        h_board = np.copy(board)
        v_board = np.copy(board)
        d_board = np.copy(board)
        h_score, h_matches = solve_horizontal(h_board)
        v_score, v_matches = solve_vertical(v_board)
        d_score, d_matches = solve_diagonal(d_board)
        matches_array = [h_matches, v_matches, d_matches]
        score_array = [h_score, v_score, d_score]
        board_array = [h_board, v_board, d_board]
        if sum(score_array) == 0:
            break
        max_index = np.argmax(score_array)
        matches.extend(matches_array[max_index])
        score += score_array[max_index]
        board = board_array[max_index]
    return (score, matches)