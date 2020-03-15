#!/usr/bin/python3

import time
import logging

from ubxlib.server import GnssUBlox
from ubxlib.frame import UbxAckAck
from ubxlib.ubx_cfg_tp5 import UbxCfgTp5Poll
from ubxlib.ubx_upd_sos import UbxUpdSosPoll, UbxUpdSosAction


FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('gnss_tool')
logger.setLevel(logging.DEBUG)


msg_stop = bytearray.fromhex('06 04 04 00 00 00 08 00')    # stop
msg_cold_start = bytearray.fromhex('06 04 04 00 FF FF 01 00')  # Cold Start
msg_mon_ver = bytearray.fromhex('0A 04 00 00')  # MON-VER
msg_cfg_port_poll = bytearray.fromhex('06 00 01 00 01')  # UBX-CFG-PRT poll
msg_nav_status_poll = bytearray.fromhex('01 03 00 00')

# msg_cfg_port_uart_9600 = bytearray.fromhex('06 00 14 00 01 00 00 00 c0 08 00 00 80 25 00 00 07 00 01 00 00 00 00 00')
msg_cfg_port_uart_115200 = bytearray.fromhex('06 00 14 00 01 00 00 00 c0 08 00 00 00 c2 01 00 07 00 01 00 00 00 00 00')

msg_upd_sos_save = bytearray.fromhex('09 14 04 00 00 00 00 00')
msg_upd_sos_clear = bytearray.fromhex('09 14 04 00 01 00 00 00')

r = GnssUBlox('/dev/ttyS3')
r.setup()

# Remove backup
m = UbxUpdSosAction()
m.f_cmd = 1
m.f_res1_1 = 0
m.f_res1_2 = 0
m.f_res1_3 = 0
m.pack()
print(m)
print(m.f_cmd)

r.expect(UbxAckAck.CID)
r.send(m)
r.wait()

for i in range(0, 1):
    print(f'***** {i} ***********************')

    logger.debug('getting SOS state')
    msg_upd_sos_poll = UbxUpdSosPoll()
    res = r.poll(msg_upd_sos_poll)
    if res:
        print(f'SOS state is {res.fields["response"]}')

    msg_cfg_tp5_poll = UbxCfgTp5Poll()
    res = r.poll(msg_cfg_tp5_poll)
    print(res)

    res.f_flags |= 1
    # res.fields['flags'] = 1 + 2 + 16    # Active, lock to GPS, isLength
    res.f_freqPeriod = 1000     # 1 us = kHz
    res.f_pulseLenRatio = 500   # 500 ns = 50% duty cycle
    print(res)
    res.pack()

    r.expect(UbxAckAck.CID)
    r.send(res)
    r.wait()

    time.sleep(0.87)

r.cleanup()
