# Kitty hints processor for mouse clicking

This is a [custom
processor](https://sw.kovidgoyal.net/kitty/kittens/hints.html#completely-customizing-the-matching-and-actions-of-the-kitten)
for the [hints kitten](https://sw.kovidgoyal.net/kitty/kittens/hints.html) in
the [kitty terminal emulator](https://sw.kovidgoyal.net/kitty/) which allows
you to send mouse click events to the program running in the terminal emulator.

## Installation

Place the `hints_mouse_click.py` file in the same directory as `kitty.conf`.

If you want to match against emojis, you have to install the
[emoji](https://pypi.org/project/emoji/) package.

Map a key to launch the hints kitten with this processor. E.g. for using
`kitty_mod+y` to right click on emojis add this to `kitty.conf`:

```
map kitty_mod+y kitten hints --type emoji --customize-processing hints_mouse_click.py right
```

## Usage

This is used just like the standard hints kitten, except for these differences:

- You can specify the mouse button you want to use as the last argument. This
  can be `left`, `middle`, `right`, `scroll_up`, `scroll_down`, `scroll_left`,
  `scroll_right`, `back` or `forward`. Defaults to `left` if not specified.
- The `--type` option supports `emoji` and `emoji_char_and_name` in addition to
  the standard types. `emoji` will match emoji characters.
  `emoji_char_and_name` will in addition match the regex `:[a-z0-9_+-]+:` which
  is typically how emojis are represented by name in ascii. These two types
  force `--minimum-match-length` to `1` to be able to match emojis.
