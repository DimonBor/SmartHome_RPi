from flask import Flask, request, render_template, redirect
import time as t
import setup

app = Flask(__name__)

@app.route('/')
def home_page():

    device_list = setup.get_device_list()
    setup.update_gpio()
    return render_template('home.html', device_list=device_list)


@app.route('/setup')
def setup_page():

    device_list = setup.get_device_list()
    setup.update_gpio()
    return render_template('setup.html', device_list=device_list)


@app.route('/help')
def hekp_page():

    setup.update_gpio()
    return render_template('help.html')


@app.route('/changestate', methods=['POST'])
def changestate():

    try: device_name = request.form['device_name']
    except: return "Wrong Data!"

    setup.update_gpio()
    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            if device[2] == "click":
                setup.turn_on(device)
                t.sleep(0.5)
                device[1] = "on"
                setup.turn_off(device)
            elif device[1] == "off": setup.turn_on(device)
            else: setup.turn_off(device)
            return redirect('/')

    return "ERROR: Device not found"


@app.route('/add_device', methods=['POST'])
def add_device():

    setup.update_gpio()

    print(request.form)

    try:
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        gpio = request.form['gpio']
    except: return "Wrong Data!"

    if device_type not in ["switch", "click"]:
        return "Wrong type!"

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            device_name += "_new"
    for device in device_list:
        if device[3] == gpio and gpio != "none":
            return "ERROR: GPIO already used."

    setup.create_device(device_name, device_type, gpio)
    return redirect('/setup')


@app.route('/remove_device', methods=['POST'])
def remove_device():

    setup.update_gpio()

    try: device_name = request.form['device_name']
    except: return "Wrong Data!"

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name:
            setup.delete_device(device_name)
            return "OK"

    return "ERROR: Not found"


@app.route('/edit_device', methods=['POST'])
def edit_device():

    print(request.form)

    try:
        device_name = request.form['device_name']
        device_type = request.form['radios']
        gpio = request.form['gpio']
        button_sel = request.form['button_sel']
        device_id = request.form['device_id']
    except: return "Wrong Data!"

    if button_sel == "Удалить":
        setup.delete_device(device_name)
        return redirect('/setup')

    device_list = setup.get_device_list()

    for device in device_list:
        if device[0] == device_name and device[4] != int(device_id):
            return "ERROR: Name already used."

    for device in device_list:
        if device[4] == int(device_id):
            setup.edit_device(device_id, device_name, device_type, gpio)
            return redirect('/')

    return "ERROR: Not found"


@app.route('/get_devices_status', methods=['GET'])
def get_devices_status():

    setup.update_gpio()
    return str(setup.get_device_list())


app.run(host='0.0.0.0', port=5000)
