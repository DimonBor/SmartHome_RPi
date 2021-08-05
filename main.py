from flask import Flask, request, render_template
from markupsafe import escape
import setup

app = Flask(__name__)

@app.route('/')
def home_page():
    device_list = setup.get_device_list()
    return render_template('home.html', device_list=device_list)


@app.route('/setup')
def setup_page():

    return render_template('setup.html')


@app.route('/help')
def hekp_page():

    return render_template('help.html')


@app.route('/changestate', methods=['POST'])
def changestate():

    try: device_name = request.form['device_name']
    except: return "Wrong Data!"

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            if device[1] == "off": setup.turn_on(device)
            else: setup.turn_off(device)
            return "OK"

    return "ERROR: Device not found"


@app.route('/add_device', methods=['POST'])
def add_device():

    try:
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        gpio_number = request.form['gpio']
    except: return "Wrong Data!"

    if device_type not in ["switch", "click"]:
        return "Wrong type!"

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            return "ERROR: Device already exists."
    for device in device_list:
        if device[3] == gpio_number:
            return "ERROR: GPIO already used."

    setup.create_device(device_name, device_type, gpio_number)
    return "OK"


@app.route('/remove_device', methods=['POST'])
def remove_device():

    try: device_name = request.form['device_name']
    except: return "Wrong Data!"

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            setup.delete_device(device_name)
            return "OK"

    return "ERROR: Not found"


@app.route('/get_devices_status', methods=['GET'])
def get_devices_status():
    return str(setup.get_device_list())

app.run(host='0.0.0.0', port=5000)
