import dateutil.parser as dp
import hikari
import miru
import math
import libs.Types.TesseractTypes as Types
from libs.Types.TesseractTypes import tesseract_logger as Logger

emojis = {"X": "<:gradex:1262201488009072701>", "SS": "<:gradess:1262201547190702152>",
          "S": "<:grades:1262201580007067780>", "A": "<:gradea:1262201623577366609>",
          "B": "<:gradeb:1262201655097561209>", "C": "<:gradec:1262201670188929074>",
          "D": "<:graded:1262201683526684757>", "F": "<:gradef:1262728266205106258>"}

class ProfileEmbedv2(hikari.Embed):
    def generate_judgement_text(self) -> str:
        
        def get_percent_judgement(judgement_value: int) -> float:
            return (judgement_value / total_judgements) * 100
        
        attrs = vars(self.keys_stats)
        total_judgements = 0
        for attr in attrs.keys():
            if attr.startswith("total_") and attr not in ["total_miss", "total_score"]:
                total_judgements += getattr(self.keys_stats, attr)
        
        rows = [f"**Marvelous: {self.keys_stats.total_marvelous:,} ({get_percent_judgement(self.keys_stats.total_marvelous):.2f}%) | Perfect: {self.keys_stats.total_perfect:,} ({get_percent_judgement(self.keys_stats.total_perfect):.2f}%)**\n",
        f"**Great: {self.keys_stats.total_great:,} ({get_percent_judgement(self.keys_stats.total_great):.2f}%) | Good: {self.keys_stats.total_good:,} ({get_percent_judgement(self.keys_stats.total_good):.2f}%)**\n",
        f"**Okay: {self.keys_stats.total_okay:,} ({get_percent_judgement(self.keys_stats.total_okay):.2f}%) | Miss: {self.keys_stats.total_miss:,}**\n",
        f"**Total: {total_judgements:,}**"]
        
        max_length = 0
        for row in rows:
            if len(row) > max_length:
                max_length = len(row)
        result = ""
        for row in rows:
            result += row.center(max_length)
        return result
    
    
    def __init__(self, user_info: Types.QuaverUser, mode: int = None) -> None:
        self.user_info = user_info
        self.mode = mode
        if self.mode is None:
            try:
                self.mode = self.user_info.misc_information['default_mode']
            except KeyError:
                Logger.warning(f"Unable to set default_mode for ProfileEmbedv2 for {self.user_info.username}, defaulting to 4K")
                self.mode = 1
        match self.mode:
            case 1:
                self.keys_stats = user_info.stats_keys4
                keys_str = "4K"
            case 2:
                self.keys_stats = user_info.stats_keys7
                keys_str = "7K"
        super().__init__(title=f"{self.user_info.username}'s profile in {keys_str}",
                         description=f"**#{self.keys_stats.ranks['global']:,} (:flag_{self.user_info.country.lower()}: #{self.keys_stats.ranks['country']:,})**",
                         url=f"https://quavergame.com/user/{self.user_info.id}?mode={self.mode}", color=(0, 204, 204))
        
        self.set_thumbnail(self.user_info.avatar_url)
        self.set_footer(f"Registered at {dp.isoparse(self.user_info.time_registered).strftime('%d.%m.%Y %H:%M:%S')}")
        
        self.add_field(name="Total Score", value=f"**{self.keys_stats.total_score:,}**", inline=True)
        self.add_field(name="Overall Accuracy", value=f"**{self.keys_stats.overall_accuracy:.2f}%**", inline=True)
        self.add_field(name="Play Count", value=f"**{self.keys_stats.play_count:,}**", inline=True)

        self.add_field(name="Ranked Score", value=f"**{self.keys_stats.ranked_score:,}**", inline=True)
        self.add_field(name="Overall Rating", value=f"**{self.keys_stats.overall_performance_rating:.2f}**", inline=True)
        self.add_field(name="Max Combo", value=f"**{self.keys_stats.max_combo:,}**", inline=True)
        
        self.add_field(name="Grades", value=f"**{emojis['X']}: {self.keys_stats.count_grade_x} | {emojis['SS']}: {self.keys_stats.count_grade_ss} | {emojis['S']}: {self.keys_stats.count_grade_s} | {emojis['A']}: {self.keys_stats.count_grade_a} | {emojis['B']}: {self.keys_stats.count_grade_b} | {emojis['C']}: {self.keys_stats.count_grade_c} | {emojis['D']}: {self.keys_stats.count_grade_d}**")

        self.add_field(name="Judgements", value=self.generate_judgement_text())

class AchievementsEmbedv2(hikari.Embed):
        # TODO: Implement creating progress string for achievements
    def __init__(self, achievement_list: list[Types.QuaverAchievement], user_profile: Types.QuaverUser, page: int = 0) -> None:
        self.achievement_list = achievement_list
        self.user_profile = user_profile
        self.page = page
        super().__init__(title=f"**{self.user_profile.username}'s achievements**", color=(218, 165, 32))
        
        for i in range(5):
            valid_index = i + (5 * self.page)
            try:
                self.add_field(name=f"**#{valid_index + 1} {self.achievement_list[valid_index].name}**",
                               value=f"""{self.achievement_list[valid_index].description}
                               Difficulty: {self.achievement_list[valid_index].difficulty}
                               Status: {"Unlocked" if self.achievement_list[valid_index].is_unlocked else "Locked"}""")
            except IndexError:
                break

class RecentScoreEmbedv2(hikari.Embed):
    def generate_title(self) -> str:
        return f"{self.score.map.artist} - {self.score.map.title} ({self.score.map.difficulty_name})"
    
    def generate_desc(self) -> str | None:
        if self.score.is_personal_best:
            return "*A new personal best!*"
        else: 
            return None
    @staticmethod
    def get_original_difficulty(performance_rating: float, accuracy: float) -> float:
        return performance_rating / math.pow((accuracy / 98), 6)
    
    @staticmethod 
    def get_max_rating(base_difficulty: float) -> float:
        return base_difficulty * math.pow((100 / 98), 6)
    
    def __init__(self, scores: list[Types.QuaverScore], user_info: Types.QuaverUser) -> None:
        self.score = scores[0]
        self.user_info = user_info
        super().__init__(title=self.generate_title(), description=self.generate_desc(), url=f"https://quavergame.com/mapset/map/{self.score.map.id}", color=(0, 128, 255), timestamp=dp.isoparse(self.score.timestamp))

        self.set_author(name=f"Mapset by {self.score.map.creator_username}")
        
        self.add_field(name="Difficulty", value=f"{self.score.map.difficulty_rating:.2f}")

        self.add_field(name="Grade", value=emojis[self.score.grade], inline=True)
        self.add_field(name="Score", value=f"{self.score.total_score:,}", inline=True)
        self.add_field(name="Performance Rating", value=f"{self.score.performance_rating:.2f} / {self.get_max_rating(self.get_original_difficulty(self.score.performance_rating, self.score.accuracy)):.2f}", inline=True)
        
        self.add_field(name="Accuracy", value=f"{self.score.accuracy:.2f}%", inline=True)
        self.add_field(name="Misses", value=f"{self.score.count_miss:,}x", inline=True)
        self.add_field(name="Combo", value=f"{self.score.max_combo}x / {self.score.map.max_combo}x", inline=True)
        
        self.set_image(f"https://cdn.quavergame.com/mapsets/{self.score.map.mapset_id}.jpg")
        
        self.set_footer(text=f"Score by {self.user_info.username}", icon=self.user_info.avatar_url)