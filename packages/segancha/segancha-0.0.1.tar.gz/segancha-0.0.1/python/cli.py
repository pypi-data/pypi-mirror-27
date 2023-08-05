from argparse import ArgumentParser, RawDescriptionHelpFormatter
from getpass import getuser
from textwrap import dedent
from .profile import parse
from .theme import update_context
from .version import __version__


def argparser():
    ps = ArgumentParser(
        prog='segancha',
        description=dedent("""
            Generate optimized discernible color palette and themes settings

            Example:
              segancha --temperature -1 --profile demo
              segancha --background 97 --profile vscode
            """),
        formatter_class=RawDescriptionHelpFormatter)

    ps.add_argument(
        '-n',
        '--name',
        default='default',
        type=str,
        help='theme name, default: \'default\'')
    ps.add_argument(
        '-f',
        '--foreground',
        '--Lf',
        default=-1,
        dest='Lf',
        metavar='Lf',
        type=float,
        help='foreground luminosity between 0 < Lf < 100')
    ps.add_argument(
        '-b',
        '--background',
        '--Lb',
        default=-1,
        dest='Lb',
        metavar='Lb',
        type=float,
        help='background luminosity 0 < Lb < 100')
    ps.add_argument(
        '-L',
        '--palette-luminosity',
        '--L3',
        default=-1,
        dest='L3',
        metavar='L3',
        type=float,
        help='main palette luminosity 0 < L3 < 100')
    ps.add_argument(
        '--maxC',
        default=-1,
        metavar='maxC',
        type=float,
        help='maximal chroma > 0')
    ps.add_argument(
        '-T',
        '--temperature',
        default=5000,
        dest='T',
        metavar='T',
        type=float,
        help='temperature 4000 < T < 25000')
    ps.add_argument(
        '-p',
        '--profile',
        action='append',
        default=[],
        dest='profiles',
        metavar='PROFILE',
        help='profiles to be parsed')
    ps.add_argument(
        '--L2',
        default=-1,
        dest='L2',
        metavar='L2',
        type=float,
        help='(advanced) 0 < L2 < 100')
    ps.add_argument(
        '--L1',
        default=-1,
        dest='L1',
        metavar='L1',
        type=float,
        help='(advanced) 0 < L1 < 100')
    ps.add_argument(
        '--L0',
        default=-1,
        dest='L0',
        metavar='L0',
        type=float,
        help='(advanced) 0 < L0 < 100')
    ps.add_argument('-v', '--verbose', action='store_true', default=False)

    return ps


def main():
    args = argparser().parse_args()
    ctx = {
        'name': args.name,
        'version': __version__,
        'user': getuser(),
    }

    update_context(args, ctx)
    parse(args, ctx)
