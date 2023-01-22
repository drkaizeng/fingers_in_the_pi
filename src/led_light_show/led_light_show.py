from __future__ import annotations

import argparse
import subprocess
from time import sleep
from typing import Callable, List, NamedTuple
from pathlib import Path

from gpiozero import LED


def delayed_array_blink(lead_time: float, leds: List[LED], should_blink: List[int], blink_length: float) -> None:
    sleep(lead_time)
    for led, to_blink in zip(leds, should_blink):
        if to_blink:
            led.on()
    sleep(blink_length)
    for led in leds:
        led.off()


def light_show() -> None:
    jim = LED(17)
    kai = LED(26)

    def blink(lead_time, should_blink, led_on_time):
        delayed_array_blink(lead_time, [jim, kai], should_blink, led_on_time)

    blink(1, [1, 1], 0.1)
    blink(0.5, [0, 1], 0.2)
    blink(0.3, [1, 0], 0.3)
    blink(0.9, [1, 0], 0.3)
    blink(0.7, [1, 1], 0.3)
    blink(0.2, [1, 0], 0.3)
    blink(0.8, [0, 1], 12)
    blink(1, [1, 1], 6)
    blink(0.9, [0, 1], 3)
    blink(0.3, [1, 0], 0.3)


def get_blink_controls() -> List[BlinkControl]:
    ...


class BlinkControl(NamedTuple):
    time: TimePoint
    should_blink: List[int]
    blink_length: float


def process_blink_controls(leds: List[LED], controls: List[BlinkControl]) -> List[Callable]:
    ret = []
    for i, ctrl in enumerate(controls):
        if len(leds) != len(ctrl.should_blink):
            raise ValueError()
        elif i == 0:
            ret.append(lambda: delayed_array_blink(ctrl.time.to_seconds(), leds, ctrl.should_blink, ctrl.blink_length))
        else:
            if controls[i - 1] > controls[i]:
                raise ValueError()
            lead_time = ctrl.time - controls[i - 1].time
            ret.append(lambda: delayed_array_blink(lead_time, leds, ctrl.should_blink, ctrl.blink_length))
    return ret


class TimePoint:
    """
    This is the time since the start of the song (time 0).
    """

    def __init__(self, minutes: int, seconds: float) -> None:
        if minutes < 0 or seconds < 0:
            raise ValueError()
        self._minutes = minutes
        self._seconds = seconds

    def __gt__(self, other: TimePoint) -> bool:
        if self._minutes > other._minutes:
            return True
        elif (self._minutes == other._minutes) and (self._seconds > other._seconds):
            return True
        else:
            return False

    def __sub__(self, other: TimePoint) -> float:
        """
        Return the difference in seconds.
        """
        m_diff = self._minutes - other._minutes
        s_diff = self._seconds - other._seconds
        res = 60 * m_diff + s_diff
        return res

    def add_time(self, minutes: int, seconds: float) -> TimePoint:
        return TimePoint(self._minutes + minutes, self._seconds + seconds)

    def to_seconds(self) -> float:
        return self._minutes * 60 + self._seconds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--led-gpio-ids", nargs=3, help='If the LEDs are connected to GPIO 17, 27, 22, use "--led-gpio-ids 17 27 22"'
    )
    parser.add_argument(
        "--path-to-mp3", required=True, help='Full path to the MP3 version of the "Head shoulders knees and toes" song'
    )

    args = parser.parse_args()

    if not Path(args.path_to_mp3).is_file():
        raise ValueError()

    leds = [LED(x) for x in args.led_gpio_ids]

    controls = get_blink_controls()
    funcs = process_blink_controls(leds, controls)

    subprocess.Popen(["mpg123", "--quiet", args.path_to_mp3], stderr=subprocess.DEVNULL)
    for func in funcs:
        func()


if __name__ == "__main__":
    light_show()
