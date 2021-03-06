"""Play music from stormbot"""
import os
import subprocess
from .bot import Plugin


class Music(Plugin):
    def __init__(self, args):
        self.player = args.music_player
        self.path = os.path.abspath(args.music_path)
        self.default = args.music_default

    @classmethod
    def argparse(cls, parser):
        parser.add_argument("--music-player", type=str, default="paplay", help="Music player (default: %(default)s)")
        parser.add_argument("--music-path", type=str, default=os.getcwd(), help="Music player (default: %(default)s)")
        parser.add_argument("--music-default", type=str, default=None, help="Music player (default: %(default)s)")

    def safe_path(self, path):
        path = os.path.join(self.path, path)
        path = os.path.abspath(path)
        common_prefix = os.path.commonpath([path, self.path])
        return common_prefix == self.path

    def parser(self, parser):
        subparser = parser.add_parser('music')
        subparser.set_defaults(command=self.run)
        subparser.add_argument("--volume", type=int, default=65536, help="Music player volume (default: %(default)i)")
        subparser.add_argument("music", type=str, nargs='?', default=self.default,
                               help="Music to play (default: %(default)s)")

    def run(self, bot, msg, parser, args):
        if not self.safe_path(args.music):
            bot.send_message(mto=msg['from'].bare, mbody="Don't try to mess with me !", mtype='groupchat')
            return

        bot.send_message(mto=msg['from'].bare, mbody="playing your favorite song out loud !", mtype='groupchat')
        music = os.path.join(self.path, args.music)
        cmd = [self.player, music]
        subprocess.Popen(cmd, stdin=None, stdout=None, stderr=None, close_fds=True)
