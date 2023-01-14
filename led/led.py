from gpiozero import LED
from time import sleep
from typing import List


def delayed_array_blink(lead_time: float, leds: List[LED], should_blink: List[bool], led_on_time: float) -> None:
    sleep(lead_time)
    for led, to_blink in zip(leds, should_blink):
        if to_blink:
            led.on()
    sleep(led_on_time)
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


if __name__ == "__main__":
    light_show()
