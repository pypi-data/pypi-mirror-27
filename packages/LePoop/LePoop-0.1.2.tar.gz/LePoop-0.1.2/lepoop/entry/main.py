"""Entry points manager for command line utility."""

from ..install import get_uninstall_candidates
from ..install import get_uninstall_dependencies_for
from ..install import get_installed_package_keys
from ..uninstall import get_reinstall_candidates
from ..download import get_file_candidates
from ..utils import colored
from ..utils import get_valid_pip_history
from ..utils import get_pip_command_packages
from .alias import poop_alias
from colorama import Fore
from subprocess import Popen
import argparse


def main():
    args = argparse.ArgumentParser('poop')
    args.add_argument('-a', '--alias', action='store_true',
                      help='Alias to `poop`')
    args.add_argument('--harder', action='store_true',
                      help='Look through bash history as far as possible.')
    args.add_argument('--stronger', action='store_true',
                      help='Look through bash history and module source files.'
                           ' for modules to uninstall.')
    args.add_argument('--skip', type=int, default=0,
                      help='Number of pip commands to skip.')
    args.add_argument('package', nargs='*', help='packages to uninstall')
    args = args.parse_args()

    if args.alias:
        print(poop_alias)
        return

    try:
        if args.package:
            command = create_command_using_packages(args.package)
        elif args.harder:
            command = create_command_using_pip_action('*', skip=args.skip)
        elif args.stronger:
            command = create_command_using_pip_action(
                '*', uninstall_use_creation_time=True, skip=args.skip)
        else:
            command = create_command_using_pip_action(skip=args.skip)
        input(colored('`{}` [enter/ctrl+c]'.format(command)))
        event = Popen(command.split())
        _, error = event.communicate()
    except AssertionError as e:
        print(Fore.RED + 'Already pooped. (%s)' % str(e))
    except KeyboardInterrupt:
        print()


def create_command_using_pip_action(
        num_bash_entries=10, uninstall_use_creation_time=False, skip=0):
    """Create commands using latest pip action."""
    valid_pip_commands = get_valid_pip_history(num_bash_entries)[skip:]
    assert valid_pip_commands, 'No undoable pip commands.'
    last_valid_pip_command = valid_pip_commands[0]
    last_valid_pip_action = last_valid_pip_command.split()[1]
    command = ''
    if uninstall_use_creation_time:
        command = 'pip uninstall -y {}'.format(get_uninstall_candidates())
    elif last_valid_pip_action == 'install':
        command = create_command_using_packages(get_pip_command_packages(
                last_valid_pip_command))
    elif last_valid_pip_action == 'uninstall':
        command = 'pip install {}'.format(get_reinstall_candidates())
    elif last_valid_pip_action == 'download':
        command = 'rm {}'.format(get_file_candidates())
    assert command, 'No undoable pip commands.'
    return command


def create_command_using_packages(packages):
    """Create comands using a list of packages."""
    all_packages = set(get_installed_package_keys())
    not_installed = [p for p in packages if p not in all_packages]
    installed = [p for p in packages if p in all_packages]
    assert installed, ('None of these packages are installed: %s' %
                       ', '.join(not_installed))
    packages = get_uninstall_dependencies_for(installed)
    if not_installed:
        print(colored('Packages `%s` are not installed. I\'m ignoring '
                      'them.' % ', '.join(not_installed)))
    return 'pip uninstall -y {}'.format(packages)