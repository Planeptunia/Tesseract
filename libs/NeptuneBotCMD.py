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
    if len(search_result['users']) > 1:
        await ctx.respond("Found multiple users")
    else:
        await ctx.respond(response_type=hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        user_info = Requester.get_full_profile_by_id(search_result['users'][0]['id'])
        grades = Requester.get_grades_by_id(search_result['users'][0]['id'])
        if grades:
            profile_embed = Visuals.ProfileEmbed(user_info['user'], grades)
            await ctx.respond(profile_embed, response_type=hikari.ResponseType.DEFERRED_MESSAGE_UPDATE)
        

