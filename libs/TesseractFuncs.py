import dotenv
import libs.TesseractGlobals as Globals

def get_dotenv() -> dict:
    return dotenv.dotenv_values(".env")

def process_achievement_list(user_info: dict, achievements_data: dict, lock_type: bool, top_score_7k: dict, top_score_4k: dict) -> dict:
    result = {}
    result['achievements'] = []
    user_info = user_info['user']
    result['username'] = user_info['info']['username']
    result['lock_type'] = lock_type
    for achievement in achievements_data['achievements']:
        if achievement['unlocked'] == lock_type:
            result['achievements'].append(achievement)
    for index, achievement in enumerate(result['achievements']):
        result['achievements'][index] = add_progress_str_to_achievement(achievement, get_max_playcount(user_info), get_max_total_rating(user_info),
                                                                        get_max_combo(user_info), get_max_map_rating(top_score_4k, top_score_7k),
                                                                        get_max_fails(user_info), get_max_top(user_info), get_max_hits(user_info),
                                                                        get_max_ranked_score(user_info))
    return result

def get_max_ranked_score(user_info: dict) -> int:
    return (user_info['keys4']['stats']['ranked_score'] if user_info['keys4']['stats']['ranked_score'] > user_info['keys7']['stats']['ranked_score'] else user_info['keys7']['stats']['ranked_score'])

def get_max_top(user_info: dict) -> int:
    return (user_info['keys4']['globalRank'] if user_info['keys4']['globalRank'] < user_info['keys7']['globalRank'] else user_info['keys7']['globalRank'])

def get_max_fails(user_info: dict) -> int:
    return (user_info['keys4']['stats']['fail_count'] if user_info['keys4']['stats']['fail_count'] > user_info['keys7']['stats']['fail_count'] else user_info['keys7']['stats']['fail_count'])

def get_max_combo(user_info: dict) -> int:
    return (user_info['keys4']['stats']['max_combo'] if user_info['keys4']['stats']['max_combo'] > user_info['keys7']['stats']['max_combo'] else user_info['keys7']['stats']['max_combo'])

def get_max_playcount(user_info: dict) -> int:
    return (user_info['keys4']['stats']['play_count'] if user_info['keys4']['stats']['play_count'] > user_info['keys7']['stats']['play_count'] else user_info['keys7']['stats']['play_count'])

            
def get_max_total_rating(user_info: dict) -> float:
    return (user_info['keys4']['stats']['overall_performance_rating'] if user_info['keys4']['stats']['overall_performance_rating'] > user_info['keys7']['stats']['overall_performance_rating'] else user_info['keys4']['stats']['overall_performance_rating'])
        
def get_max_map_rating(top_score_4k: dict, top_score_7k: dict) -> float:
    max_map_rating = 0.0
    if top_score_4k['scores'] not in [[], None] and top_score_7k['scores'] not in [[], None]:
        max_map_rating = (top_score_4k['scores'][0]['performance_rating'] if top_score_4k['scores'][0]['performance_rating'] > top_score_7k['scores'][0]['performance_rating'] else top_score_7k['scores'][0]['performance_rating'])
    else:
        if top_score_4k['scores'] in [[], None] and top_score_7k['scores'] in [[], None]:
            max_map_rating = 0.0
        elif top_score_4k['scores'] in [[], None]:
            max_map_rating = top_score_7k['scores'][0]['performance_rating']
        elif top_score_7k['scores'] in [[], None]:
            max_map_rating = top_score_4k['scores'][0]['performance_rating']
    return max_map_rating
    
def get_max_hits(user_info: dict) -> int:
    hits_4key = 0
    hits_7key = 0
    for key in user_info['keys4']['stats'].keys():
        if key.startswith("total_") and key not in ['total_score', 'total_pauses', 'total_miss']:
            hits_4key += user_info['keys4']['stats'][key]
    for key in user_info['keys7']['stats'].keys():
        if key.startswith("total_") and key not in ['total_score', 'total_pauses', 'total_miss']:
            hits_7key += user_info['keys7']['stats'][key]
    return (hits_4key if hits_4key > hits_7key else hits_7key)

def get_progress_percent(value: int | float, max_value: Globals.ProgressNumbers, reverse: bool = False) -> str:
    if not reverse:
        ratio = value / max_value.value
    else:
        ratio = max_value.value / value

    if ratio * 100 <= 100.00:
        return f"{ratio * 100:.2f}%"
    else:
        return f"{100.00:.2f}%"

def add_progress_str_to_achievement(achievement: dict, max_playcount: int, max_total_rating: float, max_combo: int, max_map_rating: float, max_fails: int, max_top: int, max_hits: int, max_ranked_score: int) -> dict:
    progress_str = "Progress: "
    match achievement['steam_api_name']:
        case "BABY_STEPS":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.BABY_STEPS.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.BABY_STEPS)})"
        case "ABSOLUTELY_MARVELOUS":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.ABSOLUTELY_MARVELOUS.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.ABSOLUTELY_MARVELOUS)})"
        case "PERFECTIONIST":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.PERFECTIONIST.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.PERFECTIONIST)})"
        case "KEPT_YOU_PLAYING_HUH":
            progress_str += f"{max_playcount} / {Globals.ProgressNumbers.KEPT_YOU_PLAYING_HUH.value} ({get_progress_percent(max_playcount, Globals.ProgressNumbers.KEPT_YOU_PLAYING_HUH)})"
        case "HUMBLE_BEGINNINGS":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.HUMBLE_BEGINNINGS.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.HUMBLE_BEGINNINGS)})"
        case "STEPPING_UP_THE_LADDER":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.STEPPING_UP_THE_LADDER.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.STEPPING_UP_THE_LADDER)})"
        case "WIDENING_YOUR_HORIZONS":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.WIDENING_YOUR_HORIZONS.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.WIDENING_YOUR_HORIZONS)})"
        case "REACHING_NEW_HEIGHTS":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.REACHING_NEW_HEIGHTS.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.REACHING_NEW_HEIGHTS)})"
        case "OUT_OF_THIS_WORLD":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.OUT_OF_THIS_WORLD.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.OUT_OF_THIS_WORLD)})"
        case "AREA_51":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.AREA_51.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.AREA_51)})"
        case "ALIEN":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.ALIEN.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.ALIEN)})"
        case "EXTRATERRESTRIAL":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.EXTRATERRESTRIAL.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.EXTRATERRESTRIAL)})"
        case "ET":
            progress_str += f"{max_total_rating:.2f} / {Globals.ProgressNumbers.ET.value} ({get_progress_percent(max_total_rating, Globals.ProgressNumbers.ET)})"
        case "QUOMBO":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers.QUOMBO.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers.QUOMBO)})"
        case "COMBOLICIOUS":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers.COMBOLICIOUS.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers.COMBOLICIOUS)})"
        case "ONE_TWO_MAYWEATHER":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers.ONE_TWO_MAYWEATHER.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers.ONE_TWO_MAYWEATHER)})"
        case "ITS_OVER_5000":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers.ITS_OVER_5000.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers.ITS_OVER_5000)})"
        case "7500_DEEP":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers._7500_DEEP.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers._7500_DEEP)})"
        case "TEN_THOUSAND":
            progress_str += f"{max_combo:,} / {Globals.ProgressNumbers.TEN_THOUSAND.value:,} ({get_progress_percent(max_combo, Globals.ProgressNumbers.TEN_THOUSAND)})"
        case "BEGINNERS_LUCK":
            progress_str += f"{max_map_rating:.2f} / {Globals.ProgressNumbers.BEGINNERS_LUCK.value} ({get_progress_percent(max_map_rating, Globals.ProgressNumbers.BEGINNERS_LUCK)})"
        case "ITS_GETTING_HARDER":
            progress_str += f"{max_map_rating:.2f} / {Globals.ProgressNumbers.ITS_GETTING_HARDER.value} ({get_progress_percent(max_map_rating, Globals.ProgressNumbers.ITS_GETTING_HARDER)})"
        case "GOING_INSANE":
            progress_str += f"{max_map_rating:.2f} / {Globals.ProgressNumbers.GOING_INSANE.value} ({get_progress_percent(max_map_rating, Globals.ProgressNumbers.GOING_INSANE)})"
        case "YOURE_AN_EXPERT":
            progress_str += f"{max_map_rating:.2f} / {Globals.ProgressNumbers.YOURE_AN_EXPERT.value} ({get_progress_percent(max_map_rating, Globals.ProgressNumbers.YOURE_AN_EXPERT)})"
        case "PIECE_OF_CAKE":
            progress_str += f"{max_map_rating:.2f} / {Globals.ProgressNumbers.PIECE_OF_CAKE.value} ({get_progress_percent(max_map_rating, Globals.ProgressNumbers.PIECE_OF_CAKE)})"
        case "FAILURE_IS_AN_OPTION":
            progress_str += f"{max_fails:,} / {Globals.ProgressNumbers.FAILURE_IS_AN_OPTION.value:,} ({get_progress_percent(max_fails, Globals.ProgressNumbers.FAILURE_IS_AN_OPTION)})"
        case "APPROACHING_THE_BLUE_ZENITH":
            progress_str += f"{max_top:,} / {Globals.ProgressNumbers.APPROACHING_THE_BLUE_ZENITH.value} ({get_progress_percent(max_top, Globals.ProgressNumbers.APPROACHING_THE_BLUE_ZENITH, True)})"
        case "CLICK_THE_ARROWS":
            progress_str += f"{max_hits:,} / {Globals.ProgressNumbers.CLICK_THE_ARROWS.value:,} ({get_progress_percent(max_hits, Globals.ProgressNumbers.CLICK_THE_ARROWS)})"
        case "FINGER_BREAKER":
            progress_str += f"{max_ranked_score:,} / {Globals.ProgressNumbers.FINGER_BREAKER.value:,} ({get_progress_percent(max_ranked_score, Globals.ProgressNumbers.FINGER_BREAKER)})"
        case "SLOWLY_BUT_SURELY":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.SLOWLY_BUT_SURELY.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.SLOWLY_BUT_SURELY)})"
        case "HE_WAS_NUMBER_ONE":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.HE_WAS_NUMBER_ONE.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.HE_WAS_NUMBER_ONE)})"
        case "STARVELOUS":
            progress_str += f"{int(achievement['unlocked'])} / {Globals.ProgressNumbers.STARVELOUS.value} ({get_progress_percent(int(achievement['unlocked']), Globals.ProgressNumbers.STARVELOUS)})"
    achievement['progress_str'] = progress_str
    return achievement