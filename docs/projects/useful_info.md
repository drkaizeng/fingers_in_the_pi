# Useful info

## The power rating of the pins
The following is from [here](https://forums.raspberrypi.com/viewtopic.php?t=196531). However, as the person who posted the information pointed out, there appears to be no official documentation on the matter.
> First we need to make the distinction between the actual GPIO pins, the ones with input/output capability, and the other pins on the GPIO header, which are ground (GND), 3V3 power and 5V power.
> 
> From the information I gathered while researching this, the GPIO total output current limit is 100mA for the newer models (40 pin) and 50mA for the older models (26 pin), with a limit of 16mA per GPIO pin (which is the limit of the board traces).
> 
> The 5V power pins can go higher. Not sure what the 5V power limit is, but I have run fans that pull over 300mA 24/7 for days without any problems (I expect the 5V limit is whatever the board traces can handle, but have I no idea what that is). The 3V3 power pins are limited by the 3V3 regulator, which is also different between the older and newer models (linear vs switching).
> 
> I have seen a few references that said the newer 3V3 switching regulator is 1A, but do note that the SoC and GPIO uses a significant portion of the available 3V3 power, so there's not a lot of power available on the 3V3 power pins.