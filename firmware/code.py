# SPDX-FileCopyrightText: 2021 Pierre Constantineau
# SPDX-License-Identifier: MIT

# This code is currently a work in progress for the prototype hardware
# and is not expected to work as-is on the final hardware
# firmware will be updated.

#pylint: disable = line-too-long
import time
import alarm
import board
import rotaryio
import keypad
import usb_hid
import pwmio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from pykey.keycode import PK_Keycode as KC
import pykey.lights as lights

################################################################
# init board's User Input (keys, buttons, encoders)
# replace with your own pins and stuff
################################################################
# -------------------------------------------
# Hardware definition: Switch Matrix Setup.
# -------------------------------------------
keys = keypad.KeyMatrix(
    row_pins=(board.P0_06, board.P1_13, board.P0_28),
    column_pins=(board.P0_09, board.P0_13,board.P1_06),
    columns_to_anodes=False,
)

# -------------------------------------------
# Hardware definition: Key Switch Setup.
# -------------------------------------------
buttons = None

# -------------------------------------------
# Hardware definition: rotary encoder
# -------------------------------------------
encoder = rotaryio.IncrementalEncoder(board.P0_26, board.P0_30)


################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################
# -------------------------------------------
# Hardware definition: GPIO where Neopixel (RGB LED) is connected.
# -------------------------------------------
pixel_pin = None
num_pixels = 0

# -------------------------------------------
# Hardware definition: LED Matrix
# -------------------------------------------
leds = lights.LEDMatrix((board.P0_08,board.P0_02,board.P0_03),(board.P0_24,board.P0_20,board.P0_10),True)
leds.reset_leds()


# -------------------------------------------
# Hardware definition: audio hardware
# -------------------------------------------
buzzer = pwmio.PWMOut(board.P0_29, variable_frequency=True)
buzzer.frequency = 440
OFF = 0
ON = 2**15
not_sleeping = True


################################################################
# Initialize common variables
# No need to replace things
################################################################
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
last_position = 0
layer = 0



keymap = ((KC.A,KC.B,KC.C,KC.D,KC.E,KC.F,KC.G,KC.H,KC.I),
        (KC.A,KC.B,KC.C,KC.D,KC.E,KC.F,KC.G,KC.H,KC.I))


encoder_map = ((KC.LEFT,KC.RIGHT),
                (KC.LEFT, KC.RIGHT))

################################################################
# DONE SETTING UP 
################################################################
# End of Setup: Lets play some Music to let the user we are ready
buzzer.duty_cycle = ON
buzzer.frequency = 440
time.sleep(0.05)
buzzer.frequency = 880
time.sleep(0.05)
buzzer.frequency = 1660
time.sleep(0.05)
buzzer.duty_cycle = OFF

################################################################
# loop-y-loop
################################################################
while not_sleeping:
    key_event = keys.events.get()
    if key_event:
        key = keymap[layer][key_event.key_number]
        if key_event.pressed:
            keyboard.press(key)
            leds.led_ON(key_event.key_number)
        else:
            keyboard.release(key)

    position = encoder.position
    if position != last_position:
        diff=position-last_position
        if diff>0:
            keyboard.send(encoder_map[layer][0])
        else:
            keyboard.send(encoder_map[layer][1])
    last_position = position
    time.sleep(0.002)
# if we end up here, the program will end with a short tune...
buzzer.duty_cycle = ON
buzzer.frequency = 1660
time.sleep(0.05)
buzzer.frequency = 880
time.sleep(0.05)
buzzer.frequency = 440
time.sleep(0.05)
buzzer.duty_cycle = OFF
