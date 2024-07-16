from enum import Enum
import logging

tesseract_logger = logging.getLogger("Tesseract")
tesseract_logger.setLevel(logging.DEBUG)
tesseract_logger.propagate = False

tesseract_handler = logging.StreamHandler()
class TesseractFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO:  green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

tesseract_handler.setFormatter(TesseractFormatter())
tesseract_logger.addHandler(tesseract_handler)

class ModIdentifier(Enum):
        NONE = -1
        NoSliderVelocity = 1 << 0 # No Slider Velocity
        Speed05X = 1 << 1 # Speed 0.5x
        Speed06X = 1 << 2 # Speed 0.6x
        Speed07X = 1 << 3 # Speed 0.7x
        Speed08X = 1 << 4 # Speed 0.8x
        Speed09X = 1 << 5 # Speed 0.9x
        Speed11X = 1 << 6 # Speed 1.1x
        Speed12X = 1 << 7 # Speed 1.2x
        Speed13X = 1 << 8 # Speed 1.3x
        Speed14X = 1 << 9 # Speed 1.4x
        Speed15X = 1 << 10 # Speed 1.5x
        Speed16X = 1 << 11 # Speed 1.6x
        Speed17X = 1 << 12 # Speed 1.7x
        Speed18X = 1 << 13 # Speed 1.8x
        Speed19X = 1 << 14 # Speed 1.9x
        Speed20X = 1 << 15 # Speed 2.0x
        Strict = 1 << 16 # Makes the accuracy hit windows harder
        Chill = 1 << 17 # Makes the accuracy hit windows easier
        NoPause = 1 << 18 # Disallows pausing.
        Autoplay = 1 << 19 # The game automatically plays it.
        Paused = 1 << 20 # The user paused during gameplay.
        NoFail = 1 << 21 # Unable to fail during gameplay.
        NoongNotes = 1 << 22 # Converts Ns into regular notes.
        Randomize = 1 << 23 # Randomizes the playfield's lanes.
        Speed055X = 1 << 24 # Speed 0.55x
        Speed065X = 1 << 25 # Speed 0.65x
        Speed075X = 1 << 26 # Speed 0.75x
        Speed085X = 1 << 27 # Speed 0.85x
        Speed095X = 1 << 28 # Speed 0.95x
        Inverse = 1 << 29 # Converts regular notes into Ns and Ns into gaps.
        FullN = 1 << 30 # Converts regular notes into Ns keeps existing Ns.
        Mirror = 1 << 31 # Flips the map horizontally
        Coop = 1 << 32 # Allows multiple people to play together on one client
        Speed105X = 1 << 33 # Speed 1.05x
        Speed115X = 1 << 34 # Speed 1.15x
        Speed125X = 1 << 35 # Speed 1.25x
        Speed135X = 1 << 36 # Speed 1.35x
        Speed145X = 1 << 37 # Speed 1.45x
        Speed155X = 1 << 38 # Speed 1.55x
        Speed165X = 1 << 39 # Speed 1.65x
        Speed175X = 1 << 40 # Speed 1.75x
        Speed185X = 1 << 41 # Speed 1.85x
        Speed195X = 1 << 42 # Speed 1.95x
        HealthAdjust = 1 << 43 # Test mod for making long note windows easier
        NoMiss = 1 << 44 # You miss you die

class ProgressNumbers(Enum):
    BABY_STEPS = 1
    ABSOLUTELY_MARVELOUS = 1
    PERFECTIONIST = 1
    KEPT_YOU_PLAYING_HUH = 1000
    HUMBLE_BEGINNINGS = 25.00
    STEPPING_UP_THE_LADDER = 150.00
    WIDENING_YOUR_HORIZONS = 300.00
    REACHING_NEW_HEIGHTS = 500.00
    OUT_OF_THIS_WORLD = 600.00
    AREA_51 = 700.00
    ALIEN = 800.00
    EXTRATERRESTRIAL = 900.00
    ET = 1000.00
    QUOMBO = 500
    COMBOLICIOUS = 1000
    ONE_TWO_MAYWEATHER = 2500
    ITS_OVER_5000 = 5000
    _7500_DEEP = 7500
    TEN_THOUSAND = 10000
    BEGINNERS_LUCK = 10.00
    ITS_GETTING_HARDER = 15.00
    GOING_INSANE = 25.00
    YOURE_AN_EXPERT = 30.00
    PIECE_OF_CAKE = 35.00
    FAILURE_IS_AN_OPTION = 1000
    APPROACHING_THE_BLUE_ZENITH = 100
    CLICK_THE_ARROWS = 1_000_000
    FINGER_BREAKER = 100_000_000
    SLOWLY_BUT_SURELY = 1
    HE_WAS_NUMBER_ONE = 1
    STARVELOUS = 1
    