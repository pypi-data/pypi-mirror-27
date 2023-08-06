"""
Color utilities for Charts and Datasets
"""


class Color:
    DEFAULT_COLOR = 'rgb(220,220,220, 0.5)'
    ORANGE = 'rgba(253, 163, 49, 0.5)'
    LIGHT_GREY = 'rgba(208, 208, 208, 0.5)'
    PALE_YELLOW = 'rgba(253, 218, 49, 0.5)'
    BLUE900 = 'rgba(13, 71, 161, 0.8)'
    BLUE800 = 'rgba(21, 101, 192, 0.8)'
    BLUE600 = 'rgba(30, 136, 229, 0.8)'
    BLUE400 = 'rgba(66, 165, 245, 0.8)'
    BLUE200 = 'rgba(144, 202, 249, 0.7)'
    LIGHT_BLUE = 'rgba(77, 208, 225, 0.5)'
    INDIGO900 = 'rgba(26, 35, 126, 0.9)'
    INDIGO400 = 'rgba(92, 107, 192, 0.9)'
    INDIGO200 = 'rgba(159, 168, 218, 0.8)'
    PINK900 = 'rgba(136, 14, 79, 0.8)'
    GREEN900 = 'rgba(51, 105, 30, 0.8)'
    GREEN800 = 'rgba(46, 125, 50, 0.8)'
    PURPLE900 = 'rgba(74, 20, 140, 0.6)'
    DEEP_PURPLE900 = 'rgba(49, 27, 146, 0.5)'
    RED900 = 'rgba(183, 28, 28, 0.8)'
    RED800 = 'rgba(198, 40, 40, 0.8)'
    RED600 = 'rgba(229, 57, 53, 0.8)'
    GREY700 = 'rgba(97, 97, 97, 0.7)'
    BLUE_A700 = 'rgba(48, 79, 254, 0.8)'
    YELLOW700 = 'rgba(251, 192, 45, 0.7)'

    def __init__(self, r, g, b, opacity):
        self.r = r
        self.g = g
        self.b = b
        self.opacity = opacity

    def __repr__(self):
        return 'rgba({r}, {g}, {b}, {opacity})'.format(r=self.r, g=self.g, b=self.b, opacity=self.opacity)

    @staticmethod
    def get_rgba(r, g, b, opacity=0.5):
        return 'rgba({r}, {g}, {b}, {opacity})'.format(r=r, g=g, b=b, opacity=opacity)


# default color order for subsequent datasets
COLOR_ORDER = (
    Color.GREEN800,
    Color.BLUE800,
    Color.RED800,
    Color.ORANGE,
    Color.PALE_YELLOW,
    Color.PURPLE900,
    Color.INDIGO200
)


def color_queue(color_order=COLOR_ORDER):
    for color in color_order:
        yield color
    while 1337:
        yield Color.DEFAULT_COLOR
