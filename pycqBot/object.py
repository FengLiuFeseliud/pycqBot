from __future__ import annotations
from typing import Any, TYPE_CHECKING


from pycqBot.cqEvent import Event

if TYPE_CHECKING:
    from pycqBot import cqBot, cqHttpApi


class Plugin(Event):

    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config: dict[str, Any]) -> None:
        self.bot = bot
        self.cqapi = cqapi
        self.plugin_config = plugin_config