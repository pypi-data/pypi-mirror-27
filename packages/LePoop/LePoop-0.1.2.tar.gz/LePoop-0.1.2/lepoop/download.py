"""Utilities for reversing download."""

from .utils import get_valid_pip_history
from .utils import get_pip_command_action
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def get_file_candidates(prefix='File was already downloaded'):
    """Find all files likely to be related to the latest packages."""
    pip_download_history = [command for command in get_valid_pip_history()
                            if get_pip_command_action(command) == 'download']
    assert pip_download_history, 'Already pooped'
    event = Popen(pip_download_history[0].split(), stdin=PIPE,
                  stdout=PIPE, stderr=STDOUT)
    output, error = event.communicate()

    # Search output for files
    candidates = []
    for line in output.decode('utf-8').splitlines():
        if line.strip().startswith(prefix):
            filename = line.replace(prefix, '').strip()
            candidates.append(filename)
    return ' '.join(candidates)
