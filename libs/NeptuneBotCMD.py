import dotenv
import hikari
import lightbulb
import miru
import libs.NeptuneBotRequester as Requester
import libs.NeptuneBotVisuals as Visuals
import os

bot = lightbulb.BotApp(os.getenv("DISCORD_TOKEN"), default_enabled_guilds=(1033335077779812393), intents=hikari.Intents.ALL)

client = miru.Client(bot)

activity = hikari.Activity(name='Quaver', type=hikari.ActivityType.PLAYING) 

@bot.listen(hikari.StartedEvent)
async def started(event):
    await bot.update_presence(activity=activity)
    print('Bot awake')

@bot.command
@lightbulb.option("username", "Username for needed profile", type=str, required=True)
@lightbulb.command("profile", "Get info from user's profile")
@lightbulb.implements(lightbulb.SlashCommand)
async def get_profile(ctx: lightbulb.Context):
    search_result = Requester.search_by_name(ctx.options.username)
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
        
@bot.command
@lightbulb.option("type", "Type of achievements to return", type=str, choices=['Unlocked', 'Locked'], default='Unlocked')
@lightbulb.option("username", "Username for needed profile", type=str, required=True)
@lightbulb.command("achievements", "Get achievements from user's profile")
@lightbulb.implements(lightbulb.SlashCommand)
async def get_achievements(ctx: lightbulb.Context):
    lock_type = None
    match ctx.options.type:
        case "Unlocked":
            lock_type = True
        case "Locked":
            lock_type = False
        case _:
            await ctx.respond("Invalid unlock type! Please enter a valid one")
    search_result = Requester.search_by_name(ctx.options.username)
    achievements = Requester.get_achievements_by_id(search_result['users'][0]['id'])
    achievement_list = []
    for achievement in achievements['achievements']:
        if achievement['unlocked'] == lock_type:
            achievement_list.append(achievement)
    achievement_embed = Visuals.AchievementsEmbed(achievement_list, ctx.options.username, lock_type)
    page_select = Visuals.AchievementsPagesView(achievement_list, ctx.options.username, lock_type)
    client.start_view(page_select)
    await ctx.respond(achievement_embed, components=page_select)
    
    
    

