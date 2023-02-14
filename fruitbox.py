
import AutoInput
import CSolver
import OCR
import PySolver
import time

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
    AutoInput.apply_matches(c_matches)
    print(f'\ntime to apply: {time.time() - apply_start}')
    print(f'\nrun time: {time.time() - start_time}')

main()
