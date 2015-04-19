# Ansible

Collection of ansible roles and playbooks I have found to be useful.

## Credits
 - Antti Jaakkola (Annttu)
 - Joonas Järveläinen (jonttu)
 - Veli-Matti Leppänen (velzi)


Modules
===

Ferm
---

Combined with ferm_service module, ferm provides easy to use firewall.

#### Variables

Currently none.

Ferm_service
---

This module opens ports to ferm-firewall. Useful when service requires open ports.

#### Usage

Add to role's meta/main.yml

     dependencies:
      - { role: ferm_service, name: someservice, chain: input, saddr: "source-ip-here", dport: someport, proto: tcp }

#### Variables

| name  |   description | example |
|-------|---------------| - |
| name  |	name for service | someservice | 
| interface | Interface for incoming traffic | eth0
| daddr | Destination address | 10.0.0.1 |
| saddr | Source address | 10.0.0.0/24 |
| dport | Destination port | 5555 |
| sport | source port | 5555 |
| proto | Protocol, tcp, udp, icmp| tcp |
| chain | Firewall chain, input, output, forward, input6, output6, forward6 | input |


virsh-console
----

Setup libvirt virtual to have getty on virtual serial console ttyS0.


License
===

The MIT License (MIT)

Copyright (c) 2015 Antti Jaakkola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.