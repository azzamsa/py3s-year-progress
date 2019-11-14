# Year Progress in Py3status

## Docs

```
Year progress.

Configuration parameters:
    progress_block: block type to show progress (default '▓')
    remain_block: block type to show remaining progress (default '░')
    progress_width: progress bar width (default 10)

Format placeholders:
    {progress_bar} Progress bar
    {ratio} Progress ratio

```

## Examples configuration

``` yaml
year_progress {
    format = "{progress_bar} {ratio}%"
    progress_block = '▓'
    remain_block = '░'
    progress_width = 10
}
```

## Sample Output
{'full_text': '▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 86%'}

## Credit:

Inspired by twitter.com/year_progress <https://github.com/filiph/progress_bar>
