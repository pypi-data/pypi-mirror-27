import sys
from scapy.all import sniff, ARP, dhcp_request

ip_list = set()

def test_callback(pkt):
    if ARP in pkt:
        ip_list.add(pkt.sprintf("%ARP.psrc%"))


print("Performing dhcp request")
test2 = dhcp_request()
print("DHCP request done")
print(test2)

# test = sniff(store=0, prn=test_callback, count=2000)

# print(ip_list)