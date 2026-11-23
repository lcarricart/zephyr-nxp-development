# Editable MCP server sample

This is a copy of Zephyr's `samples/net/mcp/mcp_server_hello_world` from the NXP fork at commit `1b3f4f14ad2002beb743dba17b455a1f0c688639`. Edit `src/main.c` to change the server and its tools. `prj.conf` contains the sample's Zephyr configuration; `direct-ethernet.conf` overrides its default DHCP setup for a direct PC connection.

From the workspace root in PowerShell, with the FRDM-MCXN947 connected over USB and Ethernet:

```powershell
. .\.venv\Scripts\Activate.ps1
$env:ZEPHYR_SDK_INSTALL_DIR = 'C:/Users/luchi/zephyr-sdk-1.0.1'  # Change for your machine
$ethernetConfig = (Resolve-Path 'apps/samples_mcp/direct-ethernet.conf').Path
python -m west build -p always -b frdm_mcxn947/mcxn947/cpu0 apps/samples_mcp -d builds/samples_mcp -- "-DEXTRA_CONF_FILE=$ethernetConfig"
python -m west flash -d builds/samples_mcp
```

The board is configured as `169.254.176.190/16`, serving `http://169.254.176.190:8080/mcp`. Adjust `direct-ethernet.conf` if the PC's Ethernet address or subnet requires it; rebuild and flash after changing it. To use the sample's default DHCP configuration on a network with a DHCP server, rebuild pristine without the `EXTRA_CONF_FILE` argument.

The tools are `led_control` and `delayed_response`. Use the clients in `apps/mcp_simple` to interact with them, and open the MCU-Link serial port at 115200 baud, 8N1 to see the server logs. The original sample uses a test random generator and plain HTTP; it is a demonstration configuration.
