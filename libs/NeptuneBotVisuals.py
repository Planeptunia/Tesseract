from datetime import timedelta
import dateutil.parser as dp
import hikari
import miru

emojis = {"X": "<:gradex:1262201488009072701>", "SS": "<:gradess:1262201547190702152>",
          "S": "<:grades:1262201580007067780>", "A": "<:gradea:1262201623577366609>",
          "B": "<:gradeb:1262201655097561209>", "C": "<:gradec:1262201670188929074>",
          "D": "<:graded:1262201683526684757>", "marv": "<:judgemarv:1262388667314470954>",
          "perf": "<:judgeperf:1262388692593545267>", "great": "<:judgegreat:1262388714592800898>",
          "good": "<:judgegood:1262388734901354569>", "okay": "<:judgeokay:1262388748872581180>",
          "miss": "<:judgemiss:1262388763900903504>"}

class GamemodeSelectView(miru.View):
    def __init__(self, profile_data: dict) -> None:
        self.profile_data = profile_data
        super().__init__(timeout=None, autodefer=True)
    @miru.text_select(
        placeholder = "Select Mode",
        options = [
            miru.SelectOption(label = "4K"),
            miru.SelectOption(label = "7K")
        ]
    )
    async def get_mode_option(self, ctx: miru.ViewContext, select: miru.TextSelect):
        match select.values[0]:
            case "4K":
                self.mode = 1
            case "7K":
                self.mode = 2
        await ctx.message.edit(ProfileEmbed(self.profile_data, self.mode))

class ProfileEmbed(hikari.Embed):
    def count_judge_percents(self) -> dict:
        judgements = {}
        total_judgements = 0
        for judgement in self.keys_info['stats'].keys():
            if judgement.startswith("total") and judgement != "total_score":
                total_judgements += self.keys_info['stats'][judgement]
                judgements[judgement] = 0.0
        for judgement in judgements.keys():
            judgements[judgement] = (self.keys_info['stats'][judgement] / total_judgements) * 100
        judgements['total_judgements'] = total_judgements
        return judgements
    
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

        self.add_field(name="Judgements", value=f"""**Marvelous: {self.keys_info['stats']['total_marv']:,} ({judgements_percents['total_marv']:.2f}%) | Perfect: {self.keys_info['stats']['total_perf']:,} ({judgements_percents['total_perf']:.2f}%)
                    Great: {self.keys_info['stats']['total_great']:,} ({judgements_percents['total_great']:.2f}%) | Good: {self.keys_info['stats']['total_good']:,} ({judgements_percents['total_good']:.2f}%)
                    Okay: {self.keys_info['stats']['total_okay']:,} ({judgements_percents['total_okay']:.2f}%) | Miss: {self.keys_info['stats']['total_miss']:,} ({judgements_percents['total_miss']:.2f}%)
                    Total: {judgements_percents['total_judgements']:,}**""")
        self.add_field(name="Achievements Progress", value=f"**{self.profile_data['achievement_str']}**")