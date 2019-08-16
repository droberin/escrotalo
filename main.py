import ssd1306
from ubinascii import hexlify
from machine import Pin, PWM, I2C, unique_id
from network import WLAN, STA_IF, AP_IF
from utime import sleep_ms, localtime
from ntptime import settime
from neopixel import NeoPixel
from random import getrandbits

sta_if = WLAN(STA_IF)
# ap_if = WLAN(AP_IF)

brightness_mod = 10

# define pin 2 as output
led = Pin(2, Pin.OUT)
# define value of "led" as "1" or "True" to turn on the LED
led.value(1)
# define value of "led" as "0" or "False" to turn off the LED
led.value(0)
# also you can use .on() or .off methods to control the pin:
led.off()
sleep_ms(600)
led.on()


class OLEDScreen:
    oled = None
    i2c = None
    max_lines = 4
    version = "0.1"

    def __init__(self, width=128, height=64, max_lines=6):
        self.i2c = I2C(scl=Pin(4), sda=Pin(5))
        self.oled = ssd1306.SSD1306_I2C(width, height, self.i2c)
        self.max_lines = max_lines
        self.oled.text("ersum", 48, 50)
        self.draw("logo_versum", 8, 20)
        self.oled.show()

    def print(self, message=['Empty data print']):
        self.oled.fill(0)
        count = 0
        for data_message in message:
            if count < self.max_lines:
                self.oled.text(data_message, 0, (10 * count))
                count += 1
            else:
                break
        self.oled.show()

    def draw(self, image_file_name, x_offset=0, y_offset=0, black_pixels=False):
        with open(image_file_name + '.pixelmap', 'r') as image:
            for x, row in enumerate(image.readlines()):
                for y, col in enumerate(row):
                    if col == "1" or col == " ":
                        self.oled.pixel(y + y_offset, x + x_offset, 1)
                    elif black_pixels:
                        self.oled.pixel(y + y_offset, x + x_offset, 0)
            image.close()
            self.oled.show()

    def blank_it(self):
        self.oled.fill(0)
        self.oled.show()


screen = OLEDScreen(max_lines=6)
sleep_ms(1400)
screen.blank_it()


def print_status():
    status_data = [
        "IP Address:",
        " " + sta_if.ifconfig()[0],
        "Machine ID:",
        " " + str(hexlify(unique_id()))
    ]
    screen.print(status_data)


def print_love(p):
    if not p.value():
        screen.print(["óóóóóóóó", "óLugh Brothersó", "óóóóóóóó", " DRoBoTo", "   LoVeS", " Agares"])


# screen.draw(image_file_name="tetis", x_offset=3, y_offset=40, black_pixels=True)


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


def button_bright_up(p):
    if not p.value():
        bright_up()


def button_ramdon_light_thing(p):
    if not p.value():
        if int(get_current_minute()[-1]) % 2 == 0:
            deep_blue_sea(np)
        else:
            ring_of_fire(np)


def button_bright_down(p):
    if not p.value():
        bright_down()


def bright_up():
    global brightness_mod
    if (brightness_mod + 10) <= 250:
        brightness_mod += 10
    else:
        brightness_mod = 255
    brightness(np)


def bright_down():
    global brightness_mod
    if (brightness_mod - 10) >= 10:
        brightness_mod -= 10
    else:
        brightness_mod = 10
    brightness(np)


# Buttons
# button_left = Pin(0, Pin.IN, Pin.PULL_UP)
button_down = Pin(13, Pin.IN, Pin.PULL_UP)
button_up = Pin(12, Pin.IN, Pin.PULL_UP)
button_in = Pin(14, Pin.IN, Pin.PULL_UP)


def get_current_minute():
    return str("-".join([str(x) for x in localtime()[0:3]]) + " " + ":".join([str(x) for x in localtime()[3:5]]))


def clear_screen(p):
    if p.value() == 0:
        screen.blank_it()
        ring_of_nothing(np)


def miao_up(p):
    if p.value() == 0:
        party()


def versum(p):
    if not p.value():
        screen.blank_it()
        # print_this(display=screen.oled, image=battery_full, x_offset=0, y_offset=100)
        screen.draw("logo_versum", x_offset=8, y_offset=20, black_pixels=True)
        screen.oled.text('Hermanos Lugh', 13, 1)
        screen.oled.text('ersum 2019', 48, 50)
        # screen.oled.text('2019', 75, 50)
        screen.oled.show()


def lugh():
    screen.blank_it()
    screen.draw("logo_lugh")
    screen.oled.text('Hermanos', 60, 3)
    screen.oled.text('Lugh', 65, 11)
    screen.oled.show()


def party():
    screen.blank_it()
    screen.draw('bros')
    screen.oled.text("Let's get this", 2, 33)
    screen.oled.text("party started", 6, 43)
    screen.oled.show()



lugh()
if sta_if.active():
    settime()
current_time = get_current_minute()
screen.print(["Current UTC time", current_time])
sleep_ms(2200)
screen.blank_it()


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
    for how_many_times in range(np.n * 4):
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


# circle_of_life(np)
# ring_of_fire(np)
# deep_blue_sea(np)
# ring_of_nothing(np)


# class neopixel:
#     n = 16
#     leds = []
#
#     def __init__(self):
#         for item in range(self.n):
#             self.leds.append((0, 0, 0))
#
#     def write(self):
#         for blah in self:
#             print(blah)
#
#     def __getitem__(self, item):
#         return self.leds[item]
#
#     def __setitem__(self, key, value):
#         self.leds[key] = value
#

def circle_of_death(np):
    space_between_lights = int(np.n / 4)
    for i in range(0, space_between_lights):
        for ii in range(0, space_between_lights):
            np[(ii + i)] = (0, 0, 0)
        np.write()
        sleep_ms(300)


np = NeoPixel(Pin(0), 16)

# circle_of_life(np)
# ring_of_fire(np)
# blink_in_red(np)
# blink_in_red(np, stay_red=True)

# button_left.irq(trigger=Pin.IRQ_FALLING, handler=clear_screen)
button_in.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_ramdon_light_thing)
button_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_bright_up)
button_down.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_bright_down)
circle_of_life(np)
