#!/usr/bin/python -u

import lifx
import socket
import sys
from time import sleep

print("Initializing light")
light = lifx.get_lights()[0]
print(light.hue)
print(light.saturation)
print(light.brightness)
print(light.kelvin)
print("Light done")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print("Socket created")

try:
    sock.bind(("localhost",5432))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg))
    sys.exit()

print("Socket bind complete")

sock.listen(1)
print("Socket now listening")
try:
    while 1:
        light = lifx.get_lights()[0]
        power_status = light.power
        conn, addr = sock.accept()
        print("Connected to client")
        conn.send(str(light.power))

        while 1:
            print("%s,%s,%s,%s" % (light.hue, light.saturation, light.brightness, light.kelvin))
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            print("Got data: '%s'" % data)
            info = data.split(":")
            if data == "on":
                print("Turning on lights!")
                light.set_power(True)
                power_status = True
            elif data == "off":
                print("Turning off lights!")
                light.set_power(False)
                power_status = False
            elif info[0] == "hue":
                hue = float(info[1])
                print("Setting hue to %d" % hue)
                light.set_state({"color": "hue:%f" % hue})
            elif info[0] == "saturation":
                saturation = float(info[1])
                print("Setting saturation to %d" % saturation)
                light.set_state({"color": "saturation:%f" % saturation})
            elif info[0] == "brightness":
                brightness = float(info[1])
                print("Setting brightness to %d" % brightness)
                light.set_state({"color": "brightness:%f" % brightness})
            elif info[0] == "kelvin":
                kelvin = int(info[1])
                print("Setting kelvin to %d" % kelvin)
                light.set_state({"color": "kelvin:%d" % kelvin})
            elif data == "default":
                light.set_color(0,0,1.0,1,3200)
            elif data == "mood":
                light.set_color(320,0.7,0.8,1)
            elif data == "toggle":
                #light = lifx.get_lights()[0]
                print("Toggle: " + str(power_status))

                if power_status:
                    light.set_power(False)
                    power_status = False
                else:
                    light.set_power(True)
                    power_status = True
            elif data == "status":
                print light.hue, light.saturation, light.brightness, light.kelvin
            light = lifx.get_lights()[0]
        conn.close()
finally:
    sock.close()
