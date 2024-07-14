TOKEN = 'MTAzMzMzNTc5MTAyOTYwNDQxNA.GX8hmH.2txx1w9c8F6koJaxtVjH5yuNQ2i4zXfEp9BfEQ'

import hikari
import lightbulb
import miru

bot = lightbulb.BotApp(TOKEN, default_enabled_guilds=(1033335077779812393), intents=hikari.Intents.ALL)

client = miru.Client(bot)

class BasicView(miru.View):
    # Define a new TextSelect menu with two options
    @miru.text_select(
        placeholder="Select me!",
        options=[
            miru.SelectOption(label="Option 1"),
            miru.SelectOption(label="Option 2"),
        ],
    )
    async def basic_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        await ctx.respond(f"You've chosen {select.values[0]}!")

    # Define a new Button with the Style of success (Green)
    @miru.button(label="Click me!", style=hikari.ButtonStyle.SUCCESS)
    async def basic_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond("You clicked me!")

    # Define a new Button that when pressed will stop the view
    # & invalidate all the buttons in this view
    @miru.button(label="Stop me!", style=hikari.ButtonStyle.DANGER)
    async def stop_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        ctx.message.delete()
        self.stop()  # Called to stop the view

@bot.listen(hikari.StartedEvent)
async def started(event):
    print('le cring')
    
@bot.command
@lightbulb.command('ping', 'pong')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.author.send('Pong')
    await ctx.respond('message sent')

@bot.command
@lightbulb.command('group', 'group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def group(ctx):
    pass

@group.child
@lightbulb.command('subcommand', 'subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('box')

@bot.command
@lightbulb.option('num1', 'num1', type=int)
@lightbulb.option('num2', 'num2', type=int)
@lightbulb.command('add', 'sum')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context):
    await ctx.respond(ctx.options.num1+ctx.options.num2)    

@bot.command
@lightbulb.command('embed', 'embed')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed(ctx):
    embed = hikari.Embed(title='Example embed', description='example hikari embed', color=(0, 255, 255))
    embed.add_field('field name', 'field content')
    embed.set_thumbnail('https://i.imgur.com/EpuEOXC.jpg')
    embed.set_footer('this is footer')
    await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)

@bot.command
@lightbulb.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR), lightbulb.guild_only, lightbulb.owner_only)
@lightbulb.command('button', 'button')
@lightbulb.implements(lightbulb.SlashCommand)
async def create_buttons(ctx):
    view = BasicView()
    await ctx.respond('roll', components=view)
    client.start_view(view)
    print('done')

@bot.command
@lightbulb.option('color', 'color', type=tuple)
@lightbulb.option('name', 'name', type=str)
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.command('role', 'create role')
@lightbulb.implements(lightbulb.SlashCommand)
async def create_role(ctx: lightbulb.Context):
    await bot.rest.create_role(name=ctx.options.name, color=ctx.options.color, guild=ctx.guild_id)
    await ctx.respond('role created')

@bot.command
@lightbulb.command('presence', 'presence')
@lightbulb.implements(lightbulb.SlashCommand)
async def presence(ctx: lightbulb.Context):
    activity = hikari.Activity(name='something', type=hikari.ActivityType.PLAYING) 
    await bot.update_presence(activity=activity)
    await ctx.respond('updated presence')

bot.run()
