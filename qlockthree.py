import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import datetime
import time
import urllib
import os

light_sensor_port = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light_sensor_port, GPIO.IN)

PIXEL_COUNT = 114
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

color_white_bright = Adafruit_WS2801.RGB_to_color(200, 200, 200)
color_white_dark = Adafruit_WS2801.RGB_to_color(30, 30, 30)
color_green = Adafruit_WS2801.RGB_to_color(0, 128, 0)
color_red = Adafruit_WS2801.RGB_to_color(139, 0, 0)

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


def get_color():
    return color_white_bright if is_environment_bright else color_white_dark


def draw_words():
    for led in word_es + word_ist:
        pixels.set_pixel(led, get_color())

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
            pixels.set_pixel(led, get_color())
    else:
        for led in hours[current_hour]:
            pixels.set_pixel(led, get_color())

    for led in minutes[current_minute]:
        pixels.set_pixel(led, get_color())

    dot = datetime.datetime.now().minute - (datetime.datetime.now().minute // 5 * 5)
    if dot > 0:
        for led in dots[dot]:
            pixels.set_pixel(led, get_color())


def intro():
    owner = os.environ.get('QLOCKTHREE_OWNER')
    if not owner:
        return

    if owner == 'mayca':
        word = word_mayca
    elif owner == 'ken':
        word = word_ken

    for idx in range(len(word)):
        pixels.clear()
        for idx2 in range(0, idx + 1):
            pixels.set_pixel(word[idx2], get_color())
        pixels.show()
        time.sleep(1)
    time.sleep(4)


def check_wifi():
    try:
        url = "https://www.google.com"
        urllib.urlopen(url)
        connected = True
    except:
        connected = False

    pixels.clear()
    if connected:
        color = color_green
    else:
        color = color_red

    for led in word_wifi:
        pixels.set_pixel(led, color)
    pixels.show()
    time.sleep(3)


if __name__ == "__main__":
    pixels.clear()
    pixels.show()
    time.sleep(5)

    check_wifi()
    intro()

    last_timestamp = None
    was_environment_bright = True
    while True:
        is_environment_bright = False if GPIO.input(40) == GPIO.HIGH else True

        current_timestamp = str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
        if last_timestamp is None or last_timestamp != current_timestamp or is_environment_bright != was_environment_bright:
            pixels.clear()
            draw_words()
            pixels.show()

        last_timestamp = current_timestamp
        was_environment_bright = is_environment_bright
        time.sleep(1)
