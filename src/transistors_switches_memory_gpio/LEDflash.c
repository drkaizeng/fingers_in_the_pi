// compile using: gcc LEDflash.c -o LEDflash
// execute using: sudo ./LEDflash

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/mman.h>
#include <stdint.h>   // for uint32_t - 32-bit unsigned integer
#include <unistd.h>   // getuid
#include <string.h>   // strerror

#define GPIO_BASE    0xFE200000   // The returned value of `sudo cat /proc/iomem | grep gpio -i`
#define GPSET0       0x1c         // BCM2711 datasheet p. 66; BCM2835 datasheet p. 90
#define GPCLR0       0x28         // BCM2711 datasheet p. 66; BCM2835 datasheet p. 90
#define GPLVL0       0x34         // GPLEV0 on BCM2711 p. 66; BCM2835 p. 90
static volatile uint32_t* gpio;   // pointer to the gpio (*int)

int main() {
    int fd, x;
    printf("Start of GPIO memory-manipulation test program.\n");
    if (getuid() != 0) {
       printf("You must run this program as root. Exiting.\n");
       return -EPERM;
    }
    if ((fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
       printf("Unable to open /dev/mem: %s\n", strerror(errno));
       return -EBUSY;
    }
    // get a pointer that points to the peripheral base for the GPIOs
    // All accesses are assumed to be 32-bit (BCM2711 p. 66)
    gpio = (uint32_t *) mmap(0, getpagesize(), PROT_READ | PROT_WRITE,
       MAP_SHARED, fd, GPIO_BASE);
    // On error, the value MAP_FAILED (that is, (void *) -1) is returned, and errno is set to indicate the error.
    if (gpio == (void *) -1) {
       printf("Memory mapping failed: %s\n", strerror(errno));
       return -EBUSY;
    }
    // at this point gpio points to the GPIO peripheral base address
    // set up the LED GPIO FSEL17 mode = 001 at addr GPFSEL1 (0004)
    // From the GPFSEL1 Register Table on p. 67 of BCM2711, 001 means the pin is an output
    // gpio points to uint32. Thus, moving one step is equivalent to 
    // moving 4 bytes, which is the offset for GPFSEL1
    // writing NOT 7 (i.e., ~111) clears bits 21, 22 and 23.
    *(gpio + 1) = (*(gpio + 1) & ~(7 << 21) | (1 << 21));
 
    // turn the LED on using the bit 17 on the GPSET0 register
    for (int idx = 0; idx < 10; idx++) {
        // Each move of the gpio pointer is equivalent to jumping 4 bytes. Thus divide the offset by 4.
        *(gpio + (GPSET0 / 4)) = 1 << 17;
        usleep(500000);          // cannot use sleep as it is non-blocking
        *(gpio + (GPCLR0 / 4)) = 1 << 17;  // turn the LED off
        usleep(500000);          // cannot use sleep as it is non-blocking
    }
 
    close(fd);
    return 0;
}