#
#   Flask web application for volume control
#

from flask import Flask, render_template, request
import soco,threading,time

device = soco.discovery.any_soco()

exit_event = threading.Event()

global volume
volume = 35

def AdjustVolume():  
    global volume

    while not exit_event.is_set():
        device.volume = volume
        time.sleep(0.01)

app = Flask(__name__)
app.secret_key = "SvaW4F$FGGG<>:T"

@app.route("/")
def index():
    return render_template("index.html", volume=volume, device_name=device.player_name, device_ip=device.ip_address)

@app.route("/save", methods=["POST","GET"])
def save():
    global volume
    volume = request.form['volume_input']

    return render_template("index.html", volume=str(volume), device_name=device.player_name, device_ip=device.ip_address)

def main():
    volume_thread = threading.Thread(target=AdjustVolume)
    volume_thread.start()

    app.run(host="0.0.0.0", port=80)

    exit_event.set()

if __name__ == "__main__":
    main()
