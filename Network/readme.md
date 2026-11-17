# Network learning path

Follow the lessons in order to build up from basic network concepts to practical troubleshooting. A lesson links to the relevant section of the notes; **Notes coming soon** marks a topic that does not have a guide yet.

## 1. Foundations

1. **What is a network** — [Network layers and the TCP/IP model](transport-and-sockets/readme.md#network-layers)
2. **IP addresses** — [IPv4 and IPv6](addressing-and-routing/readme.md#ipv4)
3. **Interfaces** — [Interfaces and addresses](addressing-and-routing/readme.md#interfaces-and-addresses)
4. **Subnets and CIDR** — [Subnets and CIDR](addressing-and-routing/readme.md#subnets-and-cidr)
5. **MAC addresses and ARP** — [MAC addresses, ARP, and the neighbor table](addressing-and-routing/readme.md#mac-addresses-arp-and-the-neighbor-table)
6. **The layers model** — [Network layers](transport-and-sockets/readme.md#network-layers)

## 2. Transport and application protocols

7. **Ports and sockets** — [TCP and UDP sockets](transport-and-sockets/readme.md#tcp-and-udp-sockets)
8. **TCP** — [TCP connection setup, reliability, and close](transport-and-sockets/readme.md#tcp-connection-setup-reliability-and-close)
9. **UDP** — [TCP and UDP sockets](transport-and-sockets/readme.md#tcp-and-udp-sockets)
10. **Netcat** — [Testing TCP and UDP with netcat](transport-and-sockets/readme.md#tcp-and-udp-sockets)
11. **DNS basics** — [Querying DNS](dns/readme.md#querying-dns)
12. **DNS record types** — [Record types](dns/readme.md#record-types)
13. **Run your own DNS** — [dnsmasq as a local resolver](dns/readme.md#dnsmasq-as-a-local-resolver)
14. **HTTP** — [HTTP requests and status codes](http-and-nginx/readme.md#http-requests-and-status-codes)
15. **HTTP headers, redirects, and JSON** — [Inspecting headers and following redirects](http-and-nginx/readme.md#http-requests-and-status-codes) (JSON notes coming soon)
16. **Serve a website with Nginx** — [Nginx server blocks](http-and-nginx/readme.md#nginx-server-blocks)
17. **TLS and HTTPS** — [TLS connection flow](tls-and-certificates/readme.md#tls-connection-flow)
18. **Make your own certificates** — [Create a root CA and issue a site certificate](tls-and-certificates/readme.md#create-a-root-ca-and-issue-a-site-certificate)

## 3. Routing, services, and troubleshooting

19. **Routing and gateways** — [Default gateway and route selection](addressing-and-routing/readme.md#default-gateway-and-route-selection)
20. **NAT** — [NAT and port forwarding](nat/readme.md)
21. **DHCP** — [DHCP and the DORA exchange](dhcp/readme.md#the-dora-exchange)
22. **Firewall basics** — [Packet paths and chains](firewall/readme.md#packet-paths-and-chains)
23. **Firewall practice** — [Firewall practice walkthroughs](firewall/readme.md#practice-walkthroughs)
24. **tcpdump** — [Capture and filter packets](tcpdump/readme.md)
25. **SSH and tunnels** — Notes coming soon
26. **Reverse proxy and load balancing** — [Nginx server blocks](http-and-nginx/readme.md#nginx-server-blocks) (reverse proxy notes coming soon)
27. **Scanning with nmap** — Notes coming soon
28. **The debugging playbook** — Start with [layer-specific diagnostic tools](transport-and-sockets/readme.md#network-layers), then follow the [route decision](addressing-and-routing/readme.md#default-gateway-and-route-selection) and inspect packets with [tcpdump](tcpdump/readme.md)
29. **Latency and bandwidth** — Notes coming soon
30. **Project: fix the broken server** — Project notes coming soon

## How the lessons connect

- **Local delivery:** [IP addresses](addressing-and-routing/readme.md#ipv4) are assigned to [interfaces](addressing-and-routing/readme.md#interfaces-and-addresses); [subnets](addressing-and-routing/readme.md#subnets-and-cidr) tell you which destinations are local, and [ARP](addressing-and-routing/readme.md#mac-addresses-arp-and-the-neighbor-table) finds the local MAC address.
- **Getting to a service:** the [route and gateway](addressing-and-routing/readme.md#default-gateway-and-route-selection) select the path; [ports and sockets](transport-and-sockets/readme.md#tcp-and-udp-sockets) identify the destination service; [TCP](transport-and-sockets/readme.md#tcp-connection-setup-reliability-and-close) or [UDP](transport-and-sockets/readme.md#tcp-and-udp-sockets) carries the traffic.
- **Using a website:** [DNS](dns/readme.md) finds an address, [HTTP and Nginx](http-and-nginx/readme.md) exchange web requests, and [TLS](tls-and-certificates/readme.md) protects HTTPS connections.
- **Operating and debugging:** [DHCP](dhcp/readme.md) provides network configuration, [NAT](nat/readme.md) translates addresses, [firewall rules](firewall/readme.md) filter packets, and [tcpdump](tcpdump/readme.md) lets you observe what actually happened.
