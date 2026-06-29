# dec/31/2016 20:11:18 by RouterOS 6.37.3
# software id = R9VW-5KGZ
#
/ip firewall filter
add action=reject chain=hs-unauth dst-port=80 protocol=tcp reject-with=\
    tcp-reset
add action=passthrough chain=unused-hs-chain comment=\
    "place hotspot rules here" disabled=yes
add action=drop chain=input disabled=yes dst-port=21-23 in-interface=ether1 \
    protocol=tcp
add action=drop chain=input disabled=yes dst-port=57 in-interface=ether1 \
    protocol=udp
add action=fasttrack-connection chain=forward connection-state=\
    established,related disabled=yes
add action=accept chain=forward connection-state=established,related \
    disabled=yes
