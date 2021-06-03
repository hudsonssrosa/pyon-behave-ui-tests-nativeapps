from django.utils.termcolors import colorize


class TextColor:

    """
        black = lambda text: '\033[0;30m' + text + '\033[0m'
        blue = lambda text: '\033[0;34m' + text + '\033[0m'
        cyan = lambda text: '\033[0;36m' + text + '\033[0m'
        green = lambda text: '\033[0;32m' + text + '\033[0m'
        magenta = lambda text: '\033[0;35m' + text + '\033[0m'
        red = lambda text: '\033[0;31m' + text + '\033[0m'
        white = lambda text: '\033[0;37m' + text + '\033[0m'
        yellow = lambda text: '\033[0;33m' + text + '\033[0m'
    """

    @staticmethod
    def black(text):
        black = colorize(text, fg="black")
        return black

    @staticmethod
    def blue(text):
        blue = colorize(text, fg="blue")
        return blue

    @staticmethod
    def cyan(text):
        cyan = colorize(text, fg="cyan")
        return cyan

    @staticmethod
    def green(text):
        green = colorize(text, fg="green")
        return green

    @staticmethod
    def magenta(text):
        magenta = colorize(text, fg="magenta")
        return magenta

    @staticmethod
    def red(text):
        red = colorize(text, fg="red")
        return red

    @staticmethod
    def white(text):
        white = colorize(text, fg="white")
        return white

    @staticmethod
    def yellow(text):
        yellow = colorize(text, fg="yellow")
        return yellow
