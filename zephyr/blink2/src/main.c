/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS   200

/* The devicetree node identifier for the "led0" alias. */

#define ARDUINO_GPIO DT_NODELABEL(arduino_header) // correct
#if DT_NODE_HAS_STATUS(ARDUINO_GPIO, okay)
//#define ARDU_NODE_IDENTIFIER DT_PHANDLE_BY_IDX(ARUDINO_GPIO, gpio_map, 1)
#define ARDU_POINTER_DEVICE DEVICE_DT_GET(ARDU_NODE_IDENTIFIER)
#define ARDU DT_GPIO_LABEL_BY_IDX(ARDUINO_GPIO, gpio_map, 1)
//#define ARDU DEVICE_NAME_GET(ARDU_NODE_IDENTIFIER)
//#define ARDU DEVICE_DT_NAME(ARDUINO_GPIO)
//#define ARDU DT_GPIO_PIN_BY_IDX(ARDUINO_GPIO, gpio_map, 1)
//#define ARDU_MAP DT_GPIO_PIN(ARDUINO_GPIO, gpio_map)
//#define ARDU_FLAGS DT_GPIO_FLAGS(ARDUINO_GPIO, gpio_map)
#else
#error "Phandle error"
#define ARDU ""
#define ARDU_MAP 0
#define ARDU_FLAGS 0
#endif

#define LED0_NODE DT_ALIAS(led0)
#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
#define LED0	DT_GPIO_LABEL(LED0_NODE, gpios)
#define PIN	DT_GPIO_PIN(LED0_NODE, gpios)
#define FLAGS	DT_GPIO_FLAGS(LED0_NODE, gpios)
#else
/* A build error here means your board isn't set up to blink an LED. */
#error "Unsupported board: led0 devicetree alias is not defined"
#define LED0	""
#define PIN	0
#define FLAGS	0
#endif

void main(void)
{
	const struct device *dev;
	const struct device *dev_test;
	bool led_is_on = true;
	int ret;

	dev_test = device_get_binding("GPIO_1");
	ret = gpio_pin_configure(dev_test, 27, GPIO_OUTPUT);
    //dev_test = device_get_binding(ARDU);
    //dev_test = ARDU_POINTER_DEVICE;
	dev = device_get_binding(LED0);
	if (dev == NULL) {
		return;
	}
    if(dev_test == NULL){
        return;
    }

	// ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
	if (ret < 0) {
		return;
	}

	// while (1) {
	// 	gpio_pin_set(dev, PIN, (int)led_is_on);
	// 	led_is_on = !led_is_on;
	// 	k_msleep(SLEEP_TIME_MS);
	// }
}