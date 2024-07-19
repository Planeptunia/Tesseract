import hikari
import lightbulb
import miru
from miru.ext import nav
import os
import time
import math
import re
import libs.TesseractAPIWrapper as Requester
import libs.TesseractVisuals as Visuals
import libs.TesseractFuncs as Funcs
import libs.Types.TesseractTypes as Types
from libs.Types.TesseractTypes import tesseract_logger as Logger

env = Funcs.get_dotenv()
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
    
    Logger.info(f"Started grabbing profile using v2 of {username}")
    
    search_result: Types.QuaverUser = Requester.get_profile_by_id_or_name(username)
    
    user_info = search_result
    profile_embed_4k = Visuals.ProfileEmbedv2(user_info, 1)
    profile_embed_7k = Visuals.ProfileEmbedv2(user_info, 2)
    pages = [profile_embed_4k, profile_embed_7k]
    btns = [nav.FirstButton(label="4K", emoji=None), nav.LastButton(label="7K", emoji=None)]
    navigator = nav.NavigatorView(pages=pages, items=btns)
    
    builder = await navigator.build_response_async(client)
    await builder.create_initial_response(ctx.interaction)
    client.start_view(navigator)
    
    Logger.info(f"Got profile of {username} using v2 in {time.perf_counter() - time_start:.3f}s")
    
@user.child
@lightbulb.option("username", "Username for needed profile (if not given will use your Discord Global Name)", type=str, required=False)
@lightbulb.command("achievements", "Get achievements from user's profile")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_achievements(ctx: lightbulb.Context):
    time_start = time.perf_counter()
    username = (ctx.options.username if ctx.options.username is not None else ctx.author.global_name)
    Logger.info(f"Started grabbing achievements of {username} using v2")
    user_profile = Requester.get_profile_by_id_or_name(username)
    achievements = Requester.get_achievements_by_idv2(user_profile.id)
    
    pages = []
    for page in range(math.ceil((len(achievements) / 5))):
        new_achievement_embed = Visuals.AchievementsEmbedv2(achievements, user_profile, page)
        pages.append(new_achievement_embed)
        
    navigator = nav.NavigatorView(pages=pages)
    
    builder = await navigator.build_response_async(client)
    await builder.create_initial_response(ctx.interaction)
    client.start_view(navigator)
    
    Logger.info(f"Got achievements of {username} in {time.perf_counter() - time_start:.3f}s")

@user.child
@lightbulb.option("mode", "Which gamemode score to get (4K by default)", type=str, choices=['4K', "7K"], default='4K')
@lightbulb.option("username", "Username for needed profile (if not given will use your Discord Global Name)", type=str, required=False)
@lightbulb.command("recent", "Gets the most recent score from user's profile")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_recent_score(ctx: lightbulb.Context):
    time_start = time.perf_counter()
    username = (ctx.options.username if ctx.options.username is not None else ctx.author.global_name)
    match ctx.options.mode:
        case "4K":
            mode = 1
        case "7K":
            mode = 2
    Logger.info(f"Started grabbing most recent score of {username} using v2")
    search_result = Requester.get_profile_by_id_or_name(username)
    recent_scores = Requester.get_recent_scores_by_idv2(search_result.id, mode)
    recent_score_embed = Visuals.RecentScoreEmbedv2(recent_scores, search_result)
    await ctx.respond(recent_score_embed)
    Logger.info(f"Got most recent score of {username} in {time.perf_counter() - time_start:.3f}s using v2")

@bot.command
@lightbulb.command("Compare", "Get yours best score on the map")
@lightbulb.implements(lightbulb.MessageCommand)
async def compare_score(ctx: lightbulb.MessageContext):
    def find_quaver_mapset_link(message: hikari.Message):
        pattern = "https:\/\/quavergame\.com\/mapset\/map\/(\d{1,})"
        id = None
        if message.content is not None:
            id = re.search(pattern, message.content)
            if id is not None:
                id = id.group(1)
        if len(message.embeds) > 0:
            id = re.search(pattern, message.embeds[0].url)
            if id is not None:
                id = id.group(1)
        return id
    message = list(ctx.resolved.messages.values())[0]
    map_id = find_quaver_mapset_link(message)
    if map_id == None:
        await ctx.respond("Haven't been able to find a valid mapset link in the message")
    else:
        map_info = Requester.get_mapset_info_by_id(map_id)
        await ctx.respond("mewo")

@bot.command
@lightbulb.add_checks(lightbulb.owner_only, lightbulb.guild_only)
@lightbulb.command("reboot", "Reboot the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def reboot(ctx: lightbulb.Context):
    await ctx.respond("See you soon", flags=hikari.MessageFlag.EPHEMERAL)
    Logger.info("Rebooting from Discord Command")
    os.system("python -OO TesseractRun.py")


