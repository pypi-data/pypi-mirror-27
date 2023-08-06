from colorama import init
from colorama import Style
from colorama import Fore
import os
import datetime
import pip
import platform
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from collections import defaultdict
from itertools import chain
import glob


init()
__all__ = ('get_package_groups', 'get_valid_pip_history', 'colored')


flatten = chain.from_iterable


def colored(string):
    """Print, coloring all code delimited with backticks."""
    count = string.count('`') // 2
    args = [Fore.GREEN + Style.BRIGHT, Style.RESET_ALL] * count
    return string.replace('`', '{}').format(*args)


def get_package_groups():
    """Get groups of packages installed at the same time.

    The list is ordered in reverse order, across time as (time, packages). Here,
    time is formatted as datetime objects.
    """
    mapping = defaultdict(lambda: [])
    for package_name_version, creation_time in get_packages_creation_times():
        mapping[creation_time].append(package_name_version)

    result = []
    for creation_time in sorted(mapping, reverse=True):
        pretty_mod_time = datetime.datetime.fromtimestamp(creation_time)
        result.append((pretty_mod_time, mapping[creation_time]))
    return result


def get_valid_pip_history():
    """Looks only at valid pip commands logged in history.

    See `is_valid_command` for details on `valid` commands.
    """
    commands = get_pip_history()
    for command in commands:
        if is_invalid_command(command):
            commands.remove(command)
    return commands


def is_invalid_command(command):
    """Check if the given command is valid.

    Details on what constitutes a `valid` command:
    - install: If none of the packages are still installed, ignore it
    - uninstall: If all of the packages are installed, ignore it
    - download: If no tars or wheels are found in the current directory,
                related to the specified packages, ignore it

    Any other pip command is unsupported, as it does not make sense to undo
    those functions.
    """
    all_packages = set(get_pip_package_key(package) for package
                       in pip.get_installed_distributions())
    action = get_pip_command_action(command)
    packages = get_pip_command_packages(command)
    packages = set([p.split('==')[0] for p in packages])
    return (action == 'install' and not all_packages & packages) or \
        (action == 'uninstall' and not packages - all_packages) or \
        (action == 'download' and not any(
            [get_associated_file(package) for package in packages])) or \
        (action not in ('install', 'uninstall', 'download'))


def get_associated_file(package_key):
    """Find file associated with the package key."""
    package_key = package_key.replace('-', '_')
    for path in flatten([glob.iglob('*.whl'), glob.iglob('*.tar.gz')]):
        if path.startswith(package_key):  # TODO: more specific format check
            return path


def get_pip_package_key(candidate):
    """Get package key for the provided string.

    The string may be a name and version.
    """
    return str(candidate).split()[0].split('==')[0]


def get_pip_command_action(command):
    """Return pip action for a pip command."""
    return command.split()[1]


def get_pip_command_packages(command):
    """Return packages included in a pip command."""
    return command.split()[2:]


def get_pip_history():
    """Get all pip commands logged in history."""
    commands = []
    for line in get_bash_history():
        for command in line.split(';'):
            if command.strip().startswith('pip'):
                commands.append(command)
    return commands


def get_bash_history():
    """Get bash history.

    Items are sorted in reverse order, starting with the most recent.
    """
    shell_command = 'bash -i -c "history -r; history"'
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    output, error = event.communicate()
    output = output.decode('utf-8').replace("'\n", '\n')  # clean up weirdness
    commands = [' '.join(str(line).split()[1:]) for line in output.splitlines()]
    return commands[::-1]


def get_packages_creation_times():
    """Get all pip packages and their timestamps.

    Original function taken from StackOverflow:
    https://stackoverflow.com/a/44436961/4855984
    """
    packages = []
    for package in pip.get_installed_distributions():
        package_name_version = str(package)
        package_location = get_package_location(package)
        creation_time = get_creation_date(package_location)
        packages.append([
            package_name_version,
            creation_time,
        ])
    return packages


def get_package_location(package):
    """Get module directory from the module information.

    Original function taken from StackOverflow:
    https://stackoverflow.com/a/44436961/4855984
    """
    try:
        module_dir = next(package._get_metadata('top_level.txt'))
        package_location = os.path.join(package.location, module_dir)
        os.stat(package_location)
        return package_location
    except (StopIteration, OSError):
        pass
    package_location = os.path.join(package.location, package.key)
    if os.path.isdir(package_location):
        return package_location
    return package.location


def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
