import pigpio

pi = pigpio.pi("192.168.1.81")  # Replace with your Pi's IP

if not pi.connected:
    print("❌ Could not connect to Raspberry Pi at 192.168.1.81. Is pigpiod running?")
    exit()

pi.set_mode(26, pigpio.OUTPUT)
pi.write(26, 0)  # Turn GPIO 26 ON
pi.stop()
