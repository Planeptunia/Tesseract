import dateutil.parser as dp
import hikari
import miru

emojis = {"X": "<:gradex:1262201488009072701>", "SS": "<:gradess:1262201547190702152>",
          "S": "<:grades:1262201580007067780>", "A": "<:gradea:1262201623577366609>",
          "B": "<:gradeb:1262201655097561209>", "C": "<:gradec:1262201670188929074>", "D": "<:graded:1262201683526684757>"}

class ProfileEmbed(hikari.Embed):
    def __init__(self, profile_data: dict, grades: dict):
        profile_info = profile_data['info']
        keys4_info = profile_data['keys4']
        last_online = dp.parse(profile_info['latest_activity'])
        
        if profile_info['online']:
            online = "***Currently Online***"
        else:
            online = f"**Last online: <t:{round(last_online.timestamp())}:R>**"
        
        super().__init__(title=f"{profile_info['username']}'s profile", 
                         description=f"""{online}
                         **#{keys4_info['globalRank']} (:flag_{profile_info['country'].lower()}: #{keys4_info['countryRank']})**""",
                         url=f"https://quavergame.com/user/{profile_info['id']}", color=(0, 204, 204))
        
        self.set_thumbnail(profile_info['avatar_url'])
        
        self.add_field(name="Total Score", value=f"**{keys4_info['stats']['total_score']:,}**", inline=True)
        self.add_field(name="Overall Accuracy", value=f"**{keys4_info['stats']['overall_accuracy']:.2f}%**", inline=True)
        self.add_field(name="Play Count", value=f"**{keys4_info['stats']['play_count']:,}**", inline=True)

        self.add_field(name="Ranked Score", value=f"**{keys4_info['stats']['ranked_score']:,}**", inline=True)
        self.add_field(name="Overall Rating", value=f"**{keys4_info['stats']['overall_performance_rating']:.2f}**", inline=True)
        self.add_field(name="Max Combo", value=f"**{keys4_info['stats']['max_combo']:,}**", inline=True)
        
        self.add_field(name="Grades", value=f"**{emojis['X']}: {grades['X']} | {emojis['SS']}: {grades['SS']} | {emojis['S']}: {grades['S']} | {emojis['A']}: {grades['A']} | {emojis['B']}: {grades['B']} | {emojis['C']}: {grades['C']} | {emojis['D']}: {grades['D']}**")
