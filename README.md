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

---

Added for 2.1.1.01

This readme file accompanies the Neb2 firmware (v 2.1.1.01) file uploaded on 30 March 2019.

This firmware file is named: neb_update.zip

That is the name that the Neb2 module requires in order to be recognized as a firmware update file.

This firmware is not an official firmware from Qu-Bit. Please use at your own risk.

If you choose to use this firmware file, please install it according to the instructions available on the Qu-Bit website.

This firmware file is based on the firmware 2.1.1 from Qu-Bit. Two changes have been made to the Qu-Bit firmware:

1. The code has been changed so that the module will now boot up correctly after it was shut down while an instrument from the user bank was loaded and playing. 

2. The fifth instrument (rightmost button) in the factory bank has been replaced with a new instrument. The fifth instrument in the official 2.1.1 firmware is a test instrument. (You can get the test instrument from Qu-Bit's website.) The new instrument file on this firmware is named, "e_newsize01.instr". It is a clone of the main instrument of the Neb2 module (a_granularloop.instr) with a change to the way that the 'start' and 'size' functions interact. In the original instrument (which is still on this firmware, in the same place), changing the 'start' control also changes the size of the loop. In the new version, changing the 'start' control has no effect on the size of the loop. This allows one to sweep through their loop without changing the size of the loop length and speed at which the loop plays.

It is possible that this firmware file will be updated as changes and/or improvements are made.

If you have trouble with this firmware file, please reinstall the official firmware from Qu-Bit to restore the previous functionality to your module.