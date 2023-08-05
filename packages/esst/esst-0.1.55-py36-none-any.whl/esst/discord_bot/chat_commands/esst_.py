# coding=utf-8
"""
Manages commands related to ESST itself
"""

from esst.core import CFG, __version__
from esst.core.logger import get_esst_log_file_path
from esst.discord_bot.commands import DISCORD
from esst.utils import get_esst_changelog_path

from .arg import arg


def log():
    """
    Show ESST log file
    """
    DISCORD.send(get_esst_log_file_path(CFG.saved_games_dir))


def changelog():
    """
    Show ESST changelog file
    """
    changelog_path = get_esst_changelog_path()
    if changelog_path:
        DISCORD.send(changelog_path)


def version():
    """
    Show ESST version
    """
    DISCORD.say(f'ESST v{__version__}')


@arg(protected=True)
def restart():
    """
    Restart ESST (protected)

    """
    DISCORD.say('This command is not yet implemented')


NAMESPACE = '!esst'
TITLE = 'Manage ESST application'
