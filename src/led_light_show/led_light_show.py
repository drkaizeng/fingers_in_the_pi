from __future__ import annotations

import argparse
import subprocess
from time import sleep
from typing import List, NamedTuple, Tuple
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


def get_blink_controls() -> List[BlinkControl]:
    lst = []
    lst.append(BlinkControl(TimePoint(0, 5.02), [1, 0, 0], 0.08))
    for i in range(5):
        secs = 6.1 + i * 0.38
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))
    lst.append(BlinkControl(TimePoint(0, 8.03), [1, 0, 0], 0.07))
    for i in range(3):
        secs = 8.78 + i * 0.37
        lst.append(BlinkControl(TimePoint(0, secs), [1, 0, 1], 0.07))
    lst.append(BlinkControl(TimePoint(0, 11.02), [0, 1, 0], 0.07))
    for i in range(6):
        secs = 12.15 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))
    for i in range(5):
        secs = 14.79 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))
    for i in range(4):
        secs = 17.03 + i * 0.75
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))
    
    for i in range(5):
        secs = 20.03 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))
    
    for i in range(5):
        secs = 22.29 + i * 0.75
        arr = [0] * 3
        offset = (i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    # Big ding
    lst.append(BlinkControl(TimePoint(0, 26.03), [1, 1, 1], 0.1))

    lst.append(BlinkControl(TimePoint(0, 29.05), [0, 1, 0], 0.07))
    for i in range(3):
        secs = 29.05 + (i + 1) * 0.182
        lst.append(BlinkControl(TimePoint(0, secs), [1, 0, 1], 0.04))
    
    lst.append(BlinkControl(TimePoint(0, 30.55), [0, 1, 0], 0.07))
    for i in range(3):
        secs = 30.55 + (i + 1) * 0.182
        lst.append(BlinkControl(TimePoint(0, secs), [1, 0, 1], 0.04))
    
    # Big ding
    lst.append(BlinkControl(TimePoint(0, 32.85), [1, 1, 1], 0.25))

    lst.append(BlinkControl(TimePoint(0, 35.06), [0, 1, 0], 0.07))
    for i in range(3):
        secs = 35.06 + (i + 1) * 0.182
        lst.append(BlinkControl(TimePoint(0, secs), [1, 0, 1], 0.04))

    lst.append(BlinkControl(TimePoint(0, 36.55), [0, 1, 0], 0.07))
    for i in range(2):
        secs = 36.55 + (i + 1) * 0.182
        lst.append(BlinkControl(TimePoint(0, secs), [1, 0, 1], 0.04))

    for i in range(3):
        secs = 37.28 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    lst.append(BlinkControl(TimePoint(0, 41.02), [1, 0, 1], 0.07))
    for i in range(6):
        secs = 42.16 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    lst.append(BlinkControl(TimePoint(0, 47.04), [1, 0, 0], 0.07))
    for i in range(4):
        secs = 47.65 + i * 0.75
        arr = [0] * 3
        offset = (i + 1) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    for i in range(4):
        secs = 50.4 + i * 0.37
        arr = [0] * 3
        offset = (2 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    lst.append(BlinkControl(TimePoint(0, 53.03), [1, 0, 0], 0.07))
    for i in range(6):
        secs = 54.15 + i * 0.37
        arr = [0] * 3
        offset = (1 + i) % 3
        arr[offset] = 1
        lst.append(BlinkControl(TimePoint(0, secs), arr, 0.07))

    lst.append(BlinkControl(TimePoint(0, 56.79), [1, 1, 1], 0.07))
    lst.append(BlinkControl(TimePoint(0, 57.54), [1, 1, 1], 0.07))

    # Singing begins
    for i in range(31):
        tp = TimePoint(0, 59.03).add_seconds(0.75 * i)
        arr = [0] * 3
        offset = (i % 2) * 2
        arr[offset] = 1
        lst.append(BlinkControl(tp, arr, 0.06))
    lst.append(BlinkControl(TimePoint(0, 0).add_seconds(82.28), [1, 1, 1], 0.05))

    # # Change tempo
    # for i in range(4):
    #     tp = TimePoint(1, 23).add_seconds(0.5 * i)
    #     lst.append(BlinkControl(tp, [0, 1, 0], 0.1))
    #     for i in range(2):
    #         tp = tp.add_seconds((i + 1) * 0.15)
    #         lst.append(BlinkControl(tp, [1, 0, 1], 0.05))

    return lst


class BlinkControl(NamedTuple):
    time: TimePoint
    should_blink: List[int]
    blink_length: float


def process_blink_controls(
    leds: List[LED], controls: List[BlinkControl]
) -> List[Tuple[float, List[LED], List[int], float]]:
    ret = []
    for i, ctrl in enumerate(controls):
        if len(leds) != len(ctrl.should_blink):
            raise ValueError()
        elif i == 0:
            lead_time = ctrl.time.to_seconds()
        else:
            previous_ctrl = controls[i - 1]
            if not (ctrl > previous_ctrl):
                raise ValueError()
            lead_time = ctrl.time - previous_ctrl.time - previous_ctrl.blink_length
        ret.append((lead_time, leds, ctrl.should_blink, ctrl.blink_length))
    return ret


class TimePoint:
    """
    This is the time since the start of the song (time 0).
    """

    def __init__(self, minutes: int, seconds: float) -> None:
        if minutes < 0 or seconds < 0 or seconds >= 60:
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

    def add_seconds(self, seconds: float) -> TimePoint:
        if seconds < 0:
            raise ValueError()
        seconds = self._seconds + seconds
        secs = seconds % 60
        mins = int(seconds) // 60
        return TimePoint(self._minutes + mins, secs)

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

    leds = [LED(int(x)) for x in args.led_gpio_ids]

    controls = get_blink_controls()
    processed_ctrls = process_blink_controls(leds, controls)

    proc = subprocess.Popen(["mpg123", "--quiet", args.path_to_mp3], stderr=subprocess.DEVNULL)
    for ctrl in processed_ctrls:
        delayed_array_blink(*ctrl)

    proc.terminate()


if __name__ == "__main__":
    main()
