import discord
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents) 

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def ping(ctx):
    await ctx.send('there')
        
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def repeat(ctx, amount: int, *, message: str):
    if amount < 100:
        for i in range(amount):
            await ctx.send(message)
    elif amount >= 100:
        await ctx.send("Amount must be less than 100.")

@bot.command() 
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:  # Komutun yasaklanması gereken kullanıcıyı belirtip belirtmediğinin kontrol edilmesi
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı yasaklamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)  
            await ctx.send(f" Kullanıcı {member.name} banlandı.")  
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error 
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")  
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı.")  
bot.run(token)
