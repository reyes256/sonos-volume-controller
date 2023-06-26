import soco, threading, time, sys
from flask import Flask, render_template, request
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

device = soco.discovery.any_soco()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", volume=volume, device_name=device.player_name, device_ip=device.ip_address)

@app.route("/save", methods=["POST","GET"])
def save():
    global volume
    volume = request.form['volume_input']

    return render_template("index.html", volume=str(volume), device_name=device.player_name, device_ip=device.ip_address)

global exit_application
global volume

exit_application = False
volume = 45

def runVolumeAdjustment():  
    while not exit_application:
        device.volume = volume
        time.sleep(0.01)

def runWebServer():
    app.run(host="0.0.0.0", port=80)

def runSystemTrayIcon():
    global exit_application

    Qapp = QApplication(sys.argv)
    
    menu = QMenu()
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(Qapp.quit)

    trayIcon = QSystemTrayIcon(QIcon('static/img/favicon.png'), parent=Qapp)
    trayIcon.setToolTip('Sonos Volume Controller')
    trayIcon.setContextMenu(menu)
    trayIcon.show()

    Qapp.exec_()
    
    exit_application = True  
    sys.exit()

if __name__ == "__main__":
    threading.Thread(target=runVolumeAdjustment, daemon=True).start()
    threading.Thread(target=runSystemTrayIcon, daemon=True).start()
    threading.Thread(target=runWebServer, daemon=True).start()

    while not exit_application:
        time.sleep(0.5)

    sys.exit()