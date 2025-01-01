# NPN transitors as switches and memory-based GPIO control

This project is based on the following sections in *Molloy - Exploring Raspberry Pi* (hereafter referred to as the Book):
- LED: pp. 128 - 129
- Transistors: pp. 132 - 138
- Fig. 6-2(b) on p. 223
- Memory-based GPIO control: pp. 245 - 252

## The circuit
A S8050 NPN transistor was used in a circuit similar to Fig. 6-2(b). The base resistor value was determined by using the equation on p. 135 of the Book
$$
R_{base} = \frac{V_B - V_{BE(sat)}}{2 \times (I_C \div h_{FE(min)})}
$$
For this curcuit, $V_B = 3.3\text{V}$. $I_C$ is approximately 5V (the output of pin 2) divided by 220$\Omega$ (LED has little resistance; see p. 129 of the Book), which comes out as 0.023A. This is well within the power rating of the pins (see [here](./useful_info.md#the-power-rating-of-the-pins)). From p. 2 of S8050's dataset, $h_{FE(min)} = 40$. Using the 4th figure on p. 3 of S8050's dataset, $V_{BE(sat)}$ is approximately 0.8V. Thus, $R_{base}=2173.91\Omega$. Thus, two 1K $\Omega$ resistors and one 220 $\Omega$ were used.
![](figs/transistors_switches_memory_gpio_1.jpg){:style="height:600px"}
![](figs/transistors_switches_memory_gpio_2.jpg){:style="height:600px"}

## Controlling the LED
V4 of the Pi no longer supports `sysfs` described in the Book.

### Using `pinctrl`
```bash
# Turning the LED on, by setting GPIO 17 to output high 
pinctrl set 17 op dh

# Turning the LED off, by setting GPIO 17 to be an output zero/low
pinctrl set 17 op dl
```
