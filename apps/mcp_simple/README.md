# MCP hello world: direct Ethernet

Connect the FRDM-MCXN947 to the PC with an Ethernet cable. From the workspace root in PowerShell:

```powershell
. .\.venv\Scripts\Activate.ps1
$env:ZEPHYR_SDK_INSTALL_DIR = 'C:/Users/luchi/zephyr-sdk-1.0.1'  # Change for your machine
$ethernetConfig = (Resolve-Path 'apps/mcp_simple/direct-ethernet.conf').Path
$westRoot = (python -m west topdir).Trim()
$samplePath = Join-Path $westRoot 'zephyr/samples/net/mcp/mcp_server_hello_world'
python -m west build -p always -b frdm_mcxn947/mcxn947/cpu0 $samplePath -d builds/mcp-simple -- "-DEXTRA_CONF_FILE=$ethernetConfig"
python -m west flash -d builds/mcp-simple
```

To test the server with FastMCP, run the following commands and watch the serial monitor. The client lists the tools, turns the LED off and on, and waits about 12 seconds for the delayed response:

```powershell
python -m pip install -r requirements.txt
python apps/mcp_simple/mcp_client.py
```

## Direct Ethernet connection without router

The provided example expects devices with an assigned IP address. On a typical home network, the router acts as the DHCP server, and a new device in the network can ask for an IP configuration automatically. For a direct PC-to-board Ethernet connection without a DHCP server, Windows may assign the PC a link-local address. The board uses a static address configured at build time in [direct-ethernet.conf](direct-ethernet.conf).

In order to identify the appropiate configuration values, one should inspect the Ethernet port of the host machine through

```powershell
Get-NetIPConfiguration
Get-NetIPAddress -AddressFamily IPv4 | Format-Table IPAddress, PrefixLength
```

My computer specifies its IP address to be `169.254.176.189`, and prefix length of `16`. The latter is linked to the value we should assign to the subnet mask, and it indicates the number of bits used to identify the network.

```text
169     . 254       . 176     . 189
10101001  11111110  10110000  10111101
└─ 8 ──┘ └── 8 ──┘
└─── 16 bits ────┘
```

With this information, our subnet mask necessarily needs to use all 16 bits `255.255.0.0`. Since our device needs to be part of the same network, its IP address will start with `169.254.x.x`, and since it must be different than that of the host machine, then a plausible value is `169.254.176.190`.
