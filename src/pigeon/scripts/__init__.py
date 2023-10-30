import argparse
import pigeon.scripts.commands as commands


def execute(args=None):
    parser = argparse.ArgumentParser(prog='pigeon')
    parser.add_argument(
        '-create',
                        dest='create',
                        action='store',
                        default='app',
                        nargs=1,
                        type=str,
                        help='create a new webapp and optionally provide a name'
    )
    
    args = parser.parse_args()
    
    if args.create:
        commands.create(args.create[0])