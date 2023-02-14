
import CSolver
import OCR
import pyautogui
import PySolver
import time

def apply_matches(matches):
    for match in matches:
        start_point = match[0]
        end_point = match[1]
        start_x = OCR.BOARD_LEFT + (start_point.x * OCR.APPLE_DIMS[0])
        start_y = OCR.BOARD_TOP + (start_point.y * OCR.APPLE_DIMS[1])
        end_x = OCR.BOARD_LEFT + ((end_point.x + 1) * OCR.APPLE_DIMS[0])
        end_y = OCR.BOARD_TOP + ((end_point.y + 1) * OCR.APPLE_DIMS[1])
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(end_x, end_y)
        pyautogui.mouseUp()

def reset():
    reset_button = (40, 374)
    play_button = (170, 217)
    reset_x = OCR.BOARD_LEFT + reset_button[0]
    reset_y = OCR.BOARD_TOP + reset_button[1]
    play_x = OCR.BOARD_LEFT + play_button[0]
    play_y = OCR.BOARD_TOP + play_button[1]
    pyautogui.moveTo(reset_x, reset_y)
    pyautogui.click()
    pyautogui.moveTo(play_x, play_y)
    pyautogui.click()

def main():
    start_time = time.time()
    time.sleep(2)
    ocr_start = time.time()
    board = OCR.get_board()
    #board = import_board('gameboard.txt')
    print(f'\ntime to ocr: {time.time() - ocr_start}')
    CSolver.export_board(board)
    solve_start = time.time()
    CSolver.execute_c_solver()
    c_score, c_matches, c_evaluations = CSolver.read_matches_from_file()
    print(f'evaluations: {int(c_evaluations):,}')
    py_score, py_matches = PySolver.generate_matches(board)
    print(f'\ntime to solve: {time.time() - solve_start}')
    print(f'\nC Score: {c_score}')
    print(f'Py Score: {py_score}\n')
    apply_start = time.time()
    apply_matches(c_matches)
    print(f'\ntime to apply: {time.time() - apply_start}')
    print(f'\nrun time: {time.time() - start_time}')

main()
