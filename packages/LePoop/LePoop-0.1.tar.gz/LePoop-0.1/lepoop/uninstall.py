"""Reinstallation utilities for accidental `pip uninstall`s."""

from .utils import get_valid_pip_history
from .utils import get_pip_command_action
from .utils import get_pip_command_packages


def get_reinstall_candidates():
    """Get candidates for reinstallation.

    Really, these aren't just candidates. There sure as h*ll the right ones.
    """
    pip_uninstall_history = [command for command in get_valid_pip_history()
                             if get_pip_command_action(command) == 'uninstall']
    assert pip_uninstall_history, 'Already pooped'
    return ' '.join(get_pip_command_packages(pip_uninstall_history[0]))
