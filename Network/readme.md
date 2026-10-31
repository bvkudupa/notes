![alt text](image.png)

# IPV4

Each IPv4 address is 32 bits, written as four groups of 8 bits (called octets). The dots are just a readable way to separate those groups.
In one 8-bit group, the bit positions have these values:
```
Bit:    1   1   1   1   1   1   1   1
Value: 128  64  32  16   8   4   2   1
```
Those values are powers of 2, from (2^7) down to (2^0). Adding them gives:
```
2⁷ + 2⁶ + 2⁵ + 2⁴ + 2³ + 2² + 2¹ + 2⁰ = 255
```
So an octet can represent values from 0 to 255—that’s 256 possible values. The highest value is 255 because counting starts at zero.

For four octets, the total number of possible combinations is:
```
256 × 256 × 256 × 256 = 256⁴ = 2³² = 4,294,967,296
```

![alt text](image-1.png)

![alt text](image-2.png)

Each entry names the interface and shows its state. UP means the interface is enabled and passing traffic. A DOWN interface is a closed door: its addresses stop answering. The loopback interface reports UNKNOWN instead of UP, which is normal for lo and nothing to worry about.

Real servers often have more doors: a second network card, VPN interfaces, bridges for containers. A DevOps engineer reads this list to learn which networks a machine is connected to, and a door showing DOWN when it should be UP explains many outages in one line.

![alt text](image-3.png)

![alt text](image-4.png)

![alt text](image-5.png)

![alt text](image-6.png)

![alt text](image-7.png)

![alt text](image-8.png)

![alt text](image-9.png)

![alt text](image-10.png)

![alt text](image-11.png)

![alt text](image-12.png)

![alt text](image-13.png)

![alt text](image-14.png)

```
vi gateway-neighbor.txt
root@escbash-lab:~/answers# ip -4 route show default
default via 172.30.0.1 dev eth0 
root@escbash-lab:~/answers# ip route show
default via 172.30.0.1 dev eth0 
172.30.0.0/30 dev eth0 proto kernel scope link src 172.30.0.2 
root@escbash-lab:~/answers# ip neigh
172.30.0.1 dev eth0 lladdr 6e:a4:b5:08:53:0c REACHABLE 
root@escbash-lab:~/answers# 
```

```
root@escbash-lab:~# ip neigh flush all && ip neigh > /root/answers/neigh-before.txt
root@escbash-lab:~# 
root@escbash-lab:~# cd answers/
root@escbash-lab:~/answers# ll
total 28
drwxr-xr-x 2 root root  4096 Oct 30 17:01 ./
drwx------ 5 root root  4096 Oct 30 16:54 ../
-rw------- 1 root root 12288 Oct 30 16:59 .neigh-before.txt.swp
-rw-r--r-- 1 root root    18 Oct 30 16:34 eth0-mac.txt
-rw-r--r-- 1 root root    56 Oct 30 16:54 gateway-neighbor.txt
-rw-r--r-- 1 root root     0 Oct 30 17:01 neigh-before.txt
root@escbash-lab:~/answers# cat neigh-before.txt 
root@escbash-lab:~/answers# 
root@escbash-lab:~/answers# ip neigh
172.30.0.1 dev eth0 lladdr 6e:a4:b5:08:53:0c REACHABLE 
root@escbash-lab:~/answers# arping -c 4 172.30.0.1
ARPING 172.30.0.1 from 172.30.0.2 eth0
Unicast reply from 172.30.0.1 [6E:A4:B5:08:53:0C]  0.646ms
Unicast reply from 172.30.0.1 [6E:A4:B5:08:53:0C]  0.729ms
Unicast reply from 172.30.0.1 [6E:A4:B5:08:53:0C]  0.684ms
Unicast reply from 172.30.0.1 [6E:A4:B5:08:53:0C]  0.684ms
Sent 4 probes (1 broadcast(s))
Received 4 response(s)
root@escbash-lab:~/answers# 
root@escbash-lab:~/answers# 
root@escbash-lab:~/answers# ip neigh
172.30.0.1 dev eth0 lladdr 6e:a4:b5:08:53:0c REACHABLE 
root@escbash-lab:~/answers# ip neigh > /root/answers/neigh-after.txt
root@escbash-lab:~/answers# 
```
![alt text](image-15.png)

# Theoretical OSI model Layers: (This is what used for troubleshooting / Teaching)

* Application | All
* Presentation | People
* Session | Should
* Transport | Try
* Network | New
* Data link | Dominos
* Physical  | Pizza

# Practical TCP/IP model: (This is how internet is programmed)

* Link layer
* Internet layer
* Transport layer
* Application layer

```
mac and arp are assigned to the link layer

ip-address is assigned to the internet layer

tcp and port are assigned to the transport layer

http is assigned to the application layer
```

![alt text](image-16.png)

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

![alt text](image-20.png)

![alt text](image-21.png)

```
getent hosts example.com >/dev/null & ss -upn
nc -u -l 9000 > /root/udp-received.txt &
printf 'hello over udp\n' | nc -u -w1 127.0.0.1 9000
nc -l 9000 > /root/incoming.txt
nc -N 127.0.0.1 9000 < /root/outgoing.txt
```

![alt text](image-22.png)

# DNS:
```
dig example.com A                    # query IPv4 records
dig @1.1.1.1 example.com MX          # query a specific DNS server
dig +short example.com               # show concise results
dig +trace example.com                # follow DNS delegation
dig @hera.ns.cloudflare.com example.com A +norecurse
```
![alt text](image-23.png)

![alt text](image-24.png)

![alt text](image-25.png)

```
root@escbash-lab:~# dig www.github.com

; <<>> DiG 9.18.39-0ubuntu0.24.04.7-Ubuntu <<>> www.github.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8657
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;www.github.com.                        IN      A

;; ANSWER SECTION:
www.github.com.         3564    IN      CNAME   github.com.
github.com.             24      IN      A       140.82.121.3

;; Query time: 0 msec
;; SERVER: 1.1.1.1#53(1.1.1.1) (UDP)
;; WHEN: Sat Oct 31 18:08:47 UTC 2026
;; MSG SIZE  rcvd: 73

```

![alt text](image-26.png)

![alt text](image-27.png)

# When a resolver is running on local machine with port
```
root@escbash-lab:~# dig @127.0.0.1 -p 5353 example.com

; <<>> DiG 9.18.39-0ubuntu0.24.04.7-Ubuntu <<>> @127.0.0.1 -p 5353 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30089
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            17      IN      A       104.20.23.154
example.com.            17      IN      A       172.66.147.243

;; Query time: 0 msec
;; SERVER: 127.0.0.1#5353(127.0.0.1) (UDP)
;; WHEN: Sat Oct 31 18:37:04 UTC 2026
;; MSG SIZE  rcvd: 72

root@escbash-lab:~# 
```