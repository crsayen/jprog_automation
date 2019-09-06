import time
import subprocess, datetime, socket
import sys, threading, os
import can

lastCommand = "stop"
EXCHANGE_TIMEOUT = 60
newlog = -1

def rxcmd(sock, cmd):
    try:
        data_bytes, address = sock.recvfrom(64)
    except Exception as e:
        print(e)
        return False
    if data_bytes is None or data_bytes.decode("utf-8") != cmd:
        print("error: didn't receive '{}' command in time".format(cmd))   
        return False
    sock.sendto(bytes("ok", "utf-8"), address)
    return True

def main(sock):
    global lastCommand
    global newlog
    while 1:
        print("starting")
        with open("/var/lib/cloud9/crackerLogs/seedkeylog", "r") as f:
            if newlog == -1:
                for line in f:
                    newlog += 1
        while not rxcmd(sock, "proceed"): continue
        with open("/var/lib/cloud9/crackerLogs/seedkeylog", "a+") as f:
            for s in ["100","62C 01 40 00 00 00 00 00 00","13FFE060","10244060 00","102C6060 00 33 0B 00 96 87","103BC060 00","103D6060 01","10444060 00 00","10448060 00 00 00 00","1045C060 40","10774060 00","1084A060 05","10A04060 00","10ACE060 1E 00 00 00 00 00 00 00","103DA060 00","10812060 00","10B0A060 00 1E 04","13FFE060","1084A060 05","10244060 02","103D6060 01","10ACE060 1E 00 10 00 00 00 00 00","10B0A060 00 2B 04","10ACE060 2B 00 00 00 00 00 00 00","10B0A060 00 16 04","10B0A060 00 19 04","10B0A060 00 0E 04","13FFE060","13FFE060"]:
                c = s.split(" ")
                s_id = '0' + c[0] if len(c[0]) % 2 !=0 else c[0]
                s_data = "".join(c[1:]) if len(c) != 1 else None
                b_data = bytes.fromhex(s_data) if s_data else None
                msg = can.Message(
                    arbitration_id=int.from_bytes(bytes.fromhex(s_id), byteorder='big'),
                    extended_id=len(s_id) > 4,
                    data=b_data,
                    channel="can0",
                )
                bus.send(msg)
            line = doExchange()
            if line is not None:
                f.write(line)

def doExchange():
    global lastCommand
    global newlog
    noSeed = True
    i = 0
    start = time.time()
    while noSeed:
        i+=1
        try:
            msg = bus.recv(0.5)
        except Exception:
            continue
        if msg is None:
            continue
        if msg.data.hex() == '0227010000000000':
            seed = hex(newlog)[2:]
            while len(seed) < 4:
                seed = '0' + seed
            data = '046701{}aaaaaa'.format(seed)
        elif msg.data.hex() == 'fe01280000000000':
            data = '0168aaaaaaaaaaaa'
        elif msg.data.hex() == '021acb0000000000':
            data = '065acb0164ec65aa'
        elif msg.data.hex() == '021a900000000000':
            data = '10135a9031474e53'
        elif msg.data.hex() == '3000000000000000':
            data = '214b484b43334752'
            msg = can.Message(
                arbitration_id=0x64c,
                extended_id=False,
                data=bytes.fromhex(data),
                channel="can0",
            )
            data = '22323333313531AA'
        elif msg.data.hex()[:6] == "042702":
            newlog +=1
            return "\n{} {}".format(seed,msg.data.hex()[6:10])
        msg = can.Message(
            arbitration_id=0x64c,
            extended_id=False,
            data=bytes.fromhex(data),
            channel="can0",
        )
        bus.send(msg)
        if time.time() - start > EXCHANGE_TIMEOUT:
            return None
 
if __name__ == "__main__":
    bus = can.interface.Bus(bustype="socketcan", channel="can0")
    path = "/var/lib/cloud9/crackerLogs/"
    address = ("0.0.0.0", 11000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(60)
    sock.bind(address)
    main(sock)