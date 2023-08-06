class Color(object):

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def red(self):
        return self.red

    def green(self):
        return self.green

    def blue(self):
        return self.blue

    def values(self):
        return [self.red, self.green, self.blue]

    def __str__(self):
        return "{R = " + str(self.red)   \
            + ", G = " + str(self.green)   \
            + ", B = " + str(self.blue) + "}"

class Colors(object):
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    YELLOW = Color(255, 255, 0)
    MAGENTA = Color(255, 0, 255)
    CYAN = Color(0, 255, 255)
