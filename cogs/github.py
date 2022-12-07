from collections import OrderedDict
import logging
from discord.ext import commands
import helpers

_log = logging.getLogger(__name__)

class Github(commands.Cog, name="Github"):
    def __init__(self, bot, token):
        _log.info("Commands created")
        self.bot = bot
        self.token = token
 
    @commands.command(help="Toont aantal commits per persoon")
    async def commits(self, ctx):
        all_repos = helpers.get_repos(self.token)
        res = helpers.get_commits_per_member(all_repos, self.token)
        top_res = OrderedDict(sorted(res.items(), key = lambda x:x[1]))
        string = "🏆   TOP COMMITS ALL-TIME   🏆\n"
        for i, (p, comm) in enumerate(top_res.items()):
            string += "\n{}.\t_{}_ met **{}** commits".format(i+1, p, comm)
        await ctx.send(string)
