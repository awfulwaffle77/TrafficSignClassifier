#include <zephyr.h>
#include <device.h>
#include <drivers/gpio.h>
#include <sys/printk.h>

#define LED_PORT GPIO_AD_B0_050
#define LED LED_Y1
#define SLEEP_TIME 1000

void main(void)
{
    int x = 6;
    printk("Hello world %d %s\n", x, CONFIG_BOARD);

    int count = 0;
    struct device *dev;
    dev = device_get_binding(LED_PORT);
    gpio_pin_configure(dev, LED, GPIO_DIR_OUT);
}
