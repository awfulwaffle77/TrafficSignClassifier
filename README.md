# Traffic Sign Classifier
A traffic sign classifier on the MIMXRT1020 EVK. 

## Issues

###  Getting Zephyr on the board
- The OpenSDA J-Link probe is an **onboard** chip and an external debugger is **not** needed
- The reset button is SW5, next to the Micro USB port
- **WSL did not support `west flash` at the time of writing, as JLinkExe was throwing the `Connecting to J-Link failed` error even after adding the `99-jlink.rules` ruleset to `/etc/udev/rules.d`**
- Be sure to add the [firmware](https://www.segger.com/downloads/jlink/OpenSDA_MIMXRT1020-EVK) to be able to see the board in `/dev` (by holding SW5 while powering up the board)
- Testing with the GUI Putty did not work for me, so I did from CLI with the following command: `sudo putty /dev/ttyACM0 -serial -sercfg 115200,8,n,1`. The connection should show some numbers when nothing is flashed on it
- Be sure to download [J-Link](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack) **and read the README included**
- Only after Dual Booting Linux was I able to get it working by following the steps on [Zephyr website](https://docs.zephyrproject.org/latest/boards/arm/mimxrt1020_evk/doc/index.html).
- I have also installed `libusb-1.0-0-dev`, but I do not believe it is needed
