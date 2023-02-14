import OCR
import pyautogui

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