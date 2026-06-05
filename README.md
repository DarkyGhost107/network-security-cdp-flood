# CDP Flood Attack - Laboratorio de Seguridad de Redes

**Ambiente:** GNS3 (Controlado) | **Herramienta:** Python 3 + Scapy | **Capa OSI:** Capa 2

## Aviso Legal

Este repositorio es de uso **exclusivamente educativo** dentro de un laboratorio controlado (GNS3).
El uso de estas tecnicas en redes reales sin autorizacion expresa es **ilegal**.

## 1. Objetivo del Laboratorio

Demostrar como un atacante puede saturar la tabla de vecinos CDP (Cisco Discovery Protocol) de un switch o router Cisco enviando un gran volumen de paquetes CDP con identificadores de dispositivo y MACs falsas, causando agotamiento de memoria en el dispositivo objetivo.

## 2. Objetivo del Script

`cdp_flood.py` genera y envia continuamente paquetes CDP falsos hacia la direccion multicast `01:00:0c:cc:cc:cc`, haciendo que el switch Cisco registre cientos de vecinos inexistentes hasta agotar su tabla CDP.

## 3. Parametros del Script

| Parametro | Flag | Tipo | Default | Descripcion |
|-----------|------|------|---------|-------------|
| Interfaz | `-i` / `--interface` | str | eth0 | Interfaz de red |
| Cantidad | `-c` / `--count` | int | 500 | Numero de paquetes CDP falsos |
| Delay | `-d` / `--delay` | float | 0.0 | Pausa en segundos entre paquetes |

### Ejemplo de uso

```bash
sudo python3 cdp_flood.py
sudo python3 cdp_flood.py -i eth1 -c 1000
sudo python3 cdp_flood.py -i eth0 -c 2000 -d 0.01
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-cdp-flood/blob/main/screenshots/ejemplo%20de%20uso.png)


## 4. Requisitos

```bash
Python 3.8+
pip install scapy
pip install scapy[complete]
root (sudo)
```

## 5. Funcionamiento del Script

1. Generar MAC fuente aleatoria
2. Generar Device ID aleatorio
3. Construir frame Ethernet con dst=01:00:0c:cc:cc:cc
4. Encapsular LLC + SNAP (OUI Cisco 0x00000c)
5. Agregar cabecera CDPv2 con TLVs: DeviceID, PortID, Platform, Version
6. Enviar via sendp() por la interfaz especificada
7. Repetir N veces

## 6. Topologia de Red (GNS3)
![Texto alternativo](https://github.com/DarkyGhost107/network-security-cdp-flood/blob/main/screenshots/topologia%20MITM%20ARP.png)
### Direccionamiento IP

| Dispositivo | Interfaz | IP | Rol |
|-------------|----------|----|-----|
| Atacante (Kali) | eth0 | 192.168.1.50/24 | Origen del ataque |
| Switch Cisco | Gi0/0 | 192.168.1.1/24 | Objetivo (CDP activo) |

### VLANs

| VLAN | Nombre | Uso |
|------|--------|-----|
| 1 | default | Red de laboratorio |
| 10 | management | Acceso de gestion |

**Comandos para verificar el impacto:**
```
SW# show cdp neighbors
SW# show cdp neighbors detail
SW# show processes cpu | include CDP
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-cdp-flood/blob/main/screenshots/proccess%20cpu.png)
![Texto alternativo](https://github.com/DarkyGhost107/network-security-cdp-flood/blob/main/screenshots/cdp%20neighbor.png)
## 7. Contramedidas

| Contramedida | Comando Cisco IOS | Descripcion |
|---|---|---|
| Deshabilitar CDP globalmente | `no cdp run` | Desactiva CDP en todo el dispositivo |
| Deshabilitar CDP por interfaz | `no cdp enable` | Solo en puertos de acceso hacia usuarios |
| Rate-limiting | `storm-control broadcast level 10` | Limita trafico multicast |

```cisco
interface range GigabitEthernet0/1 - 24
 no cdp enable
interface GigabitEthernet0/25
 cdp enable
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-cdp-flood/blob/main/screenshots/contramedida.png)
## 8. Referencias

- [CVE-2020-3120 - Cisco CDP DoS](https://nvd.nist.gov/vuln/detail/CVE-2020-3120)
- [Scapy Documentation](https://scapy.readthedocs.io/)

---
## 9.Enlaces:
video: https://youtu.be/qo0xjj3oBUU

*Laboratorio de Seguridad de Redes | GNS3 | Uso educativo exclusivo*
