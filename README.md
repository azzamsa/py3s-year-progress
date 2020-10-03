> 📢 **PSA**: A successor was born: [Zman](https://sr.ht/~azzamsa/Zman/)

# Year Progress in Py3status

Show year progress in your py3status

## Feature

- Show year progress
- Show month, week, day progress (toggled with mouse click)
- Custom end date (still in alpha)

## Installation

Put this file in one of [py3status custom module location][1] such as
`~/.config/i3status/py3status`, then add proper configuration in your i3status
config.

## Docs

See the docs string

## Examples configuration

``` yaml
year_progress {
    format = "{progress_bar} {ratio}%{mode}"
    progress_block = '▓'
    remain_block = '░'
    progress_width = 10
}
```

## Sample Output

{'full_text': '▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 86%'y}

![image](https://user-images.githubusercontent.com/17734314/68861839-e6c05880-071e-11ea-91b3-5373484e51f7.png)

## Credit:

Part of the code are ported from twitter.com/year_progress <https://github.com/filiph/progress_bar>

[1]: https://py3status.readthedocs.io/en/latest/writing_modules.html#importing-custom-modules
