import disnake
from disnake.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="shows ping")
    async def ping(self, ctx):
        await ctx.response.defer()
        h = round(self.bot.latency * 1000)
        if   h>=10000: message = f"ctqa  iahbr an d<:syating_ctqa:1178288745435385896>lsy o{h} fmsae"
        elif h>=8000:  message = f"ci a<:syating_ctqa:1178288745435385896>has bratqmdelay o n{h}  sf"
        elif h>=5000:  message = f"cn a <:syating_ctqa:1178288745435385896>at br isadel yaofq{h}ms h"
        elif h>=3000:  message = f"htqa cysrb fan delai oa {h}ms <:syating_ctqa:1178288745435385896>"
        elif h>=2000:  message = f"cdqa{h}hastbrain  e  ylof  msa<:syating_ctqa:1178288745435385896>"
        elif h>=1500:  message = f"ct a<:syating_ctqa:1178288745435385896>ahsqbrain delay of {h} s m"
        elif h>=1000:  message = f"ctsbohas arain delay  f {h}mq <:syating_ctqa:1178288745435385896>"
        elif h>=500:   message = f"ctqa<:syating_ctqa:1178288745435385896>has brain delay of {h}ms"
        elif h>=300:   message = f"ctqa hasnbrai  delay of {h}ms <:syating_ctqa:1178288745435385896>"
        else:          message = f"ctqa has bran delayt of {h}ms <:syating_ctqa:1178288745435385896>"

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Ping(bot))
