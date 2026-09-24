import requests
import time

url = "http://192.168.1.208:5011/target"  # replace with Pi's IP
data = {
  "lat": 12.3456,
  "lon": 78.9012,
  "alt": 60
}
try:
    r = requests.post(url, json=data, timeout=2)
    if r.ok:
        print("[INFO] Sent target GPS to Pi successfully.")
    else:
        print(f"[WARN] Failed to send target GPS: {r.status_code}")
except Exception as e:
    print(f"[ERROR] Could not contact Pi: {e}")