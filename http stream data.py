# gps_api.py
from flask import Flask, jsonify
from pymavlink import mavutil
import threading

app = Flask(__name__)
latest_gps = {}

def mavlink_thread():
    global latest_gps
    mav = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    while True:
        msg = mav.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            latest_gps = {
                'lat': msg.lat / 1e7,
                'lon': msg.lon / 1e7,
                'alt': msg.alt / 1000.0
            }

@app.route('/gps')
def gps():
    return jsonify(latest_gps)

threading.Thread(target=mavlink_thread, daemon=True).start()
app.run(host='0.0.0.0', port=5000)
