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

class AchievementsPagesView(miru.View):
    def __init__(self, achievement_data: list[dict], username: str, lock_type: bool) -> None:
        self.achievement_data = achievement_data
        self.username = username
        self.lock_type = lock_type
        self.page = 0
        self.total_pages = math.floor((len(achievement_data) / 5))
        super().__init__(timeout=None, autodefer=True)
        if self.page == 0:
            self.get_item_by_id('back').disabled = True

    
    @miru.button(emoji="⬅", custom_id="back")
    async def go_back_page(self, ctx: miru.ViewContext, button: miru.Button):
        self.page -= 1
        if self.page == 0:
            button.disabled = True
        self.get_item_by_id('next').disabled = False
        await ctx.message.edit(AchievementsEmbed(self.achievement_data, self.username, self.lock_type, self.page), components=self)
    
    @miru.button(emoji="➡", custom_id="next")
    async def go_next_page(self, ctx: miru.ViewContext, button: miru.Button):
        if self.page != self.total_pages:
            self.page += 1
            if self.page == self.total_pages:
                button.disabled = True
            self.get_item_by_id('back').disabled = False
        await ctx.message.edit(AchievementsEmbed(self.achievement_data, self.username, self.lock_type, self.page), components=self)

class GamemodeSelectView(miru.View):
    def __init__(self, profile_data: dict) -> None:
        self.profile_data = profile_data
        super().__init__(timeout=None, autodefer=True)

    @miru.button("4K", style=hikari.ButtonStyle.SUCCESS, custom_id="4k", disabled=True)
    async def switch_to_4k(self, ctx: miru.ViewContext, button: miru.Button):
        button.disabled = True
        self.get_item_by_id("7k").disabled = False
        await ctx.message.edit(ProfileEmbed(self.profile_data, 1), components=self)
    
    @miru.button("7K", style=hikari.ButtonStyle.PRIMARY, custom_id="7k")
    async def switch_to_7k(self, ctx: miru.ViewContext, button: miru.Button):
        button.disabled = True
        self.get_item_by_id("4k").disabled = False
        await ctx.message.edit(ProfileEmbed(self.profile_data, 2), components=self)

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
        

class ProfileEmbed(hikari.Embed):
    def count_judge_percents(self) -> dict:
        judgements = {}
        total_judgements = 0
        for judgement in self.keys_info['stats'].keys():
            if judgement.startswith("total_") and judgement not in ["total_score", "total_pauses"]:
                if judgement != 'total_miss':
                    total_judgements += self.keys_info['stats'][judgement]
                judgements[judgement] = 0.0
        for judgement in judgements.keys():
            if judgement != 'total_miss':
                judgements[judgement] = (self.keys_info['stats'][judgement] / total_judgements) * 100
        judgements['total_judgements'] = total_judgements
        return judgements
    
    def create_judgements_text(self, keys_info: dict, judgements_percents: dict) -> str:
        max_length = 0
        
        rows = [f"**Marvelous: {keys_info['stats']['total_marv']:,} ({judgements_percents['total_marv']:.2f}%) | Perfect: {keys_info['stats']['total_perf']:,} ({judgements_percents['total_perf']:.2f}%)**\n",
        f"**Great: {keys_info['stats']['total_great']:,} ({judgements_percents['total_great']:.2f}%) | Good: {keys_info['stats']['total_good']:,} ({judgements_percents['total_good']:.2f}%)**\n",
        f"**Okay: {keys_info['stats']['total_okay']:,} ({judgements_percents['total_okay']:.2f}%) | Miss: {keys_info['stats']['total_miss']:,}**\n",
        f"**Total: {judgements_percents['total_judgements']:,}**"]
        
        for row in rows:
            if len(row) > max_length:
                max_length = len(row)
        result = ""
        for row in rows:
            row.center(max_length)
            result += row
        return result
    
    def __init__(self, profile_data: dict, mode: int = 1):
        self.profile_data = profile_data
        self.profile_info = profile_data['info']
        match mode:
            case 1:
                self.keys_info = profile_data['keys4']
                self.mode_str = "4K"
            case 2:
                self.keys_info = profile_data['keys7']
                self.mode_str = "7K"
            case _:
                raise ValueError("Wrong mode int")
        self.register_time = dp.isoparse(self.profile_info['time_registered']).strftime("%d.%m.%Y %H:%M:%S")
        judgements_percents = self.count_judge_percents()
        
        super().__init__(title=f"{self.profile_info['username']}'s profile in {self.mode_str}", 
                         description=f"**#{self.keys_info['globalRank']} (:flag_{self.profile_info['country'].lower()}: #{self.keys_info['countryRank']})**",
                        url=f"https://quavergame.com/user/{self.profile_info['id']}?mode={mode}", color=(0, 204, 204))
        
        self.set_thumbnail(self.profile_info['avatar_url'])
        self.set_footer(f"Registered at {self.register_time}")
        
        self.add_field(name="Total Score", value=f"**{self.keys_info['stats']['total_score']:,}**", inline=True)
        self.add_field(name="Overall Accuracy", value=f"**{self.keys_info['stats']['overall_accuracy']:.2f}%**", inline=True)
        self.add_field(name="Play Count", value=f"**{self.keys_info['stats']['play_count']:,}**", inline=True)

        self.add_field(name="Ranked Score", value=f"**{self.keys_info['stats']['ranked_score']:,}**", inline=True)
        self.add_field(name="Overall Rating", value=f"**{self.keys_info['stats']['overall_performance_rating']:.2f}**", inline=True)
        self.add_field(name="Max Combo", value=f"**{self.keys_info['stats']['max_combo']:,}**", inline=True)
        
        self.add_field(name="Grades", value=f"**{emojis['X']}: {self.keys_info['stats']['count_grade_x']} | {emojis['SS']}: {self.keys_info['stats']['count_grade_ss']} | {emojis['S']}: {self.keys_info['stats']['count_grade_s']} | {emojis['A']}: {self.keys_info['stats']['count_grade_a']} | {emojis['B']}: {self.keys_info['stats']['count_grade_b']} | {emojis['C']}: {self.keys_info['stats']['count_grade_c']} | {emojis['D']}: {self.keys_info['stats']['count_grade_d']}**")

        self.add_field(name="Judgements", value=self.create_judgements_text(self.keys_info, judgements_percents))
        
        self.add_field(name="Achievements Progress", value=f"**{self.profile_data['achievement_str']}**")
        
class AchievementsEmbed(hikari.Embed):
    def __init__(self, achievement_data: list[dict], username: str, lock_type: bool, page: int = 0):
        title = ""
        match lock_type:
            case True:
                title = f"**{username}'s unlocked achievements**"
            case False:
                title = f"**{username}'s locked achievements**"
        super().__init__(title=title, color=(218, 165, 32))
        self.set_footer(f"Page {page + 1}/{math.ceil((len(achievement_data) / 5))}")
        
        for i in range(5):
            try:
                self.add_field(name=f"**#{i + (5 * page) + 1} {achievement_data[i + (5 * page)]['name']}**",
                            value=f"""{achievement_data[i + (5 * page)]['description']}
                            Difficulty: {achievement_data[i + (5 * page)]['difficulty']}
                            {achievement_data[i + (5 * page)]['progress_str']}""")
            except IndexError:
                break
            
class RecentScoreEmbed(hikari.Embed):
    def generate_title(self) -> str:
        title = ""
        mods_string = ""
        if self.score_info['mods_string'] != "None":
            mods_string = f" +{self.score_info['mods_string']}"
        title = f"{self.score_info['map']['artist']} - {self.score_info['map']['title']} ({self.score_info['map']['difficulty_name']}){mods_string}"
        return title
    
    def generate_desc(self) -> str:
        desc = ""
        if self.score_info['personal_best']:
            desc = "*A new personal best!*"
        return desc
    
    @staticmethod
    def calculate_base_diff_from_rating(rating: float, acc: float) -> float:
        base_difficulty = rating / math.pow(acc / 98, 6)
        return base_difficulty
    
    @staticmethod
    def calculate_maximum_rating(base_diff: float) -> float:
        maximum_rating = base_diff * math.pow(100 / 98, 6)
        return maximum_rating
    
    def __init__(self, score_info: dict, author_avatar: str, player_avatar: str, player_name: str, map_max_combo: int, **kwargs):
        self.score_info = score_info['scores'][0]
        if kwargs['original_diff'] is not None:
            self.base_difficulty = kwargs['original_diff']
            self.max_rating = self.calculate_maximum_rating(kwargs['original_diff'])
        else:
            self.base_difficulty = self.calculate_base_diff_from_rating(self.score_info['performance_rating'], self.score_info['accuracy'])
            self.max_rating = self.calculate_maximum_rating(self.calculate_base_diff_from_rating(self.score_info['performance_rating'], self.score_info['accuracy']))
        super().__init__(title=self.generate_title(), description=self.generate_desc(), url=f"https://quavergame.com/mapset/map/{self.score_info['map']['id']}", color=(0, 128, 255) , timestamp=dp.isoparse(self.score_info['time']))
        
        self.set_author(name=f"Mapset by {self.score_info['map']['creator_username']}", icon=author_avatar)
        
        self.add_field(name="Difficulty", value=f"{self.base_difficulty:.2f}")
        
        self.add_field(name="Grade", value=emojis[self.score_info['grade']], inline=True)
        self.add_field(name="Score", value=f"{self.score_info['total_score']:,}", inline=True)
        self.add_field(name="Performance Rating", value=f"{self.score_info['performance_rating']:.2f} / {self.max_rating:.2f}", inline=True)
        
        self.add_field(name="Accuracy", value=f"{self.score_info['accuracy']:.2f}%", inline=True)
        self.add_field(name="Ratio", value=f"{self.score_info['ratio']:.2f}", inline=True)
        self.add_field(name="Combo", value=f"{self.score_info['max_combo']}x / {map_max_combo}x", inline=True)
        
        self.set_image(f"https://cdn.quavergame.com/mapsets/{self.score_info['map']['mapset_id']}.jpg")
        
        self.set_footer(text=f"Score by {player_name}", icon=player_avatar)