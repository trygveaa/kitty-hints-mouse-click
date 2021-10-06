import re
from functools import partial
from kittens.hints.main import functions_for, regex_finditer
from kitty.fast_data_types import (
    wcswidth,
    send_mouse_event,
    PRESS,
    RELEASE,
)

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


def mark(text, args, Mark, extra_cli_args, *a):
    if extra_cli_args and extra_cli_args[0] not in button_map:
        print(f"The key `{extra_cli_args[0]}` is unknown.")
        print(f"You must specify one of: {', '.join(button_map.keys())}")
        return
    if args.type == "emoji" or args.type == "emoji_char_and_name":
        import emoji

        if args.type == "emoji":
            regex = emoji.get_emoji_regexp()
        else:
            emoji_name_pattern = r"(:[a-z0-9_+-]+:)"
            regex = re.compile(
                r"(?P<all>{}|{})".format(emoji.get_emoji_regexp().pattern, emoji_name_pattern)
            )
        args.minimum_match_length = 1
    else:
        pattern, _ = functions_for(args)
        regex = re.compile(pattern)
    for idx, (s, e, _) in enumerate(
        regex_finditer(regex, args.minimum_match_length, text)
    ):
        lines = text[:s].split("\n")
        y = len(lines) - 1
        x = wcswidth(lines[-1])
        mark_text = text[s:e].replace("\n", "").replace("\0", "")
        yield Mark(idx, s, e, mark_text, {"x": x, "y": y})


def handle_result(args, data, target_window_id, boss, extra_cli_args, *a):
    w = boss.window_id_map.get(target_window_id)
    button_name = extra_cli_args[0] if extra_cli_args else "left"
    for coords in data["groupdicts"]:
        send = partial(
            send_mouse_event,
            w.screen,
            coords["x"],
            coords["y"],
            button_map[button_name],
        )
        send(PRESS, 0)
        send(RELEASE, 0)
