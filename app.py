#
#   Web application for volume control
#   Used libraries: SoCo, Flask    
#

from flask import Flask, render_template, request
import soco,threading,time

# Search for any device
device = soco.discovery.any_soco()

# Assing exit event to kill thread
exit_event = threading.Event()

# Global variable for keeping track of the volume
global volume
volume = 35

# Function to enforce volume while exit event is not set
def AdjustVolume():  
    global volume

    while not exit_event.is_set():
        device.volume = volume
        time.sleep(0.01)

# Declare Flask app
app = Flask(__name__)
app.secret_key = "SvaW4F$FGGG<>:T"

# Index page at the root of the domain
@app.route("/")
def index():
    return render_template("index.html", volume=volume, device_name=device.player_name, device_ip=device.ip_address)

# Updating the new volume
@app.route("/save", methods=["POST","GET"])
def save():
    global volume
    volume = request.form['volume_input']

    return render_template("index.html", volume=str(volume), device_name=device.player_name, device_ip=device.ip_address)

# Main function for starting volume thread and running flask app
def main():
    volume_thread = threading.Thread(target=AdjustVolume)
    volume_thread.start()

    app.run(host="0.0.0.0", port=80)

    exit_event.set()

if __name__ == "__main__":
    main()
