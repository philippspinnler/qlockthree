from strip import Strip


class WS2801(Strip):

    def __init__(self):
        super(WS2801, self).__init__()

        import RPi.GPIO as GPIO
        import Adafruit_WS2801

        PIXEL_COUNT = 114
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.strip = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

    def clear_all(self):
        self.strip.clear()

    def show(self):
        turn_off, turn_on = self.get_changes()
        self.clear_all()
        for led in turn_on:
            self.strip.set_pixel(led['led_nr'], Adafruit_WS2801.RGB_to_color(led['color'].r, led['color'].g, led['color'].b))
            self.strip.show()
