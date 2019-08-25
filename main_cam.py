from machine import Pin, SDCard
from network import WLAN, STA_IF, AP_IF
from utime import sleep_ms, ticks_ms, ticks_diff, ticks_add
# import _thread
from neopixel import NeoPixel

# TODO: mount sdcard and try loading configuration from it instead of the hardcoded one. :)
# from uos import mount, umount, listdir



# class NeoPixel:
#     n = 16
#     led_list = []
#
#     def __init__(self, pin, led_count: int = 16):
#         self.pin = pin
#         for item in range(led_count):
#             self.led_list.append((0, 0, 0))
#
#     def write(self):
#         for blah in self.led_list:
#             print(blah)
#
#     def __getitem__(self, item):
#         return self.led_list[item]
#
#     def __setitem__(self, key, value):
#         self.led_list[key] = value
#         print("{}: {}".format(key, self.led_list[key]))

brightness_mod = 10

led = Pin(4, Pin.OUT)


def warning_led(led):
    for running_time in range(10):
        led.value(not led.value())
        if not led.value():
            sleep_ms(400)
        else:
            sleep_ms(1)
    led.off()


# Buttons

warning_led(led)
button_actions = {
    "Pin(14)": {
        "1": "deep_blue_sea",
        "0": "ring_of_fire",
        "pin_id": 14,
    },
    "Pin(13)": {
        "1": "circle_of_life",
        "0": "clean_neopixel",
        "pin_id": 13,
    },
    "Pin(15)": {
        "1": "bright_eyes",
        "0": "green_reaper",
        "pin_id": 15,
    },
}

last_ticks_for = {
}

_minimum_delay_between_push_buttons = 650


def was_a_long_press(button):
    button_state = 0
    _delay_between_cycles = 20
    _minimum_to_consider_a_push = 20
    _consider_long_push_after = 400
    if str(button) in last_ticks_for:
        if ticks_ms() - last_ticks_for[str(button)] < _minimum_delay_between_push_buttons:
            # print("Not that fast, niggah")
            return -1
    last_ticks_for[str(button)] = ticks_ms()

    deadline = ticks_add(ticks_ms(), 600)
    while ticks_diff(deadline, ticks_ms()) > 0:
        # print(button_state)
        if not button.value():
            button_state += _delay_between_cycles
            if button_state >= _consider_long_push_after:
                return 1
            sleep_ms(_delay_between_cycles)
        else:
            break
    if button_state >= _minimum_to_consider_a_push:
        if button_state >= _consider_long_push_after:
            return 1
        else:
            return 0
    else:
        return -1


np = NeoPixel(Pin(2), 16)


def brightness(np, bright=2):
    red, green, blue = 0, 0, 0
    bright_result = bright
    if (bright + brightness_mod) > 255:
        bright_result = 255
    elif (bright + brightness_mod) < 1:
        bright_result = 1
    else:
        bright_result = bright + brightness_mod
    for i in range(np.n):
        if np[i][0] > 0:
            red = bright_result
        elif np[i][1] > 0:
            green = bright_result
        elif np[i][2] > 0:
            blue = bright_result
        np[i] = (red, green, blue)
    np.write()


def deep_blue_sea(np):
    for i in range(np.n):
        np[i] = (0, 0, 0)
    np.write()
    for i in range(np.n):
        if i % 2 == 0:
            np[i] = (0, 0, 1)
        np.write()
    for i in range(np.n):
        if i % 2 != 0:
            np[i] = (0, 0, 1)
        np.write()
    for how_bright in range(1, 9):
        brightness(np, int(255 * (how_bright * 10) / 100))
        sleep_ms(20)


def blink_in_red(np, stay_red=False):
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()
    sleep_ms(2)
    for a, i in enumerate(range(0, np.n)):
        if i % 2 != 0:
            np[i] = (60, 0, 0)
        else:
            np[i] = (60, 10, 13)
    np.write()
    sleep_ms(5)
    if not stay_red:
        for i in range(0, np.n):
            np[i] = (0, 0, 0)
        np.write()
        sleep_ms(5)


def ring_of_fire(np):
    for i in range(0, np.n):
        np[i] = (60, 0, 0)
        np.write()
        sleep_ms(60)


def ring_of_nothing(np):
    for i in reversed(range(0, np.n)):
        np[i] = (0, 0, 0)
        np.write()
        sleep_ms(60)


def bright_up():
    global brightness_mod
    if (brightness_mod + 40) <= 250:
        brightness_mod += 40
    else:
        brightness_mod = 255
    brightness(np)


def bright_down():
    global brightness_mod
    if (brightness_mod - 40) >= 10:
        brightness_mod -= 40
    else:
        brightness_mod = 10
    brightness(np)


def clean_neopixel(np):
    for led in range(np.n):
        np[led] = (0, 0, 0)
    np.write()


def circle_of_life(np):
    clean_neopixel(np)
    initial_key = 0
    space_between_lights = int(np.n / 4)
    _interacting_lights = [initial_key]
    colour = [
        (0, 100, 00),
        (100, 00, 0),
        (2, 20, 80)
    ]
    for interaction in range(1, space_between_lights):
        _temp_light = _interacting_lights[0] + (interaction * 4)
        while _temp_light >= np.n:
            _temp_light -= np.n
        _interacting_lights.append(_temp_light)
    for how_many_times in range(np.n * 2):
        clean_neopixel(np)
        sleep_ms(30)
        # if how_many_times % 2 == 0:
        #     use_colour = colour[1]
        # elif how_many_times % 3 == 0:
        #     use_colour = colour[2]
        # else:
        #     use_colour = colour[0]
        use_colour = colour[0]
        for _interacting_led in _interacting_lights:
            _interacting_led += how_many_times
            while _interacting_led >= np.n:
                _interacting_led -= np.n
            np[_interacting_led] = use_colour
        np.write()
        sleep_ms(10)
    clean_neopixel(np)


def circle_of_death(np):
    space_between_lights = int(np.n / 4)
    for i in range(0, space_between_lights):
        for ii in range(0, space_between_lights):
            np[(ii + i)] = (0, 0, 0)
        np.write()
        sleep_ms(300)


def bright_eyes(np):
    for pin in range(np.n):
        np[pin] = (120, 120, 120)
        np.write()
        sleep_ms(50)


def green_reaper(np):
    for pin in reversed(range(np.n)):
        np[pin] = (0, 255, 0)
        np.write()
        sleep_ms(50)


def super_button_handler(p):
    _was_it_a_long_press = was_a_long_press(p)
    if _was_it_a_long_press != -1:
        if str(p) in button_actions:
            command_to_execute = button_actions[str(p)][str(_was_it_a_long_press)]
            desired_action = eval(command_to_execute)
            print("executing: {}".format(command_to_execute))
            if "no_arguments" in button_actions[str(p)] and button_actions[str(p)]['no_arguments']:
                desired_action()
            else:
                desired_action(np)
    else:
        # print("Super button handler: Ignoring button {}".format(str(p)))
        pass


# Create buttons and assign IRQ supper_button_handler to it.
buttons = []
for pin_in_action_buttons in button_actions:
    _temp_button = Pin(button_actions[pin_in_action_buttons]['pin_id'], Pin.IN, Pin.PULL_UP)
    # print(_temp_button)
    _temp_button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=super_button_handler)
    buttons.append(_temp_button)
