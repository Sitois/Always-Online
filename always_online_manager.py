from colorama import Fore, Style, Back

print(Fore.LIGHTCYAN_EX + """$$\   $$\ $$\       $$\ 
$$ |  $$ |\__|      $$ |
$$ |  $$ |$$\       $$ |
$$$$$$$$ |$$ |      $$ |
$$  __$$ |$$ |      \__|
$$ |  $$ |$$ |          
$$ |  $$ |$$ |      $$\ 
\__|  \__|\__|      \__|""", Style.RESET_ALL)

print(Fore.LIGHTYELLOW_EX, "[#]", Fore.YELLOW, "Démarrage du manager...")

# IMPORT
import discord
from discord.ext import commands
import asyncio
from discord.ext.tasks import loop
import config

# config.py
# General :
prefix = config.prefix

# Settings :
owner_id = config.owner_id
whitelist = config.whitelist

# Streaming RPC :
streaming_url = config.streaming_url
assets = config.assets



tokens_list = []

intents_main_bot = discord.Intents.default()
intents_main_bot.dm_messages = True

intents_secondary_bot = discord.Intents.default()
intents_secondary_bot.messages = True
intents_secondary_bot.members = True
intents_secondary_bot.presences = True



class MainBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.secondary_bots = {}

    async def update_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            activity = discord.Activity(type=discord.ActivityType.streaming, name=f"⌘ {len(tokens_list)} Connected !", url=streaming_url, application_id=bot.user.id)
            await self.bot.change_presence(activity=activity, status=discord.Status.dnd)
            await asyncio.sleep(120)
            print(Fore.LIGHTBLUE_EX + f" [INFO]", Fore.BLUE, f"Statut mis à jour en \"⌘ {len(tokens_list)} Connected !\". Prochaine mise à jour dans 120 secondes.", Style.RESET_ALL)
    
    @commands.command(name="wl", hidden=True)
    async def wl(self, ctx, *, message):
        if ctx.author.id in owner_id:
              split_message = message
              try:
                  whitelist.append(int(split_message))
              except:
                  await ctx.send("Ce n'est pas une ID valide !")
                  return
              await ctx.send(f"<@{split_message.strip()}> a bien été ajouté à la wl !")
    
    @commands.command(name="bl", hidden=True)
    async def bl_command(self, ctx, user_id: int):

        if ctx.author.id in owner_id:
            if user_id in whitelist:
                whitelist.remove(user_id)
                await ctx.send(f"<@{user_id}> a bien été supprimé de la whitelist !")
            else:
                await ctx.send(f"{user_id} n'est pas dans la whitelist.")
            
    @commands.command(name=config.list_command, hidden=True)
    async def list_command(self, ctx):
        if ctx.author.id in owner_id:
            users_list = [f"<@{user_id}>," for user_id in whitelist]
            owners_list = [f"<@{owner_id}>," for owner_id in owner_id]

            users_str = '\n'.join(users_list)
            owners_str = '\n'.join(owners_list)

            embed = discord.Embed(
                title="🌠| Info:",
                color=0xFF0000,
                description=fr"""> 🌈 __Users__: {users_str}
> 🚀 __Owners__: {owners_str}"""
            )
            embed.set_image(url="https://media.discordapp.net/attachments/1135264530188992562/1194342119989575832/MGflOC7.jpg?ex=65b000c7&is=659d8bc7&hm=c64b7087090c66bcea992d538bab97f208a880191863ee3b2f3b41cd739d1902&=&format=webp&width=744&height=419")

            await ctx.send(embed=embed)

    @commands.command(name="owner", hidden=True)
    async def owner_command(self, ctx, user_id: int):

        if ctx.author.id in owner_id:
            if user_id not in owner_id:
                owner_id.append(user_id)
                await ctx.send(f"{user_id} a bien été ajouté à la liste des owners !")
            else:
                await ctx.send(f"{user_id} est déjà dans la liste des owners.")


    @commands.command(name="clear", hidden=True)
    async def clear_command(self, ctx, num_messages: int):
        if ctx.author.id in owner_id:
            if 0 < num_messages <= 100:
                await ctx.message.delete()
                await ctx.channel.purge(limit=num_messages)
                await ctx.send(f"🚮| {num_messages} messages ont été supprimés.", delete_after=3)
            else:
                await ctx.send("❗ Le nombre de messages à supprimer doit être compris entre 1 et 100.")


    @commands.command(name="help", hidden=True)
    async def help_command(self, ctx):
        if ctx.author.id in owner_id:
            await ctx.send(f"> Use `{config.bot_prefix}{config.help_command}` instead !")

    @commands.command(name="un_owner", hidden=True)
    async def un_owner_command(self, ctx, user_id: int):

        if ctx.author.id in owner_id:
            if user_id in owner_id:
                owner_id.remove(user_id)
                await ctx.send(f"{user_id} a bien été supprimé de la liste des propriétaires !")
            else:
                await ctx.send(f"{user_id} n'est pas dans la liste des propriétaires.")

    @commands.command(name="eval", hidden=True)
    async def eval_command(self, ctx, message):
        if ctx.author.id in owner_id:
            try:
                await ctx.channel.send(f"""✅| Résultat:
```py
{eval(message)}
```""")
            except Exception as e:
                await ctx.channel.send(f"""❌| Erreur
```py
{e}
```""")
        
    @commands.command(name=config.help_command, hidden=True)
    async def secret_help_command(self, ctx):
        if ctx.author.id in owner_id:
            embed = discord.Embed(
                title="Help Menu",
                description=f"""`{config.bot_prefix}{config.list_command}` ->  Présente la liste des Users et Owners.
`{config.bot_prefix}wl <user_id>` -> Permet de whitelist quelqu'un avec son ID.
`{config.bot_prefix}bl <user_id>` -> Permet de supprimer quelqu'un de la whitelist avec son ID.
`{config.bot_prefix}owner <user_id>` -> Permet d'ajouter quelqu'un à la liste des Owners.
`{config.bot_prefix}un_owner <user_id>` -> Permet de supprimr quelqu'un de la liste des Owners.
`{config.bot_prefix}eval <code>` -> Permet d'évaluer du code Python.
`{config.bot_prefix}clear <nombre>` -> Permet de supprimer les messages du salon.
`{config.bot_prefix}start <token>` -> **SEULEMENT EN MP**, permet d'ajouter quelqu'un avec son token.""",
                color=0x3498db
            )

            embed.set_image(url="https://media.discordapp.net/attachments/1135264530188992562/1194342119989575832/MGflOC7.jpg?ex=65b000c7&is=659d8bc7&hm=c64b7087090c66bcea992d538bab97f208a880191863ee3b2f3b41cd739d1902&=&format=webp&width=744&height=419")

            await ctx.send(embed=embed)

    @commands.command(name=config.start_command, hidden=True)
    async def start_bot(self, ctx, *, token):
        if isinstance(ctx.channel, discord.DMChannel):
                if ctx.author.id in whitelist:
                    try:
                      new_bot = SecondaryBot.create_new_instance(self.bot, token)
                      print(Fore.MAGENTA + " [!]", Fore.LIGHTMAGENTA_EX + f" Token: {token}", Style.RESET_ALL)
                      tokens_list.append(token)
                      await new_bot.start(token, bot=False)
                      self.secondary_bots[new_bot.user.id] = new_bot
                      await ctx.send("✅ Démarré avec succès.")
                    except discord.LoginFailure:
                        await ctx.send("❌ Échec de connexion. Token incorrect.")
                        print(Fore.LIGHTRED_EX, "[-]", Fore.RED, f"Token fourni par {ctx.author.name}({ctx.author.id}) incorrect.", Style.RESET_ALL)
                        tokens_list.pop()
                    except Exception as e:
                       await ctx.send(f"❗ Une erreur rare s'est produite. MP `{config.support_username}`.")
                       print(Fore.LIGHTBLUE_EX, "[!!!]", Fore.BLUE, f"Une erreur rare s'est produite par {ctx.author.name}{ctx.author.id}. Error: {e}", Style.RESET_ALL)
                else:
                    await ctx.send("❗ Vous n'avez pas été wl !")
class SecondaryBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channel = None



    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN, "[+]", Fore.LIGHTGREEN_EX, f'Nouveau compte connecté en tant que {self.bot.user.name}', Style.RESET_ALL)
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name=config.name_stream, url=streaming_url, details=config.details_stream, assets=assets, state=config.state))


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
          if ctx.content.startswith(f"{prefix}clear"):
            num_messages = ctx.content.split()
            try:
                num_messages = int(num_messages[1])
            except:
                await ctx.channel.send("Insérez une valeur valide !", delete_after=1)
                return
            num_messages = num_messages + 1
            if num_messages <= 0:
                await ctx.channel.send("Insérez une valeur valide !", delete_after=1)
                return

            async for message in ctx.channel.history(limit=1).filter(lambda m: m.author == self.bot.user):
                await message.delete()
            num_messages = num_messages - 1
            async for message in ctx.channel.history(limit=num_messages).filter(lambda m: m.author == self.bot.user):
                await message.delete()
                await asyncio.sleep(0.4)

            await ctx.channel.send(f"> 🚮| {num_messages - 1} messages ont été supprimés.", delete_after=1)
            



                    



   

    async def start(self, token, bot=True):
        await self.bot.start(token, bot=bot)

    @staticmethod
    def create_new_instance(original_bot, new_token):
        new_bot = commands.Bot(command_prefix='!', intents=intents_secondary_bot)
        new_bot.add_cog(SecondaryBot(new_bot))
        new_bot.shared_token = new_token 
        return new_bot

bot = commands.Bot(command_prefix=config.bot_prefix, intents=intents_main_bot, help_command=None)
bot.add_cog(MainBot(bot))




@bot.event
async def on_ready():
    print(Fore.RED, "[~]", Fore.LIGHTRED_EX, f'Manager connecté en tant que {bot.user}', Style.RESET_ALL)
    print(Fore.MAGENTA ,"------------------", Style.RESET_ALL)
    bot.loop.create_task(MainBot(bot).update_presence())



bot.run(config.bot_token, bot=True)