import disnake, asyncio, random, os, pickle
from math import floor
from disnake.ext import commands

bot=commands.Bot(command_prefix="ctqa!", help_command=None, intents=disnake.Intents.all())

type_dict = {
    "Fine": 1000,
    "Nice": 750,
    "Good": 500,
    "Uncommon": 350,
    "Rare": 275,
    "Wild": 230,
    "Baby": 200,
    "Epic": 175,
    "Brave": 150,
    "Reverse": 125,
    "Inverted": 100,
    "Superior": 80,
    "Tema5002": 50,
    "Legendary": 35,
    "Mythic": 25,
    "8bit": 20,
    "Corrupted": 15,
    "Professor": 10,
    "Real": 8,
    "Ultimate": 5,
    "Cool": 2
}

if not os.path.exists("ctqas.dat"):
    pickle.dump({}, open("ctqas.dat", "wb"))

if not os.path.exists("ctqa channels.dat"):
    pickle.dump([], open("ctqa channels.dat", "wb"))

CAT_TYPES = []

def makecatlist():
    global CAT_TYPES
    global cat_types
    CAT_TYPES = []
    cat_types = []
    for k, v in type_dict.items():
        CAT_TYPES += [k]*v
        cat_types += [k]

makecatlist()

def get_cat():
    global CAT_TYPES
    if len(CAT_TYPES) == 0: makecatlist()
    return CAT_TYPES.pop(random.randrange(len(CAT_TYPES)))

def get_user_cats(server_id, member_id):
    filepath = os.path.join(os.path.dirname(__file__), "cats")
    if not os.path.exists(filepath): os.makedirs(filepath)
    filepath = os.path.join(filepath, str(server_id))
    if not os.path.exists(filepath): os.makedirs(filepath)
    filepath = os.path.join(filepath, f"{member_id}.dat")
    if os.path.exists(filepath):
        return pickle.load(open(filepath, "rb"))
    return {}

def save_user_cats(server_id, member_id, cats):
    filepath = os.path.join(os.path.dirname(__file__), "cats", str(server_id), f"{member_id}.dat")
    pickle.dump(cats, open(filepath, "wb"))

def get_custom_cats(member_id):
    filepath = os.path.join(os.path.dirname(__file__), "custom cats")
    if not os.path.exists(filepath): os.makedirs(filepath)
    filepath = os.path.join(filepath, f"{member_id}.dat")
    if os.path.exists(filepath):
        return pickle.load(open(filepath, "rb"))
    return {}

def give_custom_cat(member_id, cat_type, amount):
    cats = get_custom_cats(member_id)
    if cat_type in cats: cats[cat_type] += amount
    else: cats[cat_type] = amount
    filepath = os.path.join(os.path.dirname(__file__), "custom cats", f"{member_id}.dat")
    pickle.dump(cats, open(filepath, "wb"))

def givecat(server_id, member_id, cat_type, amount):
    cats = get_user_cats(server_id, member_id)
    if cat_type in cats: cats[cat_type] += amount
    else: cats[cat_type] = amount
    save_user_cats(server_id, member_id, cats)

def emoji(name):
    return str(disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=name))

def ctqa_emoji(name):
    name = name.lower()
    if name == "octopus": catemoji = "🐙"
    else: catemoji = disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=f"{name}ctqa") or "emoji fail"
    return catemoji

@bot.event
async def on_ready():
    print(f"@{bot.user} is now online")
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Cat Bot sanity"))
    folder_path = os.path.join(os.path.dirname(__file__), "spawn config")
    while True:
        for list in pickle.load(open("ctqa channels.dat", "rb")):
            guild_id, channel_id = list
            channel = await bot.get_guild(guild_id).fetch_channel(channel_id)
            cat = get_cat()
            cat_emoji = ctqa_emoji(cat)
            cat_list = pickle.load(open("ctqas.dat", "rb"))
            if not channel_id in cat_list:
                msg = await channel.send(f"A wild {cat_emoji} **{cat} Ctqa** just appeared! Type \"ctqa\" to catch it!", file = disnake.File("syating_ctqa.webp"))
                cat_list[channel_id] = [cat, msg.id]
                print(type(cat_list))
                print(cat_list)
                pickle.dump(cat_list, open("ctqas.dat", "wb"))
        await asyncio.sleep(random.randint(30, 60*5))

@bot.event
async def on_message(message):
    cat_list = pickle.load(open("ctqas.dat", "rb"))
    await bot.process_commands(message)
    current_time = message.created_at.timestamp()
    msg = message.content
    msglow = msg.lower()

    if msglow == "ctqa":
        
        filepath = os.path.join(os.path.dirname(__file__), "whitelisted bots")
        if not os.path.exists(filepath): os.makedirs(filepath)
        filepath = os.path.join(filepath, f"{message.guild.id}.dat")
        if not os.path.exists(filepath): pickle.dump([], open(filepath, "wb"))
        bots = pickle.load(open(filepath, "rb"))

        if message.channel.id in cat_list and (not message.author.bot or message.author.id in bots):
            catlist = cat_list.pop(message.channel.id)
            pickle.dump(cat_list, open(f"ctqas.dat", "wb"))
            ctqamessage = await message.channel.fetch_message(catlist[1])
            then = ctqamessage.created_at.timestamp()
            time = round(abs(current_time-then)*100)/100

            cats = get_user_cats(message.guild.id, message.author.id)
            if not "fastest_catch" in cats:  cats["fastest_catch"] = time
            elif cats["fastest_catch"]>time: cats["fastest_catch"] = time

            if not "slowest_catch" in cats:  cats["slowest_catch"] = time
            elif cats["slowest_catch"]<time: cats["slowest_catch"] = time
            save_user_cats(message.guild.id, message.author.id, cats)

            days = int(time//86400)
            hours= int(time//3600%24)
            mins = int(time//60%60)
            secs = time%60
            caught_time = ""
            if days: caught_time += f"{days} days "
            if hours: caught_time += f"{hours} hours "
            if mins: caught_time += f"{mins} minutes "
            if secs:
                acc_seconds = round(secs*100)/100
                caught_time += f"{acc_seconds} seconds"
            caught_time = caught_time.strip()
            try: await ctqamessage.delete()
            except: pass
            try: await message.delete()
            except: pass
            cat_type = catlist[0]
            givecat(message.guild.id, message.author.id, cat_type, 1)
            await message.channel.send(f"{message.author.mention} caught a {ctqa_emoji(cat_type)} **{cat_type} Ctqa** in **{caught_time}**!\n"+\
                                       f"They now have **{get_user_cats(message.guild.id, message.author.id)[cat_type]} {cat_type} Ctqas** in their inventory.")
        else:
            await message.add_reaction(bot.get_emoji(1178287922756194394))

@bot.slash_command(name="setup", description="make bot spawn cats here (OWNER ONLY)")
async def send_splash_here(ctx):
    channels = pickle.load(open("ctqa channels.dat", "rb"))

    if ctx.author.id in [ctx.guild.owner_id, 558979299177136164]:
        if [ctx.guild.id, ctx.channel.id] in channels:
            channels.pop(ctx.guild.id)
            await ctx.send(f"**#{ctx.channel}** was removed from ctqa spawn list ❌")
        else:
            channels += [[ctx.guild.id, ctx.channel.id]]
            await ctx.send(f"**#{ctx.channel}** was added to ctqa spawn list ✅")
        pickle.dump(channels, open("ctqa channels.dat", "wb"))
    else:
        await ctx.send(f"lmao perms fail imagine having a skill issue {emoji('pointlaugh')}")

@bot.slash_command(name="inv", description="inventory")
async def inventory(ctx, member: disnake.Member = None):
    member = member or ctx.author
    inv = get_user_cats(ctx.guild.id, member.id)
    customs = get_custom_cats(member.id)
    fastest=slowest = "unknown"
    if "fastest_catch" in inv:
        fastest = f"{inv['fastest_catch']}s"
    if "slowest_catch" in inv:
        slowest = f"{round(inv['slowest_catch']/36)/100}h"
    if member==ctx.author: description = f"Your fastest catch is {fastest} and\n"+\
                                         f"your slowest catch is {slowest}"
    else: description = f"Their fastest catch is {fastest} and\n"+\
                        f"their slowest catch is {slowest}"
    if not (inv or customs): description = f"you have no ctqas go and cry about it {emoji('pointlaugh')}"
    if member==ctx.author: title = "Your ctqas:"
    else: title = f"{member.name}#{member.discriminator}'s ctqas:"
    embed = disnake.Embed(title=title, description=description)
    cats_counter = 0
    if description != f"you have no ctqas go and cry about it {emoji('pointlaugh')}":
        for type in cat_types:
            if type in inv:
                embed.add_field(name=f"{ctqa_emoji(type)} {type}", value=inv[type])
                cats_counter += inv[type]
        for type in customs:
            embed.add_field(name=f"{ctqa_emoji(type)} {type}", value=customs[type])
    footer_dict={"text": f"Total ctqas: {cats_counter}"}
    embed.set_footer(**footer_dict)
    await ctx.send(embed=embed)

@bot.slash_command(name="lb", description="leaderboards")
async def leaderboards(ctx):
    folder_path = os.path.join(os.path.dirname(__file__), "cats")
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    folder_path = os.path.join(folder_path, str(ctx.guild.id))
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    lb = {}
    for file in os.listdir(folder_path):
        cats_counter = 0
        inv = get_user_cats(ctx.guild.id, file.removesuffix(".dat"))
        for type in cat_types:
            if type in inv:
                cats_counter += inv[type]
        lb[int(file.removesuffix(".dat"))] = cats_counter
    lb = sorted(lb.items(), key=lambda x:x[1], reverse=True)
    if len(lb)>15: lb=lb[:15]
    lb = dict(lb)
    description = ""
    counter = 1
    for k, v in lb.items():
        description += f"{counter}. {v} ctqas: <@{k}>\n"
        counter += 1
    try: await ctx.send(embed = disnake.Embed(title=f"{ctx.guild.name} ctqa leaderboards:", description = description))
    except Exception as e: await ctx.send("uhhh sorry there is an error happened while sending your message and its mostly because your leaderboard is empty"+f"\n\n```{e}```")

@bot.command()
async def custom(ctx, user_id: int, cat_type: str, amount: int = 1):
    if not ctx.author.id in [558979299177136164, 903650492754845728]:
        await ctx.send(emoji("typing"))
        return
    if cat_type in cat_types:
        await ctx.send(f"{cat_type} is not a custom cat type")
        return
    give_custom_cat(user_id, cat_type, amount)
    await ctx.send(f"gave {bot.get_user(user_id)} {amount} {cat_type} ctqas")

@bot.command()
async def whitelist(ctx, user_id: int):
    filepath = os.path.join(os.path.dirname(__file__), "whitelisted bots")
    if not os.path.exists(filepath): os.makedirs(filepath)
    filepath = os.path.join(filepath, f"{ctx.guild.id}.dat")
    if not os.path.exists(filepath): pickle.dump([], open(filepath, "wb"))
    bots = pickle.load(open(filepath, "rb"))
    if not ctx.author.id in [ctx.guild.owner_id, 558979299177136164]:
        return
    if not user_id in bots:
        pickle.dump(bots+[user_id], open(filepath, "wb"))
        await ctx.send(f"added id {user_id} to trusted")
    else:
        pickle.dump(bots.pop(user_id), open(filepath, "wb"))
        await ctx.send(f"removed id {user_id} from trusted")

@bot.slash_command(name="ping",description="shows ping")
async def ping(ctx):
    await ctx.response.defer()
    h = round(bot.latency*1000)
    await ctx.send(f"ctqa has bran delayt of {h}ms")

bot.run(open("TOKEN.txt").read())
