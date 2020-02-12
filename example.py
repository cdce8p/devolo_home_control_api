import logging

from devolo_home_control_api.homecontrol import HomeControl
from devolo_home_control_api.mydevolo import Mydevolo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

user = "username"
password = "password"


class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f'{self.name} got message "{message}"')


mydevolo = Mydevolo()
mydevolo.user = user
mydevolo.password = password

gateway_id = mydevolo.gateway_ids[0]
homecontrol = HomeControl(gateway_id=gateway_id)

for device in homecontrol.devices:
    homecontrol.devices[device].subscriber = Subscriber(device)
    homecontrol.mprm.publisher.register(device, homecontrol.devices[device].subscriber))
