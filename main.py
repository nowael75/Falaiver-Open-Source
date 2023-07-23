#modules
print("----IMPORTATION DES MODULES & INTENTS----")
import discord
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True)
print("----IMPORTATION DES MODULES & INTENTS RÉUSSI----")
print("--------")

bot = commands.Bot(command_prefix='!', intents=intents)



print("----PREPARATION DE L'EVENT----")
print("--------")
@bot.event
async def on_ready():
    activity = discord.Game(name="", type=3) #Mettez ce que vous voulez entre les ""
    await bot.change_presence(status=discord.Status.online, activity=activity) #online, idle, dnd
    print(f"SUCCES : {bot.user} est actuellement connectée sur discord !")
    print("--------")
    print("Logs commande :")


@bot.slash_command(name="help", description=f"Regarder la page help de {bot.user}")
async def help(ctx):
    embed = discord.Embed(title="Page help", description=f"Ci dessous, toute les commandes de {bot.user}", color=749198)
    embed.add_field(name="- Modérations", value="`nuke`, `ban`, `kick`, `lock`, `unlock`", inline=False)
    embed.add_field(name="- Informations", value="`help`", inline=False)
    embed.set_footer(text=f"Demandé par {ctx.author}")
    await ctx.respond(embed=embed)
    print(f"SUCCES : {ctx.author} à effectué help")

@bot.slash_command(name="ban", description="Permet de banni un membre du serveur")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.respond(f"{ctx.author} a banni {member} pour la raison {reason}")
    print(f"SUCCES : {ctx.author} a banni {member} pour la raison {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
    	await ctx.respond(f"Désolé {ctx.author}, tu n'as pas la permissions `ban_members` pour executé cette commande")
    	print(f"ERROR : {ctx.author} / ban / Pas de permission")
        
@bot.slash_command(name="kick", description="Permet d'expulser un membre")
@commands.has_permissions(manage_messages=True)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send (f"{ctx.author} a expulsé {user}.")

    
@kick.error
async def kick_error(ctx, error, user : discord.User):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Désolé {ctx.author}, tu n'as pas la permission de faire cela")
        print(f"ERROR : {ctx.author} / {user} / MissingPermission")
        

        
@bot.slash_command(name="lock", description="Permet de verouiller un salon")
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Ce salon a bien était verouiller !")
    print(f"SUCCES : {ctx.author} a effectué lock")
    
@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Désolé {ctx.author}, vous n'avez pas la permission `Manage Channel` pour effectué cette commande")
        print(f"ERROR : {ctx.author} / lock / Missing Permission")

@bot.slash_command(name="unlock", description="Permet de deverouiller un salon")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Ce salon a bien était deverouiller avec succès !")
    print(f"SUCCES : {ctx.author} a effectué unlock")
    
@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Désolé {ctx.author}, vous n'avez pas la permission `Manage Channel` pour executé cette commande !")
        print(f"ERROR : {ctx.author} / unlock / Missing Permission")
    
@bot.slash_command(name="nuke", description="Permet de recréé un salon et de supprimé l'ancien")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx, channel: discord.TextChannel = True):
    if channel == None: 
        await ctx.send(f"{ctx.author.mention}, mentionnez le salon à nuke !")
        print(f"ERROR : Nuke / {ctx.author} / Aucun salon specifié")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Nuke [Nuke automatique]")
        await nuke_channel.delete()
        await new_channel.send("Salon recréé avec succès",delete_after=10)
        await ctx.send(f"Le Salon {channel.name} est en train d'être recréé !")
        print(f"SUCCES : Nuke / {channel.name} / {ctx.author} / Salon Nuke")

    else:
        await ctx.send(f"je trouve pas le salon {channel.name} merci de réesayer")
        print(f"ERROR : Nuke / {channel.name} / {ctx.author} / Salon invalide")
    

    
        

print("----TOKEN VALIDÉ----")
print("--------")
bot.run("") #Token de votre bot
