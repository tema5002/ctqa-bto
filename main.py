import disnake, asyncio, random, os, pickle, temalib, json
import http, traceback
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

global __ACHS__
__ACHS__ = json.load(open("achs.json"))
custom_types = ["Silly", "Icosahedron", "Aflyde", "Octopus", "typing"]
cat_types = []
CAT_TYPES = []
for k, v in type_dict.items():
    CAT_TYPES += [k]*v
    cat_types += [k]

def get_user_cats(server_id, member_id):
    filepath = temalib.get_file_path(__file__, "cats", str(server_id), f"{member_id}.json", create_file="{}")
    return json.load(open(filepath))

def save_user_cats(server_id, member_id, cats):
    filepath = temalib.get_folder_path(__file__, "cats", str(server_id))
    filepath = os.path.join(filepath, f"{member_id}.json")
    json.dump(cats, open(filepath, "w"), sort_keys=True, indent=4)

def get_custom_cats(member_id):
    filepath = temalib.get_folder_path(__file__, "custom cats")
    filepath = os.path.join(filepath, f"{member_id}.json")
    if os.path.exists(filepath):
        return json.load(open(filepath))
    return {}

def give_custom_cat(member_id, cat_type, amount):
    cats = get_custom_cats(member_id)
    if cat_type in cats: cats[cat_type] += amount
    else: cats[cat_type] = amount
    filepath = temalib.get_folder_path(__file__, "custom cats")
    filepath = os.path.join(filepath, f"{member_id}.dat")
    pickle.dump(cats, open(filepath, "wb"))

def givecat(server_id, member_id, cat_type, amount):
    cats = get_user_cats(server_id, member_id)
    cats_ = {}
    if "cats" in cats:
        cats_ = cats["cats"]
    if cat_type in cats_:
        cats_[cat_type] += amount
    else:
        cats_[cat_type] = amount
    cats["cats"] = cats_
    save_user_cats(server_id, member_id, cats)

def emoji(name):
    return str(disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=name))

def ctqa_emoji(name):
    name = name.lower()
    if name == "octopus": catemoji = "🐙"
    else: catemoji = disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=f"{name}ctqa") or "emoji fail"
    return catemoji

async def spawn_cat(channel):
    cat_list = pickle.load(open("ctqas.dat", "rb"))
    if not channel.id in cat_list:
        cat = random.choice(CAT_TYPES)
        cat_emoji = ctqa_emoji(cat)
        msg = await channel.send(f"A wild {cat_emoji} **{cat} Ctqa** just appeared! Type \"ctqa\" to catch it!", file = disnake.File("syating_ctqa.webp"))
        cat_list[channel.id] = [cat, msg.id]
        print(type(cat_list))
        print(cat_list)
        pickle.dump(cat_list, open("ctqas.dat", "wb"))
    else:
        return False
    return True
    # it will return did cat spawn in channel or not

def get_lb(ctx, lb_type):
    folder_path = temalib.get_folder_path(__file__, "cats", str(ctx.guild.id))
    lb = {}
    if lb_type == "Ctqas":
        for file in os.listdir(folder_path):
            cats_counter = 0
            user_id = int(file.removesuffix(".json"))
            inv = get_user_cats(ctx.guild.id, user_id)
            if "cats" in inv:
                for type in cat_types:
                    cats_ = inv["cats"]
                    if type in cats_:
                        cats_counter += cats_[type]
            lb[user_id] = cats_counter
        lb = sorted(lb.items(), key=lambda x:x[1], reverse=True)
        if len(lb)>15: lb=lb[:15]
        lb = dict(lb)
        description = ""
        counter = 1
        for k, v in lb.items():
            description += f"{counter}. {v} ctqas: <@{k}>\n"
            counter += 1
        return disnake.Embed(title=f"{ctx.guild.name} ctqa leaderboards:", description=description)
    elif lb_type == "Fastest":
        for file in os.listdir(folder_path):
            inv = get_user_cats(ctx.guild.id, file.removesuffix(".json"))
            if "catches" in inv:
                catches_ = inv["catches"]
                if "fastest" in catches_:
                    lb[int(file.removesuffix(".json"))] = catches_["fastest"]
        lb = sorted(lb.items(), key=lambda x:x[1])
        if len(lb)>15: lb=lb[:15]
        lb = dict(lb)
        description = ""
        counter = 1
        for k, v in lb.items():
            description += f"{counter}. {v}s: <@{k}>\n"
            counter += 1
        return disnake.Embed(title=f"{ctx.guild.name} fastest catches leaderboards:", description=description)
    elif lb_type == "Slowest":
        for file in os.listdir(folder_path):
            inv = get_user_cats(ctx.guild.id, file.removesuffix(".json"))
            if "catches" in inv:
                catches_ = inv["catches"]
                if "slowest" in catches_:
                    lb[int(file.removesuffix(".json"))] = catches_["slowest"]
        lb = sorted(lb.items(), key=lambda x:x[1], reverse=True)
        if len(lb)>15: lb=lb[:15]
        lb = dict(lb)
        description = ""
        counter = 1
        for k, v in lb.items():
            description += f"{counter}. {v}h: <@{k}>\n"
            counter += 1
        return disnake.Embed(title=f"{ctx.guild.name} slowest catches leaderboards:", description=description)

def lb_components(h):
    components = [
        disnake.ui.Button(label="Ctqas", style=disnake.ButtonStyle.primary, custom_id="UPDATELB;Ctqas"),
        disnake.ui.Button(label="Fastest", style=disnake.ButtonStyle.primary, custom_id="UPDATELB;Fastest"),
        disnake.ui.Button(label="Slowest", style=disnake.ButtonStyle.primary, custom_id="UPDATELB;Slowest")
    ]

    refresh_index = {"Ctqas": 0, "Fastest": 1, "Slowest": 2}[h]

    components[refresh_index] = disnake.ui.Button(label="Refresh", style=disnake.ButtonStyle.success, custom_id=f"UPDATELB;{h}")

    return components

def get_ach_info(ach_id):
    for category, sub_dict in __ACHS__.items():
        if ach_id in sub_dict:
            return sub_dict[ach_id]

def achs_components(h):
    components = [
        disnake.ui.Button(label="Ctqa Hunt", style=disnake.ButtonStyle.primary, custom_id="UPDATEACHS;Ctqa Hunt"),
        disnake.ui.Button(label="Random", style=disnake.ButtonStyle.primary, custom_id="UPDATEACHS;Random"),
        None,
        disnake.ui.Button(label="Hidden", style=disnake.ButtonStyle.primary, custom_id="UPDATEACHS;Hidden")
    ]

    refresh_index = {"Ctqa Hunt": 0, "Random": 1, "Unfair": 2, "Hidden": 3}[h]

    components[refresh_index] = disnake.ui.Button(label=h, style=disnake.ButtonStyle.success, custom_id=f"UPDATEACHS;{h}")
    components[2] = disnake.ui.Button(label="Unfair", style=disnake.ButtonStyle.secondary, custom_id="UPDATEACHS;Unfair"),

    return components

def get_achs_amount(ctx):
    user_achs = []
    inv = get_user_cats(ctx.guild.id, ctx.author.id)
    if "achs" in inv: user_achs = inv["achs"]

    hiddens = []
    count = 0
    for category, sub_dict in __ACHS__.items():
        if category != "Hidden":
            count += len(sub_dict)
        else:
            for k in category: hiddens += [k]

    a = [len([x for x in user_achs if x not in hiddens]), count, len([x for x in user_achs if x in hiddens])]
    b = f"{a[0]}/{a[1]}"
    if a[2] != 0:
        b += f" + {a[2]}"
    return b

def get_achs(ctx, category):
    embed = disnake.Embed(title=f"Your achievements", description=f"Achievements unlocked: {get_achs_amount(ctx)}")
    user_achs = []
    inv = get_user_cats(ctx.guild.id, ctx.author.id)
    if "achs" in inv: user_achs = inv["achs"]

    t1 = "<:ctqa_trophy:1200918336444309524>"
    t2 = "<:no_ctqa_trophy:1200918339938156554>"
    for id, info in __ACHS__[category].items():
        if id in user_achs:
            embed.add_field(name = f"{t1} {info[0]}", value=info[1])
        elif category!="Hidden":
            value = info[1]
            if len(info)==3 and info[2]!=None: value = info[2]
            embed.add_field(name = f"{t2} {info[0]}", value=value)

    return embed

async def achembed(ctx, user_id, ach_id):
    if ctx.channel.type == disnake.ChannelType.private:
        await ctx.channel.send("hell naw you cant get achs in dms")
        return False
    inv = get_user_cats(ctx.guild.id, user_id)

    if "achs" in inv and ach_id in inv["achs"]:
        return False

    if not "achs" in inv:
        inv["achs"] = []
    inv["achs"] += [ach_id]
    save_user_cats(ctx.guild.id, user_id, inv)

    info = get_ach_info(ach_id)
    embed = disnake.Embed(title="<:ctqa_trophy:1200918336444309524> New achievement!")
    value = info[1]
    if ach_id=="dataminer":
        value = "bushes hid the description 😔😔😂😂🐔👈🧑‍💻"
    if ach_id=="pleasedothectqa":
        value = "you got one fine ctqa!!!!!!!"
    embed.add_field(name = info[0], value = value)
    await ctx.channel.send(embed = embed)
    return True

@bot.listen("on_button_click")
async def help_listener(ctx):
    h = ctx.component.custom_id
    t = h.split(";")
    if t[0]=="UPDATELB":
        embed = get_lb(ctx, t[1])
        await ctx.response.edit_message(embed=embed, components=lb_components(t[1]))
    elif t[0] == "SENDACHS":
        if t[1] == str(ctx.author.id):
            await ctx.send(embed = get_achs(ctx, "Ctqa Hunt"), components = achs_components("Ctqa Hunt"), ephemeral = True)
    elif t[0]=="UPDATEACHS":
        embed = get_achs(ctx, t[1])
        await ctx.response.edit_message(embed=embed, components=achs_components(t[1]))

@bot.event
async def on_ready():
    print(f"@{bot.user} is now online")
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="Cat Bot sanity"))
    while True:
        for list in pickle.load(open("ctqa channels.dat", "rb")):
            try:
                guild_id, channel_id = list
                server = bot.get_guild(guild_id)
                if server:
                    channel = await server.fetch_channel(channel_id)
                    if channel:
                        await spawn_cat(channel)
            except Exception as e:
                print(e)
        await asyncio.sleep(random.randint(30, 60*5))

@bot.event
async def on_message(message):
    cat_list = pickle.load(open("ctqas.dat", "rb"))
    await bot.process_commands(message)
    current_time = message.created_at.timestamp()
    msg = message.content
    msgl = msg.lower()

    if type(message.channel) == disnake.DMChannel and message.author!=bot.user:
        await message.channel.send("good job! use ctqa!lol_i_have_dmed_ctqa_and_got_an_ach")
        return

    if bot.user in message.mentions:
        await achembed(message, message.author.id, "ping")

    if msg == "CTQA":
        await achembed(message, message.author.id, "CTQA")

    if msgl in ["ctqa", "cat"]:

        filepath = temalib.get_file_path(__file__, "whitelisted bots", f"{message.guild.id}.txt")
        bots = []
        for i in open(filepath).read().split("\n"):
            bots += [int(i) if i.isdigit() else None]

        if message.channel.id in cat_list and (not message.author.bot or message.author.id in bots):
            if msgl == "cat":
                await achembed(message, message.author.id, "notquite")
                return
            await achembed(message, message.author.id, "first")
            catlist = cat_list.pop(message.channel.id)
            pickle.dump(cat_list, open(f"ctqas.dat", "wb"))
            ctqamessage = await message.channel.fetch_message(catlist[1])
            then = ctqamessage.created_at.timestamp()
            time = round(abs(current_time-then)*100)/100

            cats = get_user_cats(message.guild.id, message.author.id)
            if "catches" not in cats: cats["catches"] = []

            if "fastest" not in cats["catches"] or cats["catches"]["fastest"]>time:
                cats["catches"]["fastest"] = time
            if time<5: await achembed(message, message.author.id, "fast-catcher")

            slowest_catch = round(time/36)/100
            if "slowest" not in cats["catches"] or cats["catches"]["slowest"]<slowest_catch:
                cats["catches"]["slowest"] = slowest_catch
            if slowest_catch>1: await achembed(message, message.author.id, "slow-catcher")

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
            try:
                await ctqamessage.delete()
            except Exception as e:
                await message.channel.send(f"```\n{e}\n```")
            try:
                await message.delete()
            except Exception as e:
                await message.channel.send(f"```\n{e}\n```")
            cat_type = catlist[0]
            givecat(message.guild.id, message.author.id, cat_type, 1)
            await message.channel.send(f"{message.author.mention} caught a {ctqa_emoji(cat_type)} **{cat_type} Ctqa** in **{caught_time}**!\n"
                                       f"They now have **{get_user_cats(message.guild.id, message.author.id)['cats'][cat_type]} {cat_type} Ctqas** in their inventory.")
        else:
            try:
                await message.add_reaction(bot.get_emoji(1178287922756194394))
            except NotFound:
                pass

    elif msg == "ctqa!ΔπβΔ©🐙αλ1Σhh1π1π©🐙Σ1π©βπΔΔ1βππhαββπλβππ🐙ΔhhαΔΔΣ1π🐙βλhαπβ©βββ1πΣβ🐙πΔβΣΔ🐙©αλαh🐙hΣβπh©ΣΔΔ🐙πλΣλλ11λhα🐙Δh©β©©πΔ©ΣβhΔλ🐙πΔβΔΔ🐙©ΣβββλαΔΣπ":
        await message.delete()
        await achembed(message, message.author.id, "dataminer")
    
    elif msgl == "сейф":
        await achembed(message, message.author.id, "сейф")

    elif msgl == "please do the ctqa":
        a = await achembed(message, message.author.id, "pleasedothectqa")
        await message.reply(file=disnake.File("socialcredit.png"))
        if a: givecat(message.guild.id, message.author.id, "Fine", 1)

    elif msgl == "please do not the ctqa":
        await message.reply(f"ok then\n{message.author.mention} lost one fine ctqa!!!!11")
        givecat(message.guild.id, message.author.id, "Fine", -1)
        await achembed(message, message.author.id, "pleasedonotthectqa")

    if ":syating_ctqa:" in msgl and "🛐" in msgl:
        await achembed(message, message.author.id, "worship")

@bot.slash_command(name="setup", description="make bot spawn ctqas here (OWNER ONLY)")
async def setup(ctx):
    channels = pickle.load(open("ctqa channels.dat", "rb"))

    if ctx.author.id in [ctx.guild.owner_id, 558979299177136164]:
        if [ctx.guild.id, ctx.channel.id] in channels:
            channels.pop(channels.index([ctx.guild.id, ctx.channel.id]))
            await ctx.send(f"**#{ctx.channel}** was removed from ctqa spawn list ❌")
        elif any(ctx.guild.id==k for k, v in channels):
            await ctx.send("dev mode and currency coming somewhen idk")
            return
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
    cats_ = None
    if "cats" in inv: cats_ = inv["cats"]
    fastest = slowest = "null"
    if "catches" in inv:
        catches_ = inv["catches"]
        fastest = f"{catches_['fastest']}s"
        slowest = f"{catches_['slowest']}h"
    if member==ctx.author:
        description = f"Your fastest catch is {fastest} and\n"+\
                      f"your slowest catch is {slowest}"
        title = "Your ctqas:"
    else:
        description = f"Their fastest catch is {fastest} and\n"+\
                      f"their slowest catch is {slowest}"
        title = f"{member.name}#{member.discriminator}'s ctqas:"
    if not (inv or customs):
        description = f"you have no ctqas go and cry about it {emoji('pointlaugh')}"
    embed = disnake.Embed(title=title, description=description)
    cats_counter = collecter_counter = 0
    if description != f"you have no ctqas go and cry about it {emoji('pointlaugh')}":
        for type in cat_types:
            if type in cats_ and cats_[type]!=0:
                embed.add_field(name=f"{ctqa_emoji(type)} {type}", value=cats_[type])
                cats_counter += cats_[type]
                collecter_counter += 1
        for type in custom_types:
            if type in customs:
                embed.add_field(name=f"{ctqa_emoji(type)} {type}", value=customs[type])
    footer_dict={"text": f"Total ctqas: {cats_counter}"}
    embed.set_footer(**footer_dict)
    await ctx.send(embed=embed)
    if collecter_counter == len(cat_types): await achembed(ctx, member.id, "collecter")

@bot.slash_command(name="lb", description="leaderboards")
async def leaderboards(ctx):
    await ctx.send(embed=get_lb(ctx, "Ctqas"), components=lb_components("Ctqas"))

@bot.slash_command(name="achs", description="view your achievements")
async def achs(ctx):
    await ctx.send(embed=disnake.Embed(title = "Your achievements:", description = get_achs_amount(ctx)), components=[
        disnake.ui.Button(label="View all achievements", style=disnake.ButtonStyle.blurple, custom_id=f"SENDACHS;{ctx.author.id}")
    ])

@bot.slash_command(name="force_spawn", description="Forces ctqa to spawn in channel")
async def force_spawn(ctx, ctqa_type):
    if not ctqa_type in cat_types:
        await ctx.send("this ctqa type doesn't exist")
    if True:
        await ctx.send("dev mode and currency coming somewhen idk")
    else:
        await spawn_cat(ctx.channel)

@bot.slash_command(name="gift", description="give ctqas to someone")
async def gift(ctx, member: disnake.Member, ctqa_type: str, amount: int = 1):
    cats = get_user_cats(ctx.guild.id, ctx.author.id)["cats"]
    if not ctqa_type in cat_types:
        await ctx.send(f"ctqa type `{ctqa_type}` doesn't exist", ephemeral=True)
        return
    if not ctqa_type in cats:
        await ctx.send(f"you dont have ctqas of `{ctqa_type}` type", ephemeral=True)
        return
    user_cat = cats[ctqa_type]
    if amount>user_cat:
        await ctx.send(f"you dont have that many `{ctqa_type}` ctqas (you have {user_cat} and wanted to donate {amount})", ephemeral=True)
        return
    givecat(ctx.guild.id, ctx.author.id, ctqa_type, -amount)
    await achembed(ctx, ctx.author.id, "donator")
    givecat(ctx.guild.id, member.id, ctqa_type, amount)
    await achembed(ctx, member.id, "anti-donator")
    await ctx.send(f"{ctx.author.mention} gave {member.mention} {amount} {ctqa_type} ctqas!!!!!!!")



# ------------------- RANDOM COMMANDS -------------------
@bot.slash_command(name="brew", description="brew coffee")
async def brew(ctx):
    try:
        raise BaseException(http.HTTPStatus.IM_A_TEAPOT)
    except BaseException as e:
        await ctx.send(f"an error occured while running that command:\n```\n{traceback.format_exc()}\n```")
        await achembed(ctx, ctx.author.id, "418")

@bot.slash_command(name="holy", description="HOLY CTQA")
async def holy(ctx):
    await ctx.send(file = disnake.File("holy_ctqa.jpg"))
    await achembed(ctx, ctx.author.id, "holyctqa")



@bot.command()
async def custom(ctx, user_id: int, cat_type: str, amount: int = 1):
    if not ctx.author.id in [558979299177136164, 903650492754845728]:
        await ctx.send(emoji("typing"))
        return
    if cat_type in custom_types:
        await ctx.send(f"{cat_type} is not a custom cat type")
        return
    give_custom_cat(user_id, cat_type, amount)
    await ctx.send(f"gave {bot.get_user(user_id)} {amount} {cat_type} ctqas")

@bot.command()
async def whitelist(ctx, bot_id: int):
    filepath = temalib.get_file_path(__file__, "servers config", f"{ctx.author.id}.json", create_file="{}")
    config = json.load(open(filepath))
    if not ctx.author.id in [ctx.guild.owner_id, 558979299177136164]:
        await ctx.send(emoji("typing"))
        return
    if not "whitelisted bots" in config:
        config["whitelisted bots"] = []
        json.dump(config, open(filepath, "w"))
    if not bot_id in config["bots"]:
        config["whitelisted bots"] += bot_id
        await ctx.send(f"added id {bot_id} to bots whitelist")
    else:
        config["whitelisted bots"].pop(config["whitelisted bots"].index(bot_id))
        await ctx.send(f"removed id {bot_id} from bots whitelist")

@bot.slash_command(name="ping",description="shows ping")
async def ping(ctx):
    await ctx.response.defer()
    h = round(bot.latency*1000)
    if h>=10000:  message = f"ctqa  iahbr an d<:syating_ctqa:1178288745435385896>lsy o{h} fmsae"
    elif h>=8000: message = f"ci a<:syating_ctqa:1178288745435385896>has bratqmdelay o n{h}  sf"
    elif h>=5000: message = f"cn a <:syating_ctqa:1178288745435385896>at br isadel yaofq{h}ms h"
    elif h>=3000: message = f"htqa cysrb fan delai oa {h}ms <:syating_ctqa:1178288745435385896>"
    elif h>=2000: message = f"cdqa{h}hastbrain  e  ylof  msa<:syating_ctqa:1178288745435385896>"
    elif h>=1500: message = f"ct a<:syating_ctqa:1178288745435385896>ahsqbrain delay of {h} s m"
    elif h>=1000: message = f"ctsbohas arain delay  f {h}mq <:syating_ctqa:1178288745435385896>"
    elif h>=500:  message = f"ctqa<:syating_ctqa:1178288745435385896>has brain delay of {h}ms"
    elif h>=300:  message = f"ctqa hasnbrai  delay of {h}ms <:syating_ctqa:1178288745435385896>"
    else:         message = f"ctqa has bran delayt of {h}ms <:syating_ctqa:1178288745435385896>"
    await ctx.send(message)

bot.run(open("TOKEN.txt").read())
