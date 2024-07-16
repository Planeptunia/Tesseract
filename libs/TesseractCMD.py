import hikari
import lightbulb
import miru
import os
import time
import libs.TesseractAPIWrapper as Requester
import libs.TesseractVisuals as Visuals
import libs.TesseractFuncs as Funcs
from libs.TesseractGlobals import tesseract_logger as Logger

env = Funcs.get_dotenv()
# default_enabled_guilds=(1033335077779812393)
bot = lightbulb.BotApp(env["DISCORD_TOKEN"], intents=hikari.Intents.ALL, owner_ids=(424559848215150592,), default_enabled_guilds=(1033335077779812393))

client = miru.Client(bot)

activity = hikari.Activity(name='Quaver', type=hikari.ActivityType.PLAYING) 

@bot.listen(hikari.StartedEvent)
async def started(event):
    await bot.update_presence(activity=activity)
    Logger.info("Bot awake")

@bot.command
@lightbulb.command("user", "User Command Group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def user(ctx: lightbulb.Context):
    pass

@user.child
@lightbulb.option("username", "Username for needed profile (if not given will use your Discord Global Name)", type=str, required=False)
@lightbulb.command("profile", "Get info from user's profile")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_profile(ctx: lightbulb.Context):
    time_start = time.perf_counter()
    username = (ctx.options.username if ctx.options.username is not None else ctx.author.global_name) 
    Logger.info(f"Started grabbing profile of {username}")
    search_result = Requester.search_by_name(username)
    user_info = Requester.get_full_profile_by_id(search_result['users'][0]['id'])
    achievements = Requester.get_achievements_by_id(search_result['users'][0]['id'])
    total_achievements = 0
    for achievement in achievements['achievements']:
        if achievement['unlocked'] == True:
            total_achievements += 1
    user_info['user']['achievement_str'] = f"{total_achievements}/{len(achievements['achievements'])}"
    profile_embed = Visuals.ProfileEmbed(user_info['user'])
    mode_select = Visuals.GamemodeSelectView(user_info['user'])
    client.start_view(mode_select)
    await ctx.respond(profile_embed, components=mode_select)
    Logger.info(f"Got profile of {username} in {time.perf_counter() - time_start:.3f}s")
        
@user.child
@lightbulb.option("type", "Type of achievements to return (Unlocked by default)", type=str, choices=['Unlocked', 'Locked'], default='Unlocked')
@lightbulb.option("username", "Username for needed profile (if not given will use your Discord Global Name)", type=str, required=False)
@lightbulb.command("achievements", "Get achievements from user's profile")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_achievements(ctx: lightbulb.Context):
    time_start = time.perf_counter()
    username = (ctx.options.username if ctx.options.username is not None else ctx.author.global_name) 
    lock_type = None
    match ctx.options.type:
        case "Unlocked":
            lock_type = True
        case "Locked":
            lock_type = False
        case _:
            await ctx.respond("Invalid unlock type! Please enter a valid one")
    Logger.info(f"Started grabbing {'unlocked' if lock_type == True else 'locked'} achievements of {username}")
    search_result = Requester.search_by_name(username)
    user_info = Requester.get_full_profile_by_id(search_result['users'][0]['id'])
    achievements = Requester.get_achievements_by_id(search_result['users'][0]['id'])
    top_score_4k = Requester.get_best_scores_by_id(search_result['users'][0]['id'], 1, 1)
    top_score_7k = Requester.get_best_scores_by_id(search_result['users'][0]['id'], 2, 1)
    achievement_list = Funcs.process_achievement_list(user_info, achievements, lock_type, top_score_7k, top_score_4k)['achievements']
    achievement_embed = Visuals.AchievementsEmbed(achievement_list, username, lock_type)
    page_select = Visuals.AchievementsPagesView(achievement_list, username, lock_type)
    client.start_view(page_select)
    await ctx.respond(achievement_embed, components=page_select)
    Logger.info(f"Got {'unlocked' if lock_type == True else 'locked'} achievements of {username} in {time.perf_counter() - time_start:.3f}s")

@user.child
@lightbulb.option("mode", "Which gamemode score to get (4K by default)", type=str, choices=['4K', "7K"], default='4K')
@lightbulb.option("username", "Username for needed profile (if not given will use your Discord Global Name)", type=str, required=False)
@lightbulb.command("recent", "Gets the most recent score from user's profile")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_recent_score(ctx: lightbulb.Context):
    time_start = time.perf_counter()
    username = (ctx.options.username if ctx.options.username is not None else ctx.author.global_name)
    mode = 1
    match ctx.options.mode:
        case "4K":
            mode = 1
        case "7K":
            mode = 2
        case _:
            await ctx.respond("Invalid gamemode! Please enter a valid one")
    Logger.info(f"Started grabbing most recent score of {username}")
    search_result = Requester.search_by_name(username)
    most_recent_score = Requester.get_recent_scores_by_id(search_result['users'][0]['id'], mode, 1)
    author_info = Requester.get_mini_profile_by_id(most_recent_score['scores'][0]['map']['creator_id'])
    map_info = Requester.get_map_info_by_id(most_recent_score['scores'][0]['map']['id'])
    original_diff = None
    if most_recent_score['scores'][0]['grade'] == "F":
        original_diff = map_info['map']['difficulty_rating']
    max_combo = map_info['map']['count_hitobject_normal'] + (map_info['map']['count_hitobject_long'] * 2)
    score_embed = Visuals.RecentScoreEmbed(most_recent_score, author_info['users'][0]['avatar_url'], search_result['users'][0]['avatar_url'], username, max_combo, original_diff=original_diff)
    await ctx.respond(score_embed)
    Logger.info(f"Got most recent score of {username} in {time.perf_counter() - time_start:.3f}s")
    
    
@bot.command
@lightbulb.add_checks(lightbulb.owner_only, lightbulb.guild_only)
@lightbulb.command("reboot", "Reboot the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def reboot(ctx: lightbulb.Context):
    await ctx.respond("See you soon", flags=hikari.MessageFlag.EPHEMERAL)
    Logger.info("Rebooting from Discord Command")
    os.system("python -OO TesseractRun.py")

