from microbit import *

display.off()

output_pins = [pin1, pin2, pin3, pin4, pin6, pin7, pin8]  # pin 5 not used
resistors = [1000000, 330000, 100000, 33000, 10000, 3300, 1000]
analog_pin = pin10
SAMPLE_COUNT = 10
Vcc = 3.3  # Positive rail voltage
Vmid = 0.5 * Vcc


def convert_to_volts(adc_reading):
    return Vcc * adc_reading / 1023.0


def read_voltage(pin):
    sleep(5)  # delay to stabilize readings
    return convert_to_volts(pin.read_analog())


def average_voltage(pin):
    total = sum([read_voltage(pin) for i in range(SAMPLE_COUNT)])
    return total / SAMPLE_COUNT


def resistance_from(res, volts):
    return res / (Vcc / volts - 1.0);


# put the pins into high-impedence mode
for pin in output_pins:
    pin.write_digital(0)
    pin.read_digital()
    pin.set_pull(pin.NO_PULL)

while True:
    minimum = Vmid
    resistance = 1.0E6
    for (pin, r1) in zip(output_pins, resistors):
        pin.write_digital(1)
        sleep(5)
        av = average_voltage(analog_pin)
        difference = abs(Vmid - av)
        if av < Vcc and difference < minimum:
            minimum = difference
            resistance = resistance_from(r1, av)
        pin.write_digital(0)
        pin.read_digital()
        pin.set_pull(pin.NO_PULL)
    print(resistance)
    sleep(3000)
