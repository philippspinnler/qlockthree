import urllib
import time

from util import mapping


def check_wifi(strip):
    try:
        url = "https://www.google.com"
        urllib.urlopen(url)
        connected = True
    except:
        connected = False

    if connected:
        color = strip.color_green
    else:
        color = strip.color_red

    for led in mapping.word_wifi:
        strip.set_pixel(led, color)
    strip.show()
    time.sleep(3)
