import re
from functools import partial
from typing import Any, Generator, Sequence, Type

from kittens.hints.main import Mark, functions_for, regex_finditer
from kitty.boss import Boss
from kitty.fast_data_types import PRESS, RELEASE, send_mouse_event, wcswidth

button_map = {
    "left": 1,
    "middle": 2,
    "right": 3,
    "scroll_up": 4,
    "scroll_down": 5,
    "scroll_left": 6,
    "scroll_right": 7,
    "back": 8,
    "forward": 9,
}


def get_matches(text: str, args: Any):
    if args.type == "emoji" or args.type == "emoji_char_and_name":
        import emoji

        for m in emoji.emoji_list(text):
            yield m["match_start"], m["match_end"]

    if args.type != "emoji":
        if args.type == "emoji_char_and_name":
            pattern = r":[a-z0-9_+-]+:"
        else:
            pattern, _ = functions_for(args)
        regex = re.compile(pattern)
        for s, e, _ in regex_finditer(regex, args.minimum_match_length, text):
            yield s, e


def mark(
    text: str, args: Any, Mark: Type[Mark], extra_cli_args: Sequence[str]
) -> Generator[Mark, None, None]:
    if extra_cli_args and extra_cli_args[0] not in button_map:
        print(f"The key `{extra_cli_args[0]}` is unknown.")
        print(f"You must specify one of: {', '.join(button_map.keys())}")
        return

    matches = sorted(get_matches(text, args))
    for idx, (s, e) in enumerate(matches):
        lines = text[:s].split("\n")
        y = len(lines) - 1
        x = wcswidth(lines[-1])
        mark_text = text[s:e].replace("\n", "").replace("\0", "")
        yield Mark(idx, s, e, mark_text, {"x": x, "y": y})


def handle_result(
    args: list[str],
    answer: dict[str, Any],
    target_window_id: int,
    boss: Boss,
    extra_cli_args: list[str],
) -> None:
    w = boss.window_id_map.get(target_window_id)
    if w:
        button_name = extra_cli_args[0] if extra_cli_args else "left"
        for coords in answer["groupdicts"]:
            send = partial(
                send_mouse_event,
                w.screen,
                coords["x"],
                coords["y"],
                button_map[button_name],
            )
            send(PRESS, 0)
            send(RELEASE, 0)
