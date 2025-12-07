"""
announcements package reads announcements
from the file.
"""

import collections.abc
import dataclasses
import json


@dataclasses.dataclass()
class Announcement:
    """
    Announcement show an announcement on the status page.
    """

    type: str
    status: bool
    message: str


if not (__announcements := list[Announcement]()):
    with open("announcements/announcements.json", encoding="utf-8") as fp:
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
