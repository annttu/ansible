# Ansible

Collection of ansible roles and playbooks I have found to be useful.

Roles are tested on Debian Jessie.


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

|  name     |   description | example |
| --------- | ------------- | ------- |
| name      |	name for service | someservice | 
| interface | Interface for incoming traffic | eth0 |
| daddr     | Destination address | 10.0.0.1 |
| saddr     | Source address | 10.0.0.0/24 |
| dport     | Destination port | 5555 |
| sport     | source port | 5555 |
| proto     | Protocol, tcp, udp, icmp | tcp |
| chain     | Firewall chain, input, output, forward, input6, output6, forward6 | input |


virsh-console
----

Setup libvirt virtual to have getty on virtual serial console ttyS0.

ldap_users
----

Setup pam authentication against ldap and nscd and nslcd to use ldap.

#### Variables

| name | description | example |
| -- | -- | -- |
| ca_crt | Local path to ca file | /etc/ca.crt |
| ldap_ca | Remote path to ca file | /etc/ldap/ca.crt (default) |
| ldap_server | LDAP server(s) URI | ldaps://ldap.example.com |
| ldap_base | LDAP base dn | dc=example,dc=com |
| login_groups | List of groups allowed to login | sysadmin

fail2ban
----

Install and setup fail2ban.

Currently only ssh service is supported.

#### Variables



Example config

    fail2ban:
      ignored_hosts:
         - 127.0.0.0/8
         - x.y.z.i/24
      bantime: 3600
      maxretry: 10
      destemail: root@localhost
      banaction: iptables-multiport
    
      services:
       - ssh:
         port: ssh
         logpath: /var/log/auth.log
         filter: sshd

nagios-nrpe
-----

Install and configure nagios-nrpe service.
Uses quite a dynamic plugin configuration via host_vars or group_vars. 

#### Variables

| name  | type | description | example | required |
| ----- | ---- | ------------| -------- | ------- |
| server_port | int | Port where nrpe server listens | 5666 ( default ) | no |
| user_groups | list | Groups which nagios user should have | Debian-exim | no |
| plugins | list | a list of plugin entries | see [below](#plugin variables) | yes |
| sudo_plugins | list | a list of plugin entries which requires sudo | see [below](#plugin variables) | no |


#### Plugin variables
| name  | type | description | default | example | required |
| -- | -- | -- | -- | -- |
| name | string | Name of plugin, automatically prefixed with "check\_" | | disk | yes |
| path | string | partial or full path to plugin | /usr/lib/nagios/plugins/check_{{ name }} | /usr/lib/nagios/plugins/check_disk or disk |  no |
| warning | string | warning limit |  | 10% | no |
| critical | string | critical limit | | 20% | no |
| args | string | plugin arguments | | -p /dev/sda1 |

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