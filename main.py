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
        self.device.shell('input swipe {} {} {} {} 3000'.format(coordinates[0], coordinates[1], coordinates[2], coordinates[3]))

    def hold(self, coordinates):
        self.device.shell('input swipe {} {} {} {} 2000'.format(coordinates[0], coordinates[1], coordinates[0], coordinates[1]))
    
class BaseBuilding:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.purchase_item = None
        self.constants = {
            'LEVEL_1': (1611, 360), # LEVEL 1 ITEM
            'LEVEL_2': (1611, 692), # WIP
            'LEVEL_3': (1611, 984), # WIP
            'LEVEL_4': (1611, 360), # WIP
            'SWIPE_UP': (1552, 1053, 1552, 750),
            'NEXT': (1025, 525), # SHOWS NEXT PAGE
        }

    def __repr__(self):
        return f"{self.name}: Level {self.level}"

    def set_purchase_item(self, item):
        self.purchase_item = item

    def get_purchase_item(self):
        return self.purchase_item

    def do_purchase(self, adb):
        if self.level == 'LEVEL_0':
            pass
        if self.level in ('LEVEL_1', 'LEVEL_2', 'LEVEL_3'):
            adb.hold(self.constants[self.level])
            adb.send_touch(self.constants['NEXT'])  
            time.sleep(2)
        elif self.level in ('LEVEL_4', 'LEVEL_5', 'LEVEL_6'):
            adb.send_swipe(self.constants['SWIPE_UP'])
            adb.hold(self.constants['LEVEL_3'])
            adb.send_touch(self.constants['NEXT'])
            time.sleep(2)

adb = AdbInterface('127.0.0.1', 62001)
adb.connect()
device = adb.get_device()

building_list = [
    BaseBuilding('Smithy', 'LEVEL_3'),
    BaseBuilding('Smithy', 'LEVEL_4'), 
    BaseBuilding('Jammery', 'LEVEL_2'),
    BaseBuilding('Carpentry Shop', 'LEVEL_1'),
    BaseBuilding('Bakery', 'LEVEL_1'),
    BaseBuilding('Jampie Diner', 'LEVEL_1'),
    BaseBuilding('Artisans Workshop', 'LEVEL_1'),
    BaseBuilding('Lumberjacks Lodge', 'LEVEL_1'),
    BaseBuilding('Lumberjacks Lodge', 'LEVEL_1'),
    BaseBuilding('Jellybean Farm', 'LEVEL_1'),
    BaseBuilding('Sugar Quarry', 'LEVEL_1'),
    BaseBuilding('Sugar Quarry', 'LEVEL_1'),
    BaseBuilding('Windmill', 'LEVEL_1'),
    BaseBuilding('Jellyberry Orchard', 'LEVEL_1')
]

while True:
    for building in building_list:
        building.do_purchase(adb)
