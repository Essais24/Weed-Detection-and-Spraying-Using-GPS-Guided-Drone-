from pymavlink import mavutil
import time

print("Connecting to MAVLink on udp:0.0.0.0:14552...")
mav = mavutil.mavlink_connection('udp:0.0.0.0:14552')

print("Waiting for messages...")

while True:
    msg = mav.recv_match(blocking=True, timeout=5)
    if msg:
        print("✅ MAVLink message received!")
    else:
        print("❌ No message received in the last 5 seconds.")
    time.sleep(1)
