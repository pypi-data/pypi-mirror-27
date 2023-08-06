# cordport

Central Office Re-architecture as Datacenter(CORD) network debug tool.

## Usage

```bash
# Get interface relationship from OVS view (default)

ubuntu@linear-fireman:~$ port
1:      vxlan (36:a4:80:4f:15:7f) -> None (None)
2:      fabric (52:54:00:68:0b:79) -> None (None)
19:     tap214953c8-8b (fe:16:3e:af:f6:86) -> 10.0.7.4 (fa:16:3e:af:f6:86)
20:     taped8465f0-ed (fe:16:3e:d6:9a:d2) -> 172.27.0.2 (fa:16:3e:d6:9a:d2)
21:     tapbd3f8054-dc (fe:16:3e:00:fa:da) -> 10.8.1.2 (fa:16:3e:00:fa:da)
22:     tap976feb17-b4 (fe:16:3e:b8:9b:05) -> 172.27.0.3 (fa:16:3e:b8:9b:05)
23:     tapfab23dc0-c9 (fe:16:3e:f0:c0:38) -> 10.0.8.4 (fa:16:3e:f0:c0:38)
24:     tapc1646504-d3 (fe:16:3e:35:1b:31) -> 10.0.6.7 (fa:16:3e:35:1b:31)
25:     tapf832ff2e-ca (fe:16:3e:89:e7:32) -> 172.27.0.4 (fa:16:3e:89:e7:32)

# Get interface relationship from VM view

ubuntu@linear-fireman:~$ port -v vm
10.0.6.7: tapc1646504-d3 (fe:16:3e:35:1b:31)
10.0.7.4: tap214953c8-8b (fe:16:3e:af:f6:86)
10.0.8.4: tapfab23dc0-c9 (fe:16:3e:f0:c0:38)
10.8.1.2: tapbd3f8054-dc (fe:16:3e:00:fa:da)
172.27.0.2: taped8465f0-ed (fe:16:3e:d6:9a:d2)
172.27.0.3: tap976feb17-b4 (fe:16:3e:b8:9b:05)
172.27.0.4: tapf832ff2e-ca (fe:16:3e:89:e7:32)
```

## Installation

```bash
# Install from PyPI
pip install cordport

# Install from GitHub source code
python setup.py install
```


