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

class QuaverAPIResponse:
    def __init__(self, status_code: int, content: dict, page: int = None) -> None:
        self.status_code = status_code
        self.content = content
        self.page = page

class Serializable:
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        if type(data) == QuaverAPIResponse:
            self.data = data.content
        else:
            self.data = data
        self.serialize()
    
    def serialize(self):
        data = self.data
        if len(data.keys()) > 0:
            for key in data.keys():
                try:
                    if data[key] is not None:
                        setattr(self, key, data[key])
                    else:
                        tesseract_logger.warning(f"Unable to serialize attribute {key} for {self.__class__.__name__}: Attribute is None in data, continuing")
                except AttributeError:
                    tesseract_logger.warning(f"Failed to serialize attribute {key} for {self.__class__.__name__}: Attribute not found in object, continuing")
                  
class QuaverUser(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.id: int = None
        self.steam_id: int = None
        self.username: str = None
        self.time_registered: str = None
        self.latest_activity: str = None
        self.country: str = None
        self.avatar_url: str = None
        self.title: str = None
        self.donator_end_time: str = None
        self.misc_information: dict = None
        self.stats_keys4: dict | QuaverKeysStats = None
        self.stats_keys7: dict | QuaverKeysStats = None
                
        super().__init__(data)
        self.stats_keys4 = QuaverKeysStats(self.stats_keys4)
        self.stats_keys7 = QuaverKeysStats(self.stats_keys7)
        
class QuaverKeysStats(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.ranks: dict = None
        self.total_score: int = None
        self.ranked_score: int = None
        self.overall_accuracy: float = None
        self.overall_performance_rating: float = None
        self.play_count: int = None
        self.fail_count: int = None
        self.max_combo: int = None
        self.total_marvelous: int = None
        self.total_perfect: int = None
        self.total_great: int = None
        self.total_good: int = None
        self.total_okay: int = None
        self.total_miss: int = None
        self.count_grade_x: int = None
        self.count_grade_ss: int = None
        self.count_grade_s: int = None
        self.count_grade_a: int = None
        self.count_grade_b: int = None
        self.count_grade_c: int = None
        self.count_grade_d: int = None
        
        super().__init__(data)

class QuaverAchievement(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.id: int = None
        self.difficulty: str = None
        self.steam_api_name: str = None
        self.name: str = None
        self.description: str = None
        self.is_unlocked: bool = None
        self.progress_str: str = None
        
        super().__init__(data)
        
    # TODO: Implement creating progress string for achievements    
        
    # def create_progress_str(self, user: QuaverUser, reverse: bool = False):
    #     progress_str: str = "Progress: "
    #     if not reverse:
    #         pass

class QuaverScore(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.id: int = None
        self.user_id: int = None
        self.map_md5: str = None
        self.replay_md5: str = None
        self.timestamp: str = None
        self.is_personal_best: bool = None
        self.performance_rating: float = None
        self.modifiers: int = None
        self.failed: bool = None
        self.total_score: int = None
        self.accuracy: float = None
        self.max_combo: int = None
        self.count_marvelous: int = None
        self.count_perfect: int = None
        self.count_great: int = None
        self.count_good: int = None
        self.count_okay: int = None
        self.count_miss: int = None
        self.grade: str = None
        self.map: dict | QuaverMapInfo = None
        
        super().__init__(data)
        self.map = QuaverMapInfo(self.map)
        
class QuaverMapInfo(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.id: int = None
        self.mapset_id: int = None
        self.md5: str = None
        self.alternative_md5: str = None
        self.creator_id: int = None
        self.creator_username: str = None
        self.game_mode: int = None
        self.ranked_status: int = None
        self.artist: str = None
        self.title: str = None
        self.difficulty_name: str = None
        self.length: int = None
        self.bpm: int = None
        self.difficulty_rating: float = None
        self.count_hitobject_normal: int = None
        self.count_hit_object_long: int = None
        self.long_note_percentage: float = None
        self.max_combo: int = None
        self.play_count: int = None
        self.play_attempts: int = None
        
        super().__init__(data)
        
class QuaverMapset(Serializable):
    def __init__(self, data: QuaverAPIResponse | dict) -> None:
        self.id: int = None
        self.package_md5: str = None
        self.creator_id: int = None
        self.creator_username: str = None
        self.artist: str = None
        self.title: str = None
        self.description: str = None
        self.date_submitted: str = None
        self.is_visible: bool = None
        self.is_explicit: bool = None
        
        super().__init__(data)