"""Runs when the `poop` alias has not been setup."""

from colorama import init
from ..utils import colored
from .alias import is_configured
from .alias import configure
init()


def main():

    if not is_configured():
        configure()

    print(colored('The `poop` alias was configured successfully.\n'
          'Run `source ~/.bashrc` or restart your shell.'))
