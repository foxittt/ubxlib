from ubxlib.frame import UbxFrame, UbxCID
from ubxlib.types import Fields, CH


class UbxMonVer_(UbxFrame):
    CID = UbxCID(0x0A, 0x04)
    NAME = 'UBX-MON-VER'


class UbxMonVerPoll(UbxMonVer_):
    NAME = UbxMonVer_.NAME + '-POLL'

    def __init__(self):
        super().__init__()


class UbxMonVer(UbxMonVer_):
    def __init__(self):
        super().__init__()

        # fields defined in unpack as they are dynamic

    def unpack(self):
        # Dynamically build fields based on message length
        self.f = Fields()
        self.f.add(CH(30, 'swVersion'))
        self.f.add(CH(10, 'hwVersion'))

        extra_length = len(self.data) - 40
        extra_info = int(extra_length / 30)
        for i in range(extra_info):
            self.f.add(CH(30, f'extension_{i}'))

        super().unpack()
