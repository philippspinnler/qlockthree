from strip.strip import Strip, Color


class TestStrip(Strip):

    def __init__(self):
        super(TestStrip, self).__init__()

        self.led_count = 114

        self.color_white_bright = Color(200, 200, 200)
        self.color_white_dark = Color(30, 30, 30)
        self.color_green = Color(0, 128, 0)
        self.color_red = Color(139, 0, 0)

    def show(self):
        turn_off, turn_on = self.get_changes()
        for led in turn_off:
            pass
        for led in turn_on:
            pass

        self.leds_currently_on = self.leds_to_turn_on
        self.leds_to_turn_on = []
