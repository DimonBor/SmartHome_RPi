import json

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


def create_device(device_name):

    device_list = get_device_list()
    new_device = [device_name, "off"]
    device_list.append(new_device)

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)


def delete_device(device_name):

    device_list = get_device_list()

    for device in device_list:
        if device[0] == device_name:
            device_list.remove(device)

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)


def turn_on(device):

    device_list = get_device_list()
    device_list[device_list.index(device)][1] = "on"

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)


def turn_off(device):

    device_list = get_device_list()
    device_list[device_list.index(device)][1] = "off"

    with open('devices', 'w') as devices:
        json.dump(device_list, devices)
