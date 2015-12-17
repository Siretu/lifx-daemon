import lifx_token
import json
import requests

api_url = "https://api.lifx.com/v1/lights/all"


class Light:
    def __init__(self, js):
        self.data = js
        self.brightness = js["brightness"]
        self.hue = js["color"]["hue"]
        self.saturation = js["color"]["saturation"]
        self.kelvin = js["color"]["kelvin"]
        self.power = js["power"] == "on"

    def set_state(self, data):
        headers = {'Authorization': 'Bearer %s' % lifx_token.token,
                   'Accept': 'application/json',
                   'Content-type': 'application/json'}
        r = requests.put(api_url + "/state", json=data, headers=headers)
        print "Setting state: %s" % str(r.text)

    def set_power(self, power):
        status = "off"
        if power:
            status = "on"
        data = {"power": status,
                "duration": 0.0}
        self.set_state(data)

    def set_color(self, hue, saturation, brightness, duration, kelvin = -1):
        color = "hue:%f saturation:%f brightness:%f" % (hue, saturation, brightness)
        if kelvin != -1:
            color += " kelvin:%d" % kelvin
        print "Setting color: %s" % color
        data = {"color": color,
                "duration": duration}
        self.set_state(data)


def get_lights():
    headers = {'Authorization': 'Bearer %s' % lifx_token.token}
    response = requests.get(api_url, headers=headers)
    return [Light(x) for x in response.json()]
    
if __name__ == "__main__":
    print(get_lights())
