from typing import TYPE_CHECKING

from phoenix_framework.server.database import ListenerModel
from phoenix_framework.server.utils.options import (DefaultListenerPool,
                                                    Option, StringType)

from ..base_listener import BaseListener

if TYPE_CHECKING:
    from phoenix_framework.server.commander import Commander


class Listener(BaseListener):
    """The Example Listener Class"""

    name = "example"
    description = "Example Listener"
    author: str = "Example"
    os = ["linux", "windows", "osx"]
    options = DefaultListenerPool(
        [
            Option(
                name="Example Option",
                description="Example Option Description",
                type=StringType(),
                default="Example Default Value",
                required=True,
            )
        ]
    )

    def __init__(self, commander: "Commander", db_entry: ListenerModel):
        super().__init__(commander, db_entry)

    def start(self):
        print("Starting listener")

    def stop(self):
        print("Stopping listener")

    def status(self) -> bool:
        print("Checking status")