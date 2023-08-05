"""Quote for stormbot"""
import sys
import random
import argparse

from stormbot.bot import Plugin
from stormbot.storage import Storage

class Quote(Plugin):
    def __init__(self, bot, args):
        self._bot = bot
        self._cache = Storage(args.quote_cache)
        if "quotes" not in self._cache:
            self._cache["quotes"] = {}
        self.quotes = self._cache["quotes"]

    @classmethod
    def argparser(cls, parser):
        parser.add_argument("--quote-cache", type=str, default="/var/cache/stormbot/quote.p", help="Cache file (default: %(default)s)")

    def cmdparser(self, parser):
        subparser = parser.add_parser('quote', bot=self._bot)
        subparser.add_argument("author", help="Quote author")
        subparser.add_argument("quote", nargs='?', help="Quote")
        subparser.set_defaults(command=self.run)

    def run(self, msg, parser, args):
        if args.quote is None:
            self._bot.write(random.choice(self.quotes[args.author]))
        else:
            if args.author not in self.quotes:
                self.quotes[args.author] = []
            self.quotes[args.author].append(args.quote)
            self._bot.write("Your words are now engraved in the stones")
