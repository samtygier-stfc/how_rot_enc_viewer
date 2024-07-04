# Parts for turntable hardware

## Pieces to build the turntable.

SVG files in laser_cutting

Worked well in plywood. Depending on the thickness of the material and the depth of the buttons, you may need several pieces of panel_2.

## Components

* CNC Rotary Encoder - 100 Pulses per Rotation - 60mm
* RaspberryPi Pico
* 16mm Momentary pushbuttons - in fun colours
* Resistors if using LEDs in the pushbuttons

## Pico firmware

The Raspberrypi Pico used the https://github.com/KMKfw/kmk_firmware firmware to emulate the keypresses to control the viewer software. This is installed on top of Circuit Python.

See code.py for the KMK configuration.