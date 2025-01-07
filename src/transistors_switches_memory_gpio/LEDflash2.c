// Compile: gcc -o LEDflash2 -l wiringPi

#include <wiringPi.h> // Include WiringPi library!
#include <unistd.h>   // usleep

int main(void)
{
    int pin_num = 17;

    // uses BCM numbering of the GPIOs and directly accesses the GPIO registers.
    wiringPiSetupGpio();

    // pin mode ..(INPUT, OUTPUT, PWM_OUTPUT, GPIO_CLOCK)
    pinMode(pin_num, OUTPUT);

    // pull up/down mode (PUD_OFF, PUD_UP, PUD_DOWN) => down
    pullUpDnControl(pin_num, PUD_OFF);

    for (int idx = 0; idx < 10; idx++) {
        digitalWrite(pin_num, HIGH);
        usleep(500000);          // cannot use sleep as it is non-blocking
        digitalWrite(pin_num, LOW);
        usleep(500000);          // cannot use sleep as it is non-blocking
    }
}