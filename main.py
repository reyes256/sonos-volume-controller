import soco, threading, time, sys, os, socket, platform, icon_rc
from flask import Flask, render_template, request
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

device = soco.discovery.any_soco()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", volume=volume, device_name=device.player_name, host_ip=getPrivateIP())

@app.route("/updateVolume", methods=["POST","GET"])
def updateVolume():
    global volume
    volume = request.form['newVolume']

    return render_template("index.html", songStatus=device.get_current_transport_info()['current_transport_state'], volume=str(volume), device_name=device.player_name, host_ip=getPrivateIP())

@app.route("/pause", methods=["POST","GET"])
def pause():
    songStatus = device.get_current_transport_info()['current_transport_state']

    if songStatus == "PLAYING":
        device.pause()
    elif songStatus == "PAUSED_PLAYBACK":
        device.play()

    return render_template("index.html", volume=str(volume), device_name=device.player_name, host_ip=getPrivateIP())

@app.route("/previous", methods=["POST","GET"])
def previous():
    try:
        device.previous()
    except:
        print("Next song")

    return render_template("index.html", volume=str(volume), device_name=device.player_name, host_ip=getPrivateIP())

@app.route("/next", methods=["POST","GET"])
def next():
    try:
        device.next()
    except:
        print("Previous Song")

    return render_template("index.html", volume=str(volume), device_name=device.player_name, host_ip=getPrivateIP())

global exit_application
global volume

exit_application = False
volume = 35

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
    exitAction = menu.addAction("Exit")
    exitAction.triggered.connect(Qapp.quit)

    openBrowserAction = menu.addAction("Open in browser")
    openBrowserAction.triggered.connect(openBrowser)

    trayIcon = QSystemTrayIcon(QIcon(":static/img/favicon.png"), parent=Qapp)
    trayIcon.setToolTip("Sonos Volume Controller")
    trayIcon.setContextMenu(menu)
    trayIcon.show()

    Qapp.exec_()

    exit_application = True
    sys.exit()

def openBrowser():
    global os_name
    url = f"http://{getPrivateIP()}:80"

    try:
        if os_name == "Windows": 
            os.system(f"start {url}")
        elif os_name == "Linux":
            os.system(f"xdg-open {url}")
        elif os_name == "Darwin":
            os.system(f"open {url}")
    except:
        print("Could not open default browser")

def getPrivateIP():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def getOperatingSystem():
    global os_name
    os_name = platform.system()


if __name__ == "__main__":
    getOperatingSystem()

    threading.Thread(target=runVolumeAdjustment, daemon=True).start()
    threading.Thread(target=runSystemTrayIcon, daemon=True).start()
    threading.Thread(target=runWebServer, daemon=True).start()

    openBrowser()

    while not exit_application:
        time.sleep(0.5)

    sys.exit()