
import logging
from os import environ
import sys


# detect ANSI code availability for root logger
if environ.get('TERM') and environ.get('TERM') != 'dumb':
    _ansi = True
else:
    _ansi = False


class AnsiColors:
    """ANSI escape code

    See also: <http://en.wikipedia.org/wiki/ANSI_escape_code>.
    """
    RESET = 0
    BOLD = 1
    UNDERLINE = 4
    NEGATIVE = 7
    NO_BOLD = 21
    NO_UNDERLINE = 24
    POSITIVE = 27
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    LIGHT_GRAY = 37
    DEFAULT = 39
    BLACK_BACKGROUND = 40
    RED_BACKGROUND = 41
    GREEN_BACKGROUND = 42
    YELLOW_BACKGROUND = 43
    BLUE_BACKGROUND = 44
    MAGENTA_BACKGROUND = 45
    CYAN_BACKGROUND = 46
    LIGHT_GRAY_BACKGROUND = 47
    DEFAULT_BACKGROUND = 49
    DARK_GRAY = 90                  # xterm
    LIGHT_RED = 91                  # xterm
    LIGHT_GREEN = 92                # xterm
    LIGHT_YELLOW = 93               # xterm
    LIGHT_BLUE = 94                 # xterm
    LIGHT_MAGENTA = 95              # xterm
    LIGHT_CYAN = 96                 # xterm
    WHITE = 97                      # xterm
    DARK_GRAY_BACKGROUND = 100      # xterm
    LIGHT_RED_BACKGROUND = 101      # xterm
    LIGHT_GREEN_BACKGROUND = 102    # xterm
    LIGHT_YELLOW_BACKGROUND = 103   # xterm
    LIGHT_BLUE_BACKGROUND = 104     # xterm
    LIGHT_MAGENTA_BACKGROUND = 105  # xterm
    LIGHT_CYAN_BACKGROUND = 106     # xterm
    WHITE_BACKGROUND = 107          # xterm

    @staticmethod
    def fullcode(x):
        return '\033[{}m'.format(x)


class Logger(logging.getLoggerClass()):
    """Level-color mapping"""
    COLORMAP = {
        logging.DEBUG: (AnsiColors.fullcode(AnsiColors.LIGHT_BLUE),
                        AnsiColors.fullcode(AnsiColors.RESET)),
        logging.INFO: (AnsiColors.fullcode(AnsiColors.LIGHT_GREEN),
                       AnsiColors.fullcode(AnsiColors.RESET)),
        logging.WARNING: (AnsiColors.fullcode(AnsiColors.LIGHT_YELLOW),
                          AnsiColors.fullcode(AnsiColors.RESET)),
        logging.ERROR: (AnsiColors.fullcode(AnsiColors.LIGHT_RED),
                        AnsiColors.fullcode(AnsiColors.RESET)),
        logging.CRITICAL: (AnsiColors.fullcode(AnsiColors.LIGHT_RED) +
                           AnsiColors.fullcode(AnsiColors.BOLD),
                           AnsiColors.fullcode(AnsiColors.RESET)),
    }

    @staticmethod
    def printlog(logger, is_ansi, level, msg, *args, **kwargs):
        """Call the parent logger, enhanced with ANSI colors."""
        if is_ansi:
            code = Logger.COLORMAP.get(level, Logger.COLORMAP[logging.INFO])
            sys.stderr.write(code[0])
        logger.log(level, msg, *args, **kwargs)
        if is_ansi:
            sys.stderr.write(code[1])
            sys.stderr.flush()

    def __init__(self, name=None, is_ansi=False):
        self.name = name
        self.is_ansi = is_ansi

        self.logger = logging.getLogger(name)

    def log(self, level, *msg_args, **kwargs):
        """Log a message."""
        msg, args = (msg_args[0], msg_args[1:]) if msg_args else ('', [])
        Logger.printlog(self.logger, self.is_ansi, level, msg, *args, **kwargs)

    def d(self, *msg_args, **kwargs):
        """Log a debugging message."""
        self.log(logging.DEBUG, *msg_args, **kwargs)

    def i(self, *msg_args, **kwargs):
        """Log an informational message."""
        self.log(logging.INFO, *msg_args, **kwargs)

    def w(self, *msg_args, **kwargs):
        """Log a warning message."""
        self.log(logging.WARNING, *msg_args, **kwargs)

    def e(self, *msg_args, **kwargs):
        """Log an error message."""
        self.log(logging.ERROR, *msg_args, **kwargs)

    def wtf(self, *msg_args, **kwargs):
        """What a Terrible Failure!"""
        self.log(logging.CRITICAL, *msg_args, **kwargs)


def log(level, *msg_args, **kwargs):
    """Log a message. (root)"""
    msg, args = (msg_args[0], msg_args[1:]) if msg_args else ('', [])
    Logger.printlog(logging, _ansi, level, msg, *args, **kwargs)


def d(*msg_args, **kwargs):
    """Log a debugging message. (root)"""
    log(logging.DEBUG, *msg_args, **kwargs)


def i(*msg_args, **kwargs):
    """Log an informational message. (root)"""
    log(logging.INFO, *msg_args, **kwargs)


def w(*msg_args, **kwargs):
    """Log a warning message. (root)"""
    log(logging.WARNING, *msg_args, **kwargs)


def e(*msg_args, **kwargs):
    """Log an error message. (root)"""
    log(logging.ERROR, *msg_args, **kwargs)


def wtf(*msg_args, **kwargs):
    """What a Terrible Failure! (root)"""
    log(logging.CRITICAL, *msg_args, **kwargs)


def get_logger(name):
    return Logger(name, _ansi)


def init_logging(level=logging.WARNING,
                 format='%(asctime)s  %(name)s  %(levelname)-8s  %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S',
                 **kwargs):
    """Initialize the logging system."""
    logging.basicConfig(level=level,
                        format=format,
                        datefmt=datefmt,
                        **kwargs)


def stop_logging():
    """Shut down the logging system."""
    logging.shutdown()
