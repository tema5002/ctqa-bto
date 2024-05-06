import asyncio
import math
import os
import pickle
import random
from typing import Type, Any

import antigrav as json
import disnake
import temalib
from disnake.ext import commands
from disnake.ui import Button

from achs import achs

blurple = disnake.ButtonStyle.blurple
green = disnake.ButtonStyle.success
gray = disnake.ButtonStyle.primary

bot = commands.Bot(command_prefix="ctqa!", help_command=None, intents=disnake.Intents.all())
cats_file: Type = dict[str, list[str] | dict[str, float] | dict[str, int] | dict[str | complex]]

type_dict = {
    "Fine": 1000,
    "Nice": 750,
    "Good": 650,
    "Uncommon": 500,
    "Rare": 350,
    "Wild": 275,
    "Baby": 230,
    "Old": 200,
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

custom_types = ["Silly", "Icosahedron", "Aflyde", "Octopus", "typing", "Kesslon", "Bread", "Blep", "cake64",
                "antaegeav"]
cat_types = []
CAT_TYPES = []
for k, v in type_dict.items():
    CAT_TYPES += [k] * v
    cat_types += [k]


# ------ quadrillion functions here ------
def repr_complex(number: int | complex) -> str:
    real = str(number.real)
    imag = str(number.imag) if number.imag else ""
    if real == "inf":
        real = "∞"
    if imag == "inf":
        imag = "∞"
    if real == "nan":
        real = "🍏"
    if imag == "nan":
        imag = "🍏"
    return real + (("+" + imag + "i") if imag else "")


def skill_issued(member: disnake.Member) -> bool:
    return not (member.guild_permissions.administrator or member.id in trustedpeople)


def get_lb(ctx, lb_type: str) -> disnake.Embed:
    folder_path = temalib.get_folder_path(__file__, "cats", str(ctx.guild.id))
    lb = {}
    if lb_type == "Ctqas":
        for file in os.listdir(folder_path):
            user_id = int(file.removesuffix(".antigrav"))
            cats_: dict[str, int | complex] = get_user_cats(ctx.guild.id, user_id).get("cats", {})
            lb[user_id] = sum(cats_.get(i, 0) for i in cat_types)
        lb = sorted(lb.items(), key=lambda x: x[1].real, reverse=True)
        if len(lb) > 15:
            lb = lb[:15]
        return disnake.Embed(
            title=f"{ctx.guild.name} ctqa leaderboards:",
            description='\n'.join(
                f"{c}. {repr_complex(t[1])} ctqas: <@{t[0]}>" for c, t in enumerate(lb))
        )
    elif lb_type == "Fastest":
        for file in os.listdir(folder_path):
            inv = get_user_cats(ctx.guild.id, file.removesuffix(".antigrav"))
            if "catches" in inv:
                catches_ = inv["catches"]
                if "fastest" in catches_:
                    lb[int(file.removesuffix(".antigrav"))] = catches_["fastest"]
        lb = sorted(lb.items(), key=lambda x: x[1])
        if len(lb) > 15:
            lb = lb[:15]
        lb = dict(lb)
        description = ""
        counter = 1
        for k, v in lb.items():
            description += f"{counter}. {v}s: <@{k}>\n"
            counter += 1
        return disnake.Embed(title=f"{ctx.guild.name} fastest catches leaderboards:", description=description)
    elif lb_type == "Slowest":
        for file in os.listdir(folder_path):
            inv = get_user_cats(ctx.guild.id, file.removesuffix(".antigrav"))
            if "catches" in inv:
                catches_ = inv["catches"]
                if "slowest" in catches_:
                    lb[int(file.removesuffix(".antigrav"))] = catches_["slowest"]
        lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)
        if len(lb) > 15:
            lb = lb[:15]
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

    components[refresh_index] = disnake.ui.Button(label="Refresh", style=disnake.ButtonStyle.success,
                                                  custom_id=f"UPDATELB;{h}")

    return components


def get_achs_amount(ctx):
    user_achs = get_user_cats(ctx.guild.id, ctx.author.id).get("achs", [])

    hiddens = []
    count = 0
    for category, sub_dict in achs.items():
        if category != "Hidden":
            count += len(sub_dict)
        else:
            for k in sub_dict:
                hiddens.append(k)

    a = [len([x for x in user_achs if x not in hiddens]), count, len([x for x in user_achs if x in hiddens])]
    b = f"{a[0]}/{a[1]}"
    if a[2] != 0:
        b += f" + {a[2]}"
    return b


def get_achs(ctx, category):
    embed = disnake.Embed(title=f"Your achievements", description=f"Achievements unlocked: {get_achs_amount(ctx)}")
    user_achs = get_user_cats(ctx.guild.id, ctx.author.id).get("achs", [])

    t1 = "<:ctqa_trophy:1200918336444309524>"
    t2 = "<:no_ctqa_trophy:1200918339938156554>"
    for id_, info in achs[category].items():
        if id_ in user_achs:
            embed.add_field(name=f"{t1} {info[0]}", value=info[1])
        elif category != "Hidden":
            value = info[1]
            if len(info) == 3 and info[2]:
                value = info[2]
            embed.add_field(name=f"{t2} {info[0]}", value=value)

    return embed


async def achembed(ctx, user: disnake.User | disnake.Member, ach_id: str) -> bool:
    if ctx.channel.type == disnake.ChannelType.private:
        await ctx.channel.send("hell naw you cant get achs in dms")
        return False
    inv = get_user_cats(ctx.guild.id, user.id)
    inv["achs"] = inv.get("achs", [])

    if ach_id in inv["achs"]:
        return False

    inv["achs"].append(ach_id)
    save_user_cats(ctx.guild.id, user.id, inv)

    info = get_ach_info(ach_id)
    embed = disnake.Embed(title="<:ctqa_trophy:1200918336444309524> New achievement!")
    value = info[1]
    if ach_id == "dataminer":
        value = "bushes hid the description 😔😔😂😂"
    if ach_id == "pleasedothectqa":
        value = "you got one fine ctqa!!!!!!!"
    embed.add_field(name=info[0], value=value)
    footer_dict = {"text": f"Unlocked by @{user}"}
    embed.set_footer(**footer_dict)
    await ctx.channel.send(embed=embed)
    return True


def achs_components(h):
    components = [
        Button(label="Ctqa Hunt", style=gray, custom_id="UPDATEACHS;Ctqa Hunt"),
        Button(label="Random", style=gray, custom_id="UPDATEACHS;Random"),
        Button(label="Unfair", style=gray, custom_id="UPDATEACHS;Unfair"),
        Button(label="Hidden", style=gray, custom_id="UPDATEACHS;Hidden")
    ]

    refresh_index = {"Ctqa Hunt": 0, "Random": 1, "Unfair": 2, "Hidden": 3}[h]

    components[refresh_index] = Button(label=h, style=green, custom_id=f"UPDATEACHS;{h}")

    return components


def get_ach_info(ach_id):
    for _, sub_dict in achs.items():
        if ach_id in sub_dict:
            return sub_dict[ach_id]


def get_config(message: disnake.Message):
    return json.load(open(
        temalib.get_file_path(__file__, "servers config", f"{message.guild.id}.antigrav", create_file="{}"))
    )


def get_user_cats(server_id: int | str, member_id: int | str) -> cats_file:
    return json.load(open(temalib.get_file_path(
        __file__, "cats", str(server_id), f"{member_id}.antigrav",
        create_file="{}"
    )))


def save_user_cats(server_id: int | str, member_id: int | str, cats: cats_file) -> None:
    json.dump(cats, open(
        temalib.get_file_path(
            __file__, "cats", str(server_id), f"{member_id}.antigrav"),
        "w"), sort_keys=True, indent=4)


def get_custom_cat(member_id: int):
    return temalib.openfile(temalib.get_file_path(__file__, "custom cats", f"{member_id}.txt")).read()


def set_custom_cat(member_id: int, cat_type: str) -> None:
    temalib.editfile(temalib.get_file_path(__file__, "custom cats", f"{member_id}.txt")).write(cat_type)


def give_cat(server_id: int, member_id: int, cat_type: str, amount: int) -> int | complex:
    cats = get_user_cats(server_id, member_id)
    if not cats.get("cats"):
        cats["cats"] = {}
    if cat_type in cats["cats"]:
        cats["cats"][cat_type] += amount
    else:
        cats["cats"][cat_type] = amount
    save_user_cats(server_id, member_id, cats)
    return cats["cats"][cat_type]


# noinspection PyTypeChecker
def give_imag_cat(server_id: int, member_id: int, cat_type: str, amount: int) -> None:
    cats = get_user_cats(server_id, member_id)
    cats["cats"] = cats.get("cats", {})
    cats["cats"][cat_type] = cats["cats"].get(cat_type, 0) + amount * 1j
    save_user_cats(server_id, member_id, cats)


async def get_channel(server_id: int, channel_id: int):
    channel = bot.get_channel(channel_id)
    channel = channel or await bot.get_guild(server_id).fetch_channel(channel_id)
    return channel


def emoji(name: str) -> str:
    return str(disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=name))


def ctqa_emoji(name: str) -> str:
    name = name.lower()
    if name == "octopus":
        return "🐙"
    if name == "antaegeav":
        return "<:antaegeav:1184160903512461392>"
    if name == "cake64":
        return "<:cake64:1217822864473067542>"
    return disnake.utils.get(bot.get_guild(1178285875608698951).emojis, name=f"{name}ctqa") or "emoji fail"


emojis_list = []


async def start_message(channel: disnake.abc.Messageable) -> disnake.Message:
    emodeez = ''.join(str(random.choice(emojis_list)) for _ in range(random.randint(25, 50)))
    return await channel.send(f"<@&1231915005730095186> i have started {emodeez}")


async def spawn_cat(channel: disnake.abc.Messageable) -> bool:
    # noinspection LongLine
    bruvver = [
        "javax.swing.text.JTextComponent",
        "кутукьюа",
        "кукумбер 🦂",
        "Скарпион 🥒",
        "чо за фигню ты нисёш 🙄💅 пажалуста удали ето 😨 у миня радители в комноте 👨‍👩‍👧 аааааааааа 🥸 please delete this now 🥺 окей 👍 тебе ПАНЯТНА ИЛИ НЕТ 🤨 УДОЛЯЙ ЭТО СЕЙЧАЗ 💀 ААААААААА 😊",
        "sake 🍶🤧"
    ]
    cat_list = pickle.load(open("ctqas.dat", "rb"))
    if channel.id not in cat_list:
        cat = random.choice(CAT_TYPES)
        cat_emoji = ctqa_emoji(cat)
        brumbler = random.choice(bruvver) if random.randint(0, 9) == 0 else "ctqa"
        if channel.id == 1230933738561474580:
            msg = f"hey <@1030817797921583236> do you want to catch a {brumbler} ⛈️⛈️⛈️⛈️⛈️⛈️⛈️"
        else:
            msg = f'A wild {cat_emoji} **{cat} Ctqa** just appeared! Type "{brumbler}" to catch it!'
        msg = await channel.send(msg, file=get_ctqa_image(cat))
        cat_list[channel.id] = {"type": cat, "id": msg.id, "say_to_catch": brumbler}
        pickle.dump(cat_list, open("ctqas.dat", "wb"))
    else:
        return False
    return True
    # it will return did cat spawn in channel or not


def get_ctqa_image(ctqa_type: str) -> disnake.File:
    filename = "syating_ctqa.webp"
    if ctqa_type == "Inverted":
        filename = "inverted_ctqa.webp"
    if ctqa_type == "Reverse":
        filename = "reverse_ctqa.webp"
    if ctqa_type == "Professor":
        filename = "professor_ctqa.webp"
    if ctqa_type == "Baby":
        filename = "baby_ctqa.webp"
    return disnake.File(temalib.get_file_path(__file__, "ctqas that are syating", filename))


@bot.listen("on_button_click")
async def help_listener(ctx):
    h = ctx.component.custom_id
    t = h.split(";")
    if t[0] == "UPDATELB":
        embed = get_lb(ctx, t[1])
        await ctx.response.edit_message(embed=embed, components=lb_components(t[1]))
    elif t[0] == "SENDACHS":
        if t[1] == str(ctx.author.id):
            await ctx.send(
                embed=get_achs(ctx, "Ctqa Hunt"),
                components=achs_components("Ctqa Hunt"),
                ephemeral=True)
        else:
            await ctx.send(
                f"{ctx.author.mention} чел ну ты и чел типо ну чел ну ты и чел капец чел чел чел саратов и смерть чел"
                f"ну ты вообще ну че чел ты ткаой чел блин чел ну чел ну ты чел вообще чел чел 🍰🍰🍰",
                delete_after=60)
    elif t[0] == "UPDATEACHS":
        embed = get_achs(ctx, t[1])
        await ctx.response.edit_message(embed=embed, components=achs_components(t[1]))


# pycharm is a wuggy games
@bot.event
async def on_ready():
    for s in [
        1202574174946861076,  # h++
        938770488702951545,  # Aflyde's lab
        1183418786481700925,  # this server is real fucked up bruh
        1132235625609834596,  # proglet software
        1042064947867287643,  # Slinx's Attic
        1178285875608698951,  # ctqa stnad
        854614974525472798,  # a silly server
        1082525827511627916,  # rech2020's server
        1206253771659804702  # this server is real fucked up
    ]:
        if s := bot.get_guild(s):
            emojis_list.extend(e for e in s.emojis if e.available)
    channel = await get_channel(1178285875608698951, 1231914439167709216)
    message = await start_message(channel)
    while True:
        try:
            await message.add_reaction(random.choice(emojis_list))
        except disnake.errors.Forbidden:
            break

    presences = [
        disnake.Activity(type=disnake.ActivityType.watching, name="Cat Bot sanity"),
        disnake.Activity(type=disnake.ActivityType.custom, name="blame babybear")
    ]
    print(f"@{bot.user} is now ready")
    while True:
        ctqa_channels: list[tuple[int, int]] = pickle.load(open("ctqa channels.dat", "rb"))
        for ids in ctqa_channels:
            try:
                await spawn_cat(await get_channel(*ids))
            except AttributeError:
                ctqa_channels.remove(ids)
        pickle.dump(ctqa_channels, open("ctqa channels.dat", "wb"))

        await bot.change_presence(activity=random.choice(presences))
        await asyncio.sleep(random.randint(60, 60 * 10))


@bot.event
async def on_message(message: disnake.Message):
    await bot.process_commands(message)
    cat_list = pickle.load(open("ctqas.dat", "rb"))
    bruvver = cat_list.get(message.channel.id, {}).get("say_to_catch", "ctqa")
    current_time = message.created_at.timestamp()
    msg = message.content
    msgl = msg.lower()

    if isinstance(message.channel, disnake.DMChannel) and message.author != bot.user:
        await message.channel.send("good job! use ctqa!lol_i_have_dmed_ctqa_and_got_an_ach")
        return

    if bot.user in message.mentions:
        await achembed(message, message.author, "ping")

    if msg == bruvver.upper():
        if bruvver == "ctqa":
            await achembed(message, message.author, "CTQA")
        else:
            await achembed(message, message.author, "NOTCTQA")

    # noinspection LongLine
    if msgl in ["cat", bruvver.lower()]:
        config = get_config(message)
        bots = config.get("whitelisted bots", [])

        if message.channel.id in cat_list and (not message.author.bot or message.author.id in bots):
            if msgl == "cat":
                await achembed(message, message.author, "notquite")
                return
            await achembed(message, message.author, "first")
            catlist = cat_list.pop(message.channel.id)
            pickle.dump(cat_list, open(f"ctqas.dat", "wb"))
            ctqamessage = await message.channel.fetch_message(catlist.get("id", -1))
            then = ctqamessage.created_at.timestamp()
            time = round(abs(current_time - then), 2)

            cats = get_user_cats(message.guild.id, message.author.id)
            if not cats.get("catches"):
                cats["catches"] = {}

            catches = cats.get("catches")
            fastest = catches.get("fastest", math.inf)
            if time < fastest:
                cats["catches"]["fastest"] = time
            if time < 5:
                await achembed(message, message.author, "fastcatcher")

            slowest_catch = round(time / 3600, 2)
            if catches.get("slowest", -2) < slowest_catch:
                cats["catches"]["slowest"] = slowest_catch
            if 1 < slowest_catch:
                await achembed(message, message.author, "slowcatcher")

            save_user_cats(message.guild.id, message.author.id, cats)

            days = int(time // 86400)
            hours = int(time // 3600 % 24)
            mins = int(time // 60 % 60)
            secs = time % 60
            caught_time = ""
            if days:
                caught_time += f"{days} days "
            if hours:
                caught_time += f"{hours} hours "
            if mins:
                caught_time += f"{mins} minutes "
            if secs:
                caught_time += f"{round(secs, 2)} seconds"
            caught_time = caught_time.strip()
            try:
                await ctqamessage.delete()
            except Exception as e:
                await message.channel.send(f"failed to deleted ctqa spawn message\n```\n{e}\n```")
            try:
                await message.delete()
            except Exception as e:
                await message.channel.send(f"failed to deleted ctqa message\n```\n{e}\n```")
            cat_type = catlist.get("type", "Unknown")
            ctqas = give_cat(message.guild.id, message.author.id, cat_type, 1)
            await message.channel.send(f"""
{message.author.mention} caught a {ctqa_emoji(cat_type)} **{cat_type} Ctqa** in **{caught_time}**!
You now have **{repr_complex(ctqas)} {cat_type} Ctqas** in your inventory."""
                                       )
        elif msgl != "cat":
            try:
                await message.add_reaction(bot.get_emoji(1178287922756194394))
            except NotFound:
                pass

    elif msg == "ctqa!ΔπβΔ©🐙αλ1Σhh1π1π©🐙Σ1π©βπΔΔ1βππhαββπλβππ🐙ΔhhαΔΔΣ1π🐙βλhαπβ©βββ1πΣβ🐙πΔβΣΔ🐙©αλαh🐙hΣβπh©ΣΔΔ🐙πλΣλλ11λhα🐙Δh©β©©πΔ©ΣβhΔλ🐙πΔβΔΔ🐙©ΣβββλαΔΣπ":
        await message.delete()
        await achembed(message, message.author, "dataminer")

    elif msgl == "сейф":
        await achembed(message, message.author, "сейф")

    elif msgl == "please do the ctqa":
        a = await achembed(message, message.author, "pleasedothectqa")
        await message.reply(file=disnake.File("socialcredit.png"))
        if a:
            give_cat(message.guild.id, message.author.id, "Fine", 1)

    elif msgl == "please do not the ctqa":
        await message.reply(f"ok then\n{message.author.mention} lost one fine ctqa!!!!11")
        give_cat(message.guild.id, message.author.id, "Fine", -1)
        await achembed(message, message.author, "pleasedonotthectqa")

    if ":syating_ctqa:" in msgl and "🛐" in msgl:
        await achembed(message, message.author, "worship")

    if "ctqa!lol_i_have_dmed_ctqa_and_got_an_ach" == msg:
        await achembed(message, message.author, "dm")


@bot.slash_command(name="setup", description="make bot spawn ctqas here (ADMIN ONLY)")
async def setup(ctx):
    await ctx.response.defer()
    channels: list[tuple[int, int]] = pickle.load(open("ctqa channels.dat", "rb"))

    if not skill_issued(ctx.author):
        if (ctx.guild.id, ctx.channel.id) in channels:
            channels.remove((ctx.guild.id, ctx.channel.id))
            await ctx.send(f"**#{ctx.channel}** was removed from ctqa spawn list ❌")
        else:
            h = True
            for guild_id, channel_id in channels:
                if ctx.guild.id == guild_id:
                    if channel_id not in [i.id for i in ctx.guild.channels]:
                        await ctx.send("there is ctqas loop linked to some non existent channel (removed it)")
                        channels.remove((ctx.guild.id, v))
                        h = False
                    else:
                        await ctx.send("you cant link ctqas to several channels")
            if h:
                channels.append((ctx.guild.id, ctx.channel.id))
                await ctx.send(f"**#{ctx.channel}** was added to ctqa spawn list ✅")
        pickle.dump(channels, open("ctqa channels.dat", "wb"))
    else:
        await ctx.send(f"lmao perms fail imagine having a skill issue {emoji('pointlaugh')}")


@bot.slash_command(name="inv", description="inventory")
async def inventory(ctx, member: disnake.Member = None):
    member = member or ctx.author
    inv = get_user_cats(ctx.guild.id, member.id)
    custom = get_custom_cat(member.id)
    cats_ = inv.get("cats", [])
    fastest = slowest = "null"
    if "catches" in inv:
        catches = inv["catches"]
        fastest = f"{catches['fastest']}s"
        slowest = f"{catches['slowest']}h"
    description = f"Your fastest catch is {fastest} and\n" + \
                  f"your slowest catch is {slowest}"
    title = "Your ctqas:"
    if member != ctx.author:
        description = f"Their fastest catch is {fastest} and\n" + \
                      f"their slowest catch is {slowest}"
        title = f"{member}'s ctqas:"
    if not (inv or custom):
        description = f"you have no ctqas go and cry about it {emoji('pointlaugh')}"
    embed = disnake.Embed(title=title, description=description)
    cats_counter = collector_counter = 0
    for ctqa in cat_types:
        if ctqa in cats_:
            embed.add_field(name=f"{ctqa_emoji(ctqa)} {ctqa}", value=repr_complex(cats_[ctqa]))
            cats_counter += cats_[ctqa]
            collector_counter += 1
    if custom:
        embed.add_field(name=f"{ctqa_emoji(custom)} {custom}", value=1)
    footer_dict = {"text": f"Total ctqas: {repr_complex(cats_counter)}"}
    embed.set_footer(**footer_dict)
    await ctx.send(embed=embed)
    if collector_counter == len(cat_types):
        await achembed(ctx, member, "collecter")


@bot.slash_command(name="lb", description="leaderboards")
async def leaderboards(ctx):
    await ctx.send(embed=get_lb(ctx, "Ctqas"), components=lb_components("Ctqas"))


@bot.slash_command(name="achs", description="view your achievements")
async def achievements(ctx):
    await ctx.send(
        embed=disnake.Embed(
            title="Your achievements:",
            description=get_achs_amount(ctx)
        ), components=[Button(label="View all achievements", style=blurple, custom_id=f"SENDACHS;{ctx.author.id}")]
    )


@bot.slash_command(name="force_spawn", description="Forces ctqa to spawn in channel")
async def force_spawn(ctx, ctqa_type):
    if ctqa_type not in cat_types:
        await ctx.send("this ctqa type doesn't exist")
    if "yes" == "yes":
        await ctx.send("dev mode and currency coming somewhen idk")
    else:
        await spawn_cat(ctx.channel)


@bot.slash_command(name="gift", description="give ctqas to someone")
async def gift(ctx, member: disnake.Member, ctqa_type: str, amount: int = 1):
    cats = get_user_cats(ctx.guild.id, ctx.author.id)["cats"]
    if member == ctx.author:
        await ctx.send("uhhhhh", ephemeral=True)
        return
    if ctqa_type not in cat_types:
        await ctx.send(f"ctqa type `{ctqa_type}` doesn't exist", ephemeral=True)
        return
    if ctqa_type not in cats:
        await ctx.send(f"you dont have ctqas of `{ctqa_type}` type", ephemeral=True)
        return
    user_cat = cats[ctqa_type]
    if amount > user_cat.real:
        await ctx.send(
            f"you dont have that many `{ctqa_type}` ctqas " +
            f"(you have {repr_complex(user_cat)} and wanted to donate {amount})",
            ephemeral=True)
        return
    if amount < 1:
        await ctx.send("nooouuuuu 😛😛😛😛", ephemeral=True)
        return
    give_cat(ctx.guild.id, ctx.author.id, ctqa_type, -amount)
    await achembed(ctx, ctx.author, "donator")
    give_cat(ctx.guild.id, member.id, ctqa_type, amount)
    await achembed(ctx, member, "antidonator")
    await ctx.send(f"{ctx.author.mention} gave {member.mention} {amount} {ctqa_type} ctqas!!!!!!!")


@bot.slash_command(description="yes")
async def gift_imag(ctx, member: disnake.Member, ctqa_type: str, amount: int):
    cats = get_user_cats(ctx.guild.id, ctx.author.id)["cats"]
    if member == ctx.author:
        await ctx.send("uhhhhh", ephemeral=True)
        return
    if ctqa_type not in cat_types:
        await ctx.send(f"ctqa type `{ctqa_type}` doesn't exist", ephemeral=True)
        return
    if ctqa_type not in cats:
        await ctx.send(f"you dont have ctqas of `{ctqa_type}` type", ephemeral=True)
        return
    user_cat = cats[ctqa_type]
    if amount > user_cat.imag:
        await ctx.send(
            f"you dont have that many `{ctqa_type}` imaginary ctqas "
            f"(you have {repr_complex(user_cat)} and wanted to donate {amount.imag}i)",
            ephemeral=True)
        return
    if amount < 1:
        await ctx.send("nooouuuuu 😛😛😛😛", ephemeral=True)
        return
    give_imag_cat(ctx.guild.id, ctx.author.id, ctqa_type, -amount)
    give_imag_cat(ctx.guild.id, member.id, ctqa_type, amount)
    await ctx.send(f"{ctx.author.mention} gave {member.mention} {amount}i {ctqa_type} ctqas!!!!!!!")


@bot.slash_command(name="ctqas", description="ctqas list")
async def ctqas(ctx):
    await ctx.send("ctqa chances:```{0}```custom ctqas:```{1}```".format(
        '\n'.join(f"{k:<15}{v / len(CAT_TYPES) * 100:.4f}%" for k, v in type_dict.items()), ', '.join(custom_types))
    )


@bot.command()
async def custom(ctx, user: disnake.User, *, cat_type: str):
    if ctx.author.id != 558979299177136164:
        await ctx.send(emoji("typing"))
        return
    if cat_type not in custom_types:
        await ctx.send(f"{cat_type} is not a custom cat type")
        return
    set_custom_cat(user.id, cat_type)
    await ctx.send("ok bro 👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍")


@bot.command()
async def whitelist(ctx, bot_id: int):
    filepath = temalib.get_file_path(__file__, "servers config", f"{ctx.guild.id}.antigrav", create_file="{}")
    config = json.load(open(filepath))
    if ctx.author.id not in [ctx.guild.owner_id, 558979299177136164]:
        await ctx.send(emoji("typing"))
        return
    if "whitelisted bots" not in config:
        config["whitelisted bots"] = []
    if bot_id not in config["whitelisted bots"]:
        config["whitelisted bots"].append(bot_id)
        await ctx.send(f"added id {bot_id} to bots whitelist")
    else:
        config["whitelisted bots"].remove(bot_id)
        await ctx.send(f"removed id {bot_id} from bots whitelist")
    json.dump(config, open(filepath, "w"))


class HTTPException(Exception):
    pass


@bot.slash_command(description="brew coffee")
async def brew(ctx):
    import http
    import traceback
    try:
        status = http.HTTPStatus.IM_A_TEAPOT
        wuggy_text = f"{status.value} {status.phrase}:\n{status.description}"
        raise HTTPException(wuggy_text)
    except HTTPException:
        await ctx.send(f"an error occured while running that command:\n```\n{traceback.format_exc()}\n```")
        await achembed(ctx, ctx.author, "418")


@bot.slash_command(description="HOLY CTQA")
async def holy(ctx):
    await ctx.send(file=disnake.File("holy_ctqa.jpg"))
    await achembed(ctx, ctx.author, "holyctqa")


# noinspection LongLine
@bot.slash_command(name="info", description="info about bot (do you really need explaination)")
async def info(ctx):
    slinx92 = bot.get_user(986132157967761408)
    description = f"""
[supportn't server](https://discord.gg/QnXad4qY4U) | [Slinx's Attic](https://discord.gg/DrwjattCUH) | [source code](https://github.com/tema5002/ctqa-bto)

i jave no clue what do i say here gdsuaghggfgsigf
run /setup to spawn cats in channel
if they randomly stopped spawning then blame discord, try running /setup again

thanks to:
- **{slinx92}** for syating ctqa image and making ctqa icons
    """
    await ctx.send(embed=disnake.Embed(title="ctqa bto (cat bot clone)", description=description))


bot.load_extension("cogs.ping")

bot.run(open("TOKEN.txt").read())
