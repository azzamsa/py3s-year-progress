# -*- coding: utf-8 -*-
"""
Year progress.

Configuration parameters:
    progress_block: block type to show progress (default '▓')
    remain_block: block type to show remaining progress (default '░')
    progress_width: progress bar width (default 5)
    cache_timeout: refresh interval for this module, default 1 hour (default 3600)
    ctime: custom time for the end of progress, useful for appointment/birthday progress.

Format placeholders:
    {progress_bar} Progress bar
    {ratio} Progress ratio
    {mode} Progress mode [year|month|day|week], click the module to cycle (default 'year')


Examples:
```
year_progress {
    format = "{progress_bar} {ratio}%{mode}"
    progress_block = '▓'
    remain_block = '░'
    progress_width = 5
    ctime = ["2020-12-16 20:59:00", "%Y-%m-%d %H:%M:%S"]
}
```

@author azzamsa <https://github.com/azzamsa>
@license GPLv3 <https://www.gnu.org/licenses/gpl-3.0.txt>

Notes:
    Credit: Part of the code are ported from twitter.com/year_progress <https://github.com/filiph/progress_bar>

SAMPLE OUTPUT
{'full_text': '▓▓▓▓░ 87%y'}

{'full_text': '▓▓▓░░ 50%m'}

{'full_text': '▓▓░░░ 33%d'}

{'full_text': '▓▓▓▓░ 83%w'}
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
    whole_diff = end - start
    whole_diff_in_seconds = whole_diff.days * 86400 + whole_diff.seconds

    if whole_diff_in_seconds == 0:
        raise ValueError("Start and end datetimes are equal.")
    current_diff = current - start
    current_diff_in_seconds = current_diff.days * 86400 + current_diff.seconds

    return float(current_diff_in_seconds) / float(whole_diff_in_seconds)


def compute_current_week_progress(current=None, week_end=None):
    """Compute current day progress to the end of the week"""
    if not current:
        current = datetime.now(tz=UTC())

    week_start = current - timedelta(days=current.weekday())
    if not week_end:
        week_end = week_start + timedelta(days=6)
    return compute_progress(week_start, week_end, current)


def compute_current_day_progress(current=None, end=None):
    """Compute current hour progress to tomorrow (00:00 AM)"""
    if not current:
        current = datetime.now().astimezone()

    # start at 00:00 AM
    start = datetime(current.year, current.month, current.day).astimezone()
    if not end:
        end = datetime(
            current.year, current.month, current.day, 23, 59, 00
        ).astimezone()

    return compute_progress(start, end, current)


def compute_current_month_progress(current=None, end=None):
    """Compute current date to the first date of  next month"""
    if not current:
        current = datetime.now(tz=UTC())

    start = datetime(current.year, current.month, 1, tzinfo=UTC())
    if not end:
        # month max 12
        if current.month == 12:
            end = datetime(current.year, current.month, 31, tzinfo=UTC())
        else:
            end = datetime(current.year, current.month + 1, 1, tzinfo=UTC())
    return compute_progress(start, end, current)


def compute_current_year_progress(current=None, end=None):
    """Compute current year progress to next year"""
    if not current:
        current = datetime.now(tz=UTC())

    start = datetime(current.year, 1, 1, tzinfo=UTC())
    if not end:
        end = datetime(current.year + 1, 1, 1, tzinfo=UTC())
    return compute_progress(start, end, current)


class Py3status:
    format = "{progress_bar} {ratio}%{mode}"
    progress_width = 5
    progress_block = "▓"
    remain_block = "░"
    cache_timeout = 3600
    progress_mode = "year"
    ctime = None
    thresholds = 90  # precentage, .e.g 90%

    def _check_urgency(self, thresholds, progress):
        urgency = False
        print(progress)
        if progress > thresholds:
            urgency = True

        return urgency

    def _create_progress_string(self, progress, width=20):
        progress_int = int(round(progress * width))
        rest_int = int(width - progress_int)
        return "{}{}".format(
            self.progress_block * progress_int, self.remain_block * rest_int
        )

    def year_progress(self):
        end_time = None
        if self.ctime:
            end_time = datetime.strptime(self.ctime[0], self.ctime[1]).astimezone()

        if self.progress_mode == "year":
            progress_ratio = compute_current_year_progress(end=end_time)
            mode = "y"
        elif self.progress_mode == "month":
            progress_ratio = compute_current_month_progress(end=end_time)
            mode = "m"
        elif self.progress_mode == "day":
            progress_ratio = compute_current_day_progress(end=end_time)
            mode = "d"
        elif self.progress_mode == "week":
            progress_ratio = compute_current_week_progress()
            if end_time:  # can't use custom end time
                progress_ratio = None
            mode = "w"

        if progress_ratio:
            ratio_int = int(progress_ratio * 100)
            progress_bar = self._create_progress_string(
                progress_ratio, width=self.progress_width
            )
            is_urgent = self._check_urgency(self.thresholds, ratio_int)
        else:
            progress_bar = ":)"
            ratio_int = 0

        color = None
        if is_urgent:
            color = self.py3.COLOR_BAD

        data = {"progress_bar": progress_bar, "ratio": ratio_int, "mode": mode}
        status = self.py3.safe_format(self.format, data)

        return {
            "full_text": status,
            "color": color,
            "cached_until": self.py3.time_in(self.cache_timeout),
        }

    def on_click(self, event):
        if self.progress_mode == "year":
            self.progress_mode = "month"
        elif self.progress_mode == "month":
            self.progress_mode = "day"
        elif self.progress_mode == "day":
            self.progress_mode = "week"
        elif self.progress_mode == "week":
            self.progress_mode = "year"


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    Py3status.progress_mode = "day"

    module_test(Py3status)
