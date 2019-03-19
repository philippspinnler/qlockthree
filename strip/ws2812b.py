from strip import Strip, Color


class WS2812b(Strip):

    def __init__(self):
        super(WS2812b, self).__init__()

        from neopixel import Adafruit_NeoPixel

        # LED strip configuration:
        LED_COUNT = 114  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.led_count = LED_COUNT

        self.color_white_bright = Color(200, 200, 200)
        self.color_white_dark = Color(30, 30, 30)
        self.color_green = Color(0, 128, 0)
        self.color_red = Color(139, 0, 0)

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def show(self):

        from neopixel import Color as WS2812Color

        turn_off, turn_on = self.get_changes()
        for led in turn_off:
            self.strip.setPixelColor(led['led_nr'], WS2812Color(0, 0, 0))
        for led in turn_on:
            self.strip.setPixelColor(led['led_nr'], WS2812Color(led['color'].r, led['color'].g, led['color'].b))

        self.strip.show()
        self.leds_currently_on = turn_on
        self.leds_to_turn_on = []
