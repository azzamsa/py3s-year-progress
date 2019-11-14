# Year Progress in Py3status

Show year progress in your py3status

## Docs

See the docs string

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

![image](https://user-images.githubusercontent.com/17734314/68861839-e6c05880-071e-11ea-91b3-5373484e51f7.png)

## Credit:

Part of the code are ported from twitter.com/year_progress <https://github.com/filiph/progress_bar>
