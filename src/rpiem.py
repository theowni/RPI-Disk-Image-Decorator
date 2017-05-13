import sys
import argparse

from lib.program_control import ProgramControl
from lib.emulate_manager import MNT_PATH


program = ProgramControl()
parser = argparse.ArgumentParser(
    description='Setup raspbian image in chroot qemu-emulated environment'
)
subparsers = parser.add_subparsers()

# Mount command specified:
parser_mnt = subparsers.add_parser(
    'mount',
    help='mount specified image in chroot'
)
required_mnt = parser_mnt.add_argument_group('required arguments')
required_mnt.add_argument(
    '-p', '--path', action='store', required=True,
    help='path to image file'
)
parser_mnt.add_argument(
    '-m', '--mnt', action='store',
    help='path to mounting point, default={}'.format(MNT_PATH)
)
parser_mnt.set_defaults(func=program.mount)

# Umount command specified:
parser_umnt = subparsers.add_parser(
    'umount',
    help='umount image and clean os'
)
parser_umnt.add_argument(
    '-p', '--path', action='store',
    help='path to image file'
)
parser_umnt.add_argument(
    '-m', '--mnt', action='store',
    help='path to mounting point, default={}'.format(MNT_PATH)
)
parser_umnt.set_defaults(func=program.umount)

# Shell command specified:
parser_shell = subparsers.add_parser(
    'shell',
    help='spawn shell in chroot environment'
)
parser_shell.add_argument(
    '-p', '--path', action='store',
    help='path to image file'
)
parser_shell.add_argument(
    '-m', '--mnt', action='store',
    help='path to mounting point, default={}'.format(MNT_PATH)
)
parser_shell.set_defaults(func=program.spawn_shell)

parser_playbook = subparsers.add_parser(
    'run_playbook',
    help='run playbook on emulated machine'
)
parser_playbook.add_argument(
    '-p', '--path', action='store',
    help='path to image file'
)
parser_playbook.add_argument(
    '-m', '--mnt', action='store',
    help='path to mounting point, default={}'.format(MNT_PATH)
)
parser_playbook.add_argument(
    '-f', '--playbook_path', action='store', required=True,
    help='path to playbook file'
)
parser_playbook.set_defaults(func=program.run_playbook)

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
program.run(args)
