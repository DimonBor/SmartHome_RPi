import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

def get_device_list():

    try:
        with open('devices', 'r') as devices:
            device_list = json.load(devices)
    except FileNotFoundError:
        with open('devices', 'w') as devices:
            json.dump([], devices)
        with open('devices', 'r') as devices:
            device_list = json.load(devices)

    return device_list


def create_device(device_name, device_type, gpio):

    device_list = get_device_list()
    new_device = [device_name, "off", device_type, gpio]
    device_list.append(new_device)

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)

    update_gpio()

def delete_device(device_name):

    device_list = get_device_list()

    for device in device_list:
        if device[0] == device_name:
            device_list.remove(device)

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)

    update_gpio()

def turn_on(device):

    device_list = get_device_list()
    device_list[device_list.index(device)][1] = "on"

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)

    update_gpio()

def turn_off(device):

    device_list = get_device_list()
    device_list[device_list.index(device)][1] = "off"

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)

    update_gpio()

def update_gpio():

    device_list = get_device_list()
    GPIO.cleanup()

    for device in device_list:
        GPIO.setup(device[3], GPIO.OUT, initial=GPIO.LOW)
        if device[1] == "on": GPIO.output(device[3], 1)
        else: GPIO.output(device[3], 0)
