# -*- coding: utf-8 -*-
"""
Year progress.

Configuration parameters:
    progress_block: block type to show progress (default '▓')
    remain_block: block type to show remaining progress (default '░')
    progress_width: progress bar width (default 5)
    cache_timeout: refresh interval for this module, default 1 hour (default 3600)

Format placeholders:
    {progress_bar} Progress bar
    {ratio} Progress ratio


Examples:
```
year_progress {
    format = "{progress_bar} {ratio}%"
    progress_block = '▓'
    remain_block = '░'
    progress_width = 5
}
```

@author azzamsa <https://github.com/azzamsa>
@license GPLv3 <https://www.gnu.org/licenses/gpl-3.0.txt>

Notes:
    Credit: Part of the code are ported from twitter.com/year_progress <https://github.com/filiph/progress_bar>

SAMPLE OUTPUT
{'full_text': '▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 86%'}
"""

from datetime import datetime, tzinfo, timedelta


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


def compute_progress(start, end, current):
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(current, datetime)

    whole_diff = end - start
    whole_diff_in_seconds = whole_diff.days * 86400 + whole_diff.seconds
    if whole_diff_in_seconds == 0:
        raise ValueError("Start and end datetimes are equal.")
    current_diff = current - start
    current_diff_in_seconds = current_diff.days * 86400 + current_diff.seconds
    return float(current_diff_in_seconds) / float(whole_diff_in_seconds)


def compute_current_year_progress(current=None):
    if not current:
        current = datetime.now(tz=UTC())
        start = datetime(current.year, 1, 1, tzinfo=UTC())
        end = datetime(current.year + 1, 1, 1, tzinfo=UTC())
    return compute_progress(start, end, current)


class Py3status:
    format = "{progress_bar} {ratio}%"
    progress_width = 5
    progress_block = "▓"
    remain_block = "░"
    cache_timeout = 3600

    def _create_progress_string(self, progress, width=20):
        progress_int = int(round(progress * width))
        rest_int = int(width - progress_int)
        return "{}{}".format(
            self.progress_block * progress_int, self.remain_block * rest_int
        )

    def year_progress(self):
        progress_ratio = compute_current_year_progress()
        ratio_int = int(progress_ratio * 100)
        progress_bar = self._create_progress_string(
            progress_ratio, width=self.progress_width
        )

        data = {"progress_bar": progress_bar, "ratio": ratio_int}
        status = self.py3.safe_format(self.format, data)

        return {
            "full_text": status,
            "cached_until": self.py3.time_in(self.cache_timeout),
        }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
