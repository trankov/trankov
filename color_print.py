# Styles text string with formatting defined by chaining notation.
#
#
#   >>> from color_print import Style
#
#
# Immediate styling:
#
#   >>> Style('weighted text').bold
#   >>> Style('bold italic text').italic.bold
#
#
# Styling with template:
#
#   >>> err = Style().color(Style.BG_RED).color(Style.WHITE).bold
#   >>> err.text = ' Error message '
#   >>> err
#
#
# Just display some text using the same template...
# Note: `display` method doesn't change `text` proprerty.
#
#   >>> print(err.display(' Another error message '))
#
#
# Styling one text for many times:
#
#   >>> text = Style(' some text ')
#   >>> text.rgbcolors((200,200,0), (0, 33, 128))
#   >>> text.clear().bg256(200)
#   >>> text.bold
#   >>> text.clear().colors(Style.YELLOW, Style.BG_RED).strike
#
#
# Available modifications and properties:
# ---------------------------------------
#   Style.BLACK, Style.BG_WHITE, ...                color constants
#   text                                            text to display
#   display(text: str)                              display text disposable
#   bold, faint, italic, underline,
#   blink, fastblink, invert,
#   conceal, strike                                 text decorations
#   color(color_code: int)                          apply single 16-bit color code
#   colors(*args)                                   apply one or two 16-bit color codes
#   bg256(color_code: int)                          apply 256-bit color code to background
#   fg256(color_code: int)                          apply 256-bit color code to foreground
#   colors256(foreground: int, background: int)     apply 256-bit colors to foreground and background
#   bgrgb(r: int, g: int, b: int)                   apply (r, g, b) color to background
#   fgrgb(r: int, g: int, b: int)                   apply (r, g, b) color to foreground
#   rgbcolors(foreground: tuple, background: tuple) apply (r, g, b) colors to foreground and background
#   clear()                                         clear template in full
#


class Style(object):

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97
    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_WHITE = 47
    BG_BRIGHT_BLACK = 100
    BG_BRIGHT_RED = 101
    BG_BRIGHT_GREEN = 102
    BG_BRIGHT_YELLOW = 103
    BG_BRIGHT_BLUE = 104
    BG_BRIGHT_MAGENTA = 105
    BG_BRIGHT_CYAN = 106
    BG_BRIGHT_WHITE = 107

    def __init__(self, string = ''):
        self._result_string = string
        self._template = ''

    def clear(self):
        self._template = ''
        return self

    def _transform(self, transformation):
        '''Supplements the template with a new value'''
        self._template = '\033[{}m{}'.format(transformation, self._template)

    @property
    def text(self):
        '''Return the text which will be stylized'''
        return self._result_string

    @text.setter
    def text(self, value):
        self._result_string = str(value)
        return self

    def display(self, value=''):
        if value:
            return '{}{}\033[m'.format(self._template, value)
        return self

    @property
    def bold(self):
        self._transform('1')
        return self

    @property
    def faint(self):
        self._transform('2')
        return self

    @property
    def italic(self):
        self._transform('3')
        return self

    @property
    def underline(self):
        self._transform('4')
        return self

    @property
    def blink(self):
        self._transform('5')
        return self

    @property
    def fastblink(self):
        self._transform('6')
        return self

    @property
    def invert(self):
        self._transform('7')
        return self

    @property
    def conceal(self):
        self._transform('8')
        return self

    @property
    def strike(self):
        self._transform('9')
        return self

    def color(self, color_code=0):
        '''
        Add one color value to template.
          n = Style().color(Style.RED)

        '''
        self._transform(color_code)
        return self


    def colors(self, *args):
        '''
        Adding 16-bit color codes from `args` to template. You can send
        any number of parameters, but only two first of them will be taken.
          Style('green text on blue').color(Style.GREEN, Style.BG_BLUE)

        '''
        [self._transform(i) for i in args[:2] if args]
        return self


    def bg256(self, color_code=0):
        self._transform('48;5;{}'.format(color_code))
        return self

    def fg256(self, color_code=0):
        self._transform('38;5;{}'.format(color_code))
        return self

    def colors256(self, foreground=0, background=0):
        self._transform('38;5;{}'.format(foreground))
        self._transform('48;5;{}'.format(background))
        return self


    def bgrgb(self, r=0, g=0, b=0):
        self._transform('48;2;{};{};{}'.format(r, g, b))
        return self

    def fgrgb(self, r=0, g=0, b=0):
        self._transform('38;2;{};{};{}'.format(r, g, b))
        return self


    def rgbcolors(self, foreground=(0, 0, 0), background=(0, 0, 0)):

        if any((type(background) is not tuple,
                type(foreground) is not tuple)):
            return self

        if any((len(foreground) != 3,
                len(background) != 3)):
            return self

        self._transform('38;2;{};{};{}'.format(*foreground))
        self._transform('48;2;{};{};{}'.format(*background))
        return self


    def __str__(self):
        return '{}{}\033[m'.format(self._template, self._result_string)

    def __repr__(self):
        return self.__str__()
