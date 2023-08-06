import argparse, traceback
import pretty_output

from kooki.exception import KookiException

class Command:

    def __init__(self, command, description):
        self.command = command

        self.parser = argparse.ArgumentParser(prog=self.command, description=description, add_help=False)
        self.parser.set_defaults(callback=self)

        self.parser.add_argument('-d', '--debug', help='Show information to help debug the bake processing', action='store_true')
        self.parser.add_argument('--no-color', help='The output has no color.', action='store_true')
        self.parser.add_argument('--no-output', help='There is no output.', action='store_true')
        self.subparsers = None

    def add_command(self, command, description='', help=''):
        if self.subparsers == None:
            self.subparsers = self.parser.add_subparsers(help=help)
        subparser = self.subparsers.add_parser(command.parser.prog, help=command.parser.description)
        subparser.__dict__ = command.parser.__dict__;

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def run(self):
        args = self.parser.parse_args()
        args.callback(args)

    def __call__(self, args):
        try:
            pretty_output.set_output_policy(not args.no_output)
            pretty_output.set_color_policy(not args.no_color)
            pretty_output.set_debug_policy(args.debug)
            pretty_output.command(self.command)
            self.callback(args)

        except KookiException as e:
            pretty_output.error_step('Errors')
            pretty_output.error(e)

        except Exception as e:
            pretty_output.error_step('Errors')
            pretty_output.error(traceback.format_exc()[:-1])

        finally:
            pretty_output.command()
