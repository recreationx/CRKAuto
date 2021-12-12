from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import time

class AdbInterface:
    def __init__(self, ip, port):
        self.device = AdbDeviceTcp(ip, port, default_transport_timeout_s=9.)
        self.signer = None

    def load_rsa(self):
        adbkey = 'key'
        with open(adbkey) as f:
            priv = f.read()
        with open(adbkey + '.pub') as f:
            pub = f.read()
        self.signer = PythonRSASigner(pub, priv)

    def get_device(self):
        return self.device
    
    def connect(self):
        if self.signer is None:
            self.load_rsa()
        self.device.connect(rsa_keys=[self.signer], auth_timeout_s=0.1)

    def send_touch(self, coordinates):
        self.device.shell('input tap {} {}'.format(coordinates[0], coordinates[1]))
    
    def send_swipe(self, coordinates):
        self.device.shell('input swipe {} {} {} {}'.format(coordinates[0], coordinates[1], coordinates[2], coordinates[3]))

    def hold(self, coordinates):
        self.device.shell('input swipe {} {} {} {}'.format(coordinates[0], coordinates[1], coordinates[0], coordinates[1]))
    
class BaseBuilding:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.purchase_item = None
        self.constants = {
            'LEVEL_1': (1611, 360), # LEVEL 1 ITEM
            'LEVEL_2': (1611, 692), # WIP
            'LEVEL_3': (1611, 999), # WIP
            'LEVEL_4': (1328, 275), # WIP
            'NEXT': (1025, 525), # SHOWS NEXT PAGE
        }

    def __repr__(self):
        return f"{self.name}: Level {self.level}"

    def set_purchase_item(self, item):
        self.purchase_item = item

    def get_purchase_item(self):
        return self.purchase_item

    def do_purchase(self, adb):
        if self.level in ('LEVEL_1', 'LEVEL_2', 'LEVEL_3'):
            adb.hold(self.constants[self.level])
            adb.send_touch(self.constants['NEXT'])  
            time.sleep(3)

adb = AdbInterface('127.0.0.1', 62001)
adb.connect()
device = adb.get_device()

building_list = [BaseBuilding('Smithy', 'LEVEL_3'), BaseBuilding('Jammery', 'LEVEL_2')]

while True:
    for building in building_list:
        building.do_purchase(adb)
