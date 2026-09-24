from flask import Flask, jsonify
from pymavlink import mavutil
import threading
import time
import math

app = Flask(__name__)
latest_gps = {}
latest_yaw = None

def mavlink_thread():
    global latest_gps, latest_yaw
    print("[MAVLINK] Starting MAVLink thread...")

    try:
        # Connect to MAVLink on UDP port
        mav = mavutil.mavlink_connection('udp:0.0.0.0:14552')

        while True:
            msg = mav.recv_match(blocking=True, timeout=5)
            if msg is None:
                print("[MAVLINK] No message received... retrying.")
                continue

            msg_type = msg.get_type()

            if msg_type == 'ATTITUDE':
                latest_yaw = msg.yaw  # radians, 0 = North
                print(f"[MAVLINK] Received yaw: {math.degrees(latest_yaw):.2f}°")

            elif msg_type == 'GLOBAL_POSITION_INT':
                gps_data = {
                    'lat': msg.lat / 1e7,
                    'lon': msg.lon / 1e7,
                    'alt': msg.relative_alt,
                    'yaw_deg': math.degrees(latest_yaw) if latest_yaw is not None else None
                }
                latest_gps = gps_data
                print(f"[MAVLINK] Received GPS + Yaw: {gps_data}")

            time.sleep(0.01)  # slight delay to avoid busy loop

    except Exception as e:
        print(f"[MAVLINK ERROR] {e}")


@app.route('/gps')
def gps():
    if latest_gps:
        return jsonify(latest_gps)
    else:
        return jsonify({"status": "waiting", "yaw_deg": None})

# Start MAVLink receiver in background
threading.Thread(target=mavlink_thread, daemon=True).start()

# Start Flask server
print("[FLASK] Starting server on http://0.0.0.0:5000")
app.run(host='0.0.0.0', port=5000)
