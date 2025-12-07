"""
announcements package reads announcements
from the file.
"""

import dataclasses
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import collections.abc


@dataclasses.dataclass()
class Announcement:
    """
    Announcement show an announcement on the status page.
    """

    type: str
    status: bool
    message: str


if not (__announcements := list[Announcement]()):
    with Path("announcements/announcements.json").open(encoding="utf-8") as fp:
        for announcement in json.load(fp):
            __announcements.append(
                Announcement(
                    type=announcement["type"],
                    status=announcement["status"],
                    message=announcement["message"],
                )
            )


def announcements() -> collections.abc.Iterator[Announcement]:
    """
    list returns an iterator for all the announcements
    """
    return iter(__announcements)
