from strip import Color
from teststrip import TestStrip


strip = TestStrip()
strip.set_pixel(1, Color(255, 255, 255))
strip.set_pixel(2, Color(255, 255, 255))
strip.set_pixel(3, Color(255, 255, 255))

strip.show()
strip.set_pixel(3, Color(255, 255, 255))
strip.set_pixel(4, Color(255, 255, 255))

strip.show()
strip.set_pixel(3, Color(255, 255, 255))
strip.set_pixel(4, Color(255, 255, 255))
strip.set_pixel(5, Color(255, 255, 255))
strip.set_pixel(6, Color(255, 255, 255))

strip.show()
strip.set_pixel(1, Color(255, 255, 255))
strip.set_pixel(2, Color(255, 255, 255))
strip.set_pixel(7, Color(255, 255, 255))

strip.show()
