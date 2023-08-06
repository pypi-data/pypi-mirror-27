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
        subparser.add_argument("--all", action="store_true", help="Show all quotes")
        subparser.add_argument("author", nargs='?', help="Quote author")
        subparser.add_argument("quote", nargs='?', help="Quote")
        subparser.set_defaults(command=self.run)

    def store(self, author, quote):
        if author not in self.quotes:
            self.quotes[author] = []
        self.quotes[author].append(quote)
        self._bot.write("Your words are now engraved in the stones")

    def get(self, args):
        if len(self.quotes) == 0:
            self._bot.write("We don't have any quote yet, feel free to add some.")
            return

        if args.all:
            self.get_all(args)
        else:
            self.get_one(args)

    def get_one(self, args):
        author = args.author if args.author is not None else random.choice(list(self.quotes.keys()))
        if author not in self.quotes or len(self.quotes[author]) < 1:
            self._bot.write("We don't have any quote for %s yet, feel free to add some." % author)
        else:
            self._bot.write("{} \"{}\"".format(author, random.choice(self.quotes[author])))

    def get_all(self, args):
        authors = [args.author] if args.author is not None else list(self.quotes.keys())
        for author in authors:
            for quote in self.quotes[author]:
                self._bot.write("{} \"{}\"".format(author, quote))

    def run(self, msg, parser, args):
        if args.quote is None:
            self.get(args)
        else:
            self.store(args.author, args.quote)

if __name__ == "__main__":
    from stormbot.bot import main
    main(Quote)
