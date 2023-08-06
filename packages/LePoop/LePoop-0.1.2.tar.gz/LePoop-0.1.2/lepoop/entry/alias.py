"""Configuration for Le Poop.

Includes alias for `poop` command hack.
"""

import os

bashrc_path = os.path.join(os.path.expanduser('~'), '.bashrc')

bashrc_content = """
# added by lepoop
eval $(lepoop --alias)
"""

poop_alias = """
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND";

function poop() {
    lepoop $@;
}
"""


def is_configured():
    with open(bashrc_path) as f:
        return bashrc_content in f.read()


def configure():
    with open(bashrc_path, 'a') as f:
        f.write(bashrc_content)
