import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

button_pins = [board.GP10, board.GP6, board.GP2]
encoder_pins = [board.GP16, board.GP17]


class MantidController1(KMKKeyboard):

    def __init__(self):
        # https://docs.circuitpython.org/en/latest/shared-bindings/keypad/index.html#keypad.Keys
        self.matrix = KeysScanner(button_pins,
                                  value_when_pressed=True,
                                  pull=True)


keyboard = MantidController1()
keyboard.keymap = [[KC.LCTL(KC.N1), KC.LCTL(KC.N2), KC.LCTL(KC.N3)]]

encoder_handler = EncoderHandler()
encoder_handler.pins = (encoder_pins, )
encoder_handler.map = (((KC.LCTL(KC.N4), KC.LCTL(KC.N5)), ), )
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
