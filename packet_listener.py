import scapy.all as scapy
from scapy_http import http

def get_packet(interface):
    scapy.sniff(iface=interface,store=False,prn=analize)   #people say 'prn = callback function'

def analize(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].laod)
get_packet("wlan0")

