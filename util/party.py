import random
from strip import Color


def color_generator(is_environment_bright):
    if is_environment_bright:
        return generate_bright_color()
    return generate_dark_color()


def generate_bright_color():
    color = []
    for x in range(3):
        if x > 1:
            if color[x - 1] > 150:
                color.append(random.randint(0, 51))
            else:
                color.append(random.randint(50, 151))
        else:
            color.append(random.randint(50, 256))

    return Color(color[0], color[1], color[2])


def generate_dark_color():
    color = []
    for x in range(3):
        if x > 1:
            if color[x - 1] > 150:
                color.append(random.randint(0, 21))
            else:
                color.append(random.randint(0, 101))
        else:
            color.append(random.randint(0, 21))

    return Color(color[0], color[1], color[2])
