import RPi.GPIO as GPIO
from neopixel import *
import datetime
import time
import urllib

light_sensor_pin = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light_sensor_pin, GPIO.IN)

# LED strip configuration:
LED_COUNT      = 114      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

color_white_bright = Color(200, 200, 200)
color_white_dark = Color(30, 30, 30)
color_green = Color(0, 128, 0)
color_red = Color(139, 0, 0)

dot_top_left = 11
dot_bottom_left = 0
dot_bottom_right = 102
dot_top_right = 113

word_es = [10, 12]
word_ist = [32, 51, 52]
word_vor = [7, 15, 28]
word_wifi = [35, 48, 55, 68]
word_nach = [75, 88, 95, 109]
word_uhr = [82, 101, 103]
word_ken = [31, 29, 26]
word_mayca = [71, 70, 46, 24, 79]

minute_fuenf = [112, 92, 91, 72]
minute_zehn = [9, 13, 30, 33]
minute_zwanzig = [50, 53, 70, 73, 90, 93, 111]
minute_dreiviertel = [8, 14, 29, 34, 49, 54, 69, 74, 89, 94, 110]
minute_viertel = [49, 54, 69, 74, 89, 94, 110]
minute_halb = [6, 16, 27, 36]

hour_elf = [56, 67, 76]
hour_fuenf = [76, 87, 96, 108]
hour_eins = [5, 17, 26, 37]
hour_ein = [5, 17, 26]
hour_zwei = [77, 86, 97, 107]
hour_drei = [4, 18, 25, 38]
hour_vier = [78, 85, 98, 106]
hour_sechs = [3, 19, 24, 39, 44]
hour_acht = [79, 84, 99, 105]
hour_sieben = [2, 20, 23, 40, 43, 60]
hour_zwoelf = [63, 80, 83, 100, 104]
hour_zehn = [1, 21, 22, 41]
hour_neun = [41, 42, 61, 62]

minutes = {
    0: word_uhr,
    5: minute_fuenf + word_nach,
    10: minute_zehn + word_nach,
    15: minute_viertel + word_nach,
    20: minute_zwanzig + word_nach,
    25: minute_fuenf + word_vor + minute_halb,
    30: minute_halb,
    35: minute_fuenf + word_nach + minute_halb,
    40: minute_zwanzig + word_vor,
    45: minute_viertel + word_vor,
    50: minute_zehn + word_vor,
    55: minute_fuenf + word_vor
}

hours = {
    0: hour_zwoelf,
    1: hour_eins,
    2: hour_zwei,
    3: hour_drei,
    4: hour_vier,
    5: hour_fuenf,
    6: hour_sechs,
    7: hour_sieben,
    8: hour_acht,
    9: hour_neun,
    10: hour_zehn,
    11: hour_elf,
    12: hour_zwoelf,
    13: hour_eins,
    14: hour_zwei,
    15: hour_drei,
    16: hour_vier,
    17: hour_fuenf,
    18: hour_sechs,
    19: hour_sieben,
    20: hour_acht,
    21: hour_neun,
    22: hour_zehn,
    23: hour_elf
}

dots = {
    1: [dot_top_left],
    2: [dot_top_left, dot_top_right],
    3: [dot_top_left, dot_top_right, dot_bottom_left],
    4: [dot_top_left, dot_top_right, dot_bottom_left, dot_bottom_right],
}

is_environment_bright = True
current_on_leds = []


def set_pixel(pixel_nr, color):
    current_on_leds.append(pixel_nr)
    strip.setPixelColor(pixel_nr, color)


def clear_all():
    while current_on_leds:
        current_on_led = current_on_leds.pop()
        strip.setPixelColor(current_on_led, Color(0, 0, 0))

    strip.show()


def test_strip():
    for led in range(strip.numPixels()):
        clear_all()
        set_pixel(led, get_color())
        strip.show()
        time.sleep(0.1)


def get_color():
    return color_white_bright if is_environment_bright else color_white_dark


def draw_words():
    clear_all()

    for led in word_es + word_ist:
        set_pixel(led, get_color())

    now = datetime.datetime.now()

    current_hour = now.hour
    current_minute = now.minute // 5 * 5

    if current_minute > 20:
        if current_hour == 23:
            current_hour = 0
        else:
            current_hour = current_hour + 1

    # show "ein uhr" and not "eins uhr"
    if current_minute == 0 and (current_hour == 1 or current_hour == 13):
        for led in hour_ein:
            set_pixel(led, get_color())
    else:
        for led in hours[current_hour]:
            set_pixel(led, get_color())

    for led in minutes[current_minute]:
        set_pixel(led, get_color())

    dot = datetime.datetime.now().minute - (datetime.datetime.now().minute // 5 * 5)
    if dot > 0:
        for led in dots[dot]:
            set_pixel(led, get_color())

    strip.show()


def check_wifi():
    try:
        url = "https://www.google.com"
        urllib.urlopen(url, timeout=1)
        connected = True
    except:
        connected = False

    clear_all()
    if connected:
        color = color_green
    else:
        color = color_red

    for led in word_wifi:
        set_pixel(led, color)
    strip.show()
    time.sleep(3)


if __name__ == "__main__":
    test_strip()

    check_wifi()

    last_timestamp = None
    was_environment_bright = True
    while True:
        is_environment_bright = False if GPIO.input(light_sensor_pin) == GPIO.HIGH else True

        current_timestamp = str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
        if last_timestamp is None or last_timestamp != current_timestamp or is_environment_bright != was_environment_bright:
            draw_words()

        last_timestamp = current_timestamp
        was_environment_bright = is_environment_bright
        time.sleep(1)
