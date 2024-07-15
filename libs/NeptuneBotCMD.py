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
    user_info['user']['achievement_str'] = achievement_str = f"{total_achievements}/{len(achievements['achievements'])}"
    profile_embed = Visuals.ProfileEmbed(user_info['user'])
    mode_select = Visuals.GamemodeSelectView(user_info['user'])
    client.start_view(mode_select)
    await ctx.respond(profile_embed, components=mode_select)
        

