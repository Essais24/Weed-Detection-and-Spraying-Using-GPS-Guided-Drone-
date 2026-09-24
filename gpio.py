import pigpio
import tkinter as tk

pi = pigpio.pi("10.109.193.105", 8891)

GPIO_PIN = 13  # MUST be 12, 13, 18, or 19 for hardware PWM

if not pi.connected:
    print("❌ Could not connect to Raspberry Pi. Is pigpiod running?")
    exit()

def turn_on():
    pi.write(GPIO_PIN, 1)

def turn_off():
    pi.write(GPIO_PIN, 0)
    pi.hardware_PWM(GPIO_PIN, 0, 0)  # stop PWM if running

def buzz():
    frequency = 1000      # 1 kHz tone
    duty_cycle = 500000   # 50% (range: 0–1,000,000)
    pi.hardware_PWM(GPIO_PIN, frequency, duty_cycle)

def on_close():
    pi.hardware_PWM(GPIO_PIN, 0, 0)
    pi.write(GPIO_PIN, 0)
    pi.stop()
    root.destroy()

root = tk.Tk()
root.title("GPIO Buzzer Controller")

on_btn = tk.Button(root, text="Turn ON", command=turn_on,
                   width=20, height=2, bg="green", fg="white")

off_btn = tk.Button(root, text="Turn OFF", command=turn_off,
                    width=20, height=2, bg="red", fg="white")

buzz_btn = tk.Button(root, text="Buzz (1 kHz)", command=buzz,
                     width=20, height=2, bg="orange", fg="black")

on_btn.pack(pady=8)
buzz_btn.pack(pady=8)
off_btn.pack(pady=8)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
