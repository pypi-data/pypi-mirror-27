"""Uninstallation utilities for accidental `pip install`s"""

from .utils import get_valid_pip_history
from .utils import get_package_groups
from .utils import get_pip_command_action
from .utils import get_pip_command_packages
from .utils import get_pip_package_key
from .utils import flatten
from pipdeptree import build_dist_index
from pipdeptree import construct_tree
from pipdeptree import reverse_tree
from pipdeptree import find_tree_root
import pip


def get_installed_package_keys():
    """Get all installed package keys."""
    return [get_pip_package_key(package) for package in
            pip.get_installed_distributions()]


def get_most_recent_packages_by_creation_time():
    """Get most recent packages as determined by module source create time."""
    package_groups = get_package_groups()
    if not package_groups:
        return set()
    time, packages = package_groups[0]
    packages = [pkg.split()[0] for pkg in packages]
    return set(packages)


def get_most_recent_packages_by_pip_history():
    """Get most recent packages as determined by pip history."""
    pip_install_history = [command for command in get_valid_pip_history()
                           if get_pip_command_action(command) == 'install']
    if not pip_install_history:
        return set()
    packages = [package.split('==')[0] for package in
                get_pip_command_packages(pip_install_history[0])]
    return set(packages)


def get_uninstall_dependencies_for(package_keys):
    """Find candidates for installation given package keys.

    1. Find all dependencies for these packages.
    2. Determine which dependencies:
       a. are not needed by any other package and
       b. have a "recent" creation date.
    """
    # 1. Find all dependencies of these packages.
    all_packages = pip.get_installed_distributions()
    dist_index = build_dist_index(all_packages)
    packages = set(dist_index[package_key] for package_key in package_keys)
    dependencies = flatten([package.requires() for package in packages])

    # 2. Determine unneeded dependencies that were installed at roughly the
    #    same time. # TODO: check time of installation
    candidates = set(package_keys)
    rtree = reverse_tree(construct_tree(dist_index))
    for dep in dependencies:
        node = find_tree_root(rtree, dep.key)
        leftover = {d.key for d in rtree[node] if d.key not in package_keys}
        if not leftover:
            candidates.add(dep.key)
    return ' '.join(candidates)


def get_uninstall_candidates():
    """Find candidates for uninstallation.

    1. Find recent modules by creation time and history. Merge the two.
    2. Find all relevant dependencies for uninstallation.
    """
    # 1. Find packages that were recently installed.
    packages_by_module = get_most_recent_packages_by_creation_time()
    packages_by_history = get_most_recent_packages_by_pip_history()
    package_keys = packages_by_module.union(packages_by_history)
    all_packages = set(get_installed_package_keys())
    package_keys = [p for p in package_keys if p in all_packages]
    assert package_keys, 'Possible uninstall candidates have' \
                         ' already been uninstalled.'

    # 2. Determine relevant dependencies.
    return get_uninstall_dependencies_for(package_keys)