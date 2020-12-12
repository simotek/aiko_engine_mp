# lib/aiko/common.py: version: 2020-12-06 16:00
#
# To Do
# ~~~~~
# - Improve set_handler() mechanism to not require individual handler shims
# - Refactor touch_pins_check() into "lib/aiko/button.py"

from machine import Pin, TouchPad, unique_id
import os

AIKO_VERSION = "v02"

handlers = {}

def hostname():
  return os.uname()[0] + "_" + serial_id()

def log(message):
  handlers["log"](message)

def set_handler(name, handler):
  handlers[name] = handler

def touch_pins_check(touch_pins):
  if touch_pins:
    touched_pins = 0
    for touch_pin in touch_pins:
      try:
        TouchPad(Pin(touch_pin)).read()
      except Exception:
        print("### Main: Touch calibration issue on GPIO: " + str(touch_pin))
      if TouchPad(Pin(touch_pin)).read() < 200:  # TODO: Fix literal "200"
        touched_pins += 1

    if touched_pins == len(touch_pins): return True
  return False

def serial_id():
  id = unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id  # 12 hexadecimal digits
