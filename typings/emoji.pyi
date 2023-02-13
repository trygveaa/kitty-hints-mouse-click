from typing import TypedDict

class EmojiMatch(TypedDict):
    match_start: int
    match_end: int
    emoji: str

def emoji_list(string: str) -> list[EmojiMatch]: ...
