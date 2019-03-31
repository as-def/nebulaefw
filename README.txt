# Firmware Update

Welcome to the guide on updating the firmware for your Qu-Bit Nebulae.

This guide illustrates updating the firmware via the USB drive on the front of the module.

## What You Need

- A USB Drive
- A neb_update.zip firmware update file

## The process

- Add the neb_update.zip to the root directory of the USB drive.
- Insert the USB drive into the Nebulae.
- Make sure that no CVs are present at the control inputs. (The module performs a self-calibration after firmware updates)
- Power on the Nebulae
- After the typical boot time, the LEDs will begin to cycle green indicating the firmware is updating successfully.
- The update will take up to 90 seconds. 
- Once the update is complete the LEDs will stop rotating, and will remain green while the Nebulae performs a software reboot.
- The LEDs will begin cycling white to indicate the boot sequence, and subsequently aqua when it begins to load files.
- Once the module is running we recommend power cycling the module (with 5 seconds between turning the module off and turning it back on).

**It is recommended that the Nebulae not be powered down during a firmware update, or when loading files.**

## Reverting to the Factory Firmware

Adding a file "revert_to_factory_firmware" to the root directory of your USB drive will cause the Nebulae to revert to the factory firmware.

The file can be empty, and will be deleted after the reversion has been complete.

If something goes wrong with a firmware update, performing this or another firmware update will likely resolve the issue.

This will always revert to v1.0.0 of the Nebulae Firmware.

After booting the module up with the revert_factory_firmware file on the USB drive, it may take longer than normal to enter the boot sequence. 