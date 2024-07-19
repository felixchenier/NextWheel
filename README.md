# NextWheel - Open design of next-generation instrumented wheelchair wheels

The only company producing commercial instrumented wheels for standard wheelchairs (SmartWheel) closed its doors in 2014. Therefore, the existing wheels are no longer supported and are now obsolete. Since no new company sells an equivalent product, we started a project to upgrade the current SmartWheel and eventually build completely new instrumented wheels, with an open-hardware, open-source approach.

In the present state of the project, we currently have a complete replacement PCB with modern components, a firmware to flash its microcontroller, and a Python module to communicate with the wheel.

This repository is in heavy development; if you are interested in this project, we recommend to communicate with our team so that we can guide you, build PCBs for you, or start collaborations: [chenier.felix@uqam.ca](mailto:chenier.felix@uqam.ca)


## Repository structure

- [schematics](schematics): The electronics schematics and masks for the replacement PCB.
- [firmware](firmware): The ESP32 firmware to be compiled and flashed to the microcontroller.
- [python](python): A python module to control de wheel and get streamed data in real time.
- [calibration](calibration): A calibration wizard written in Python that calibrates the wheel using a step-by-step procedure including spinning the wheel and applying known weights on the pushrim.

## Main contributors

- Félix Chenier: Project leader, Python module
- Dominic Létourneau: Firmware
- Antoine Parrinello: PCB
- Nicolas Fleury-Rousseau: Calibration
