# NXP Zephyr development

## Current local layout

```text
zephyr-nxp-development/
├── .venv/                       Python virtual environment
├── .west/config                 west workspace configuration
├── .vscode/settings.json        VS Code settings
├── zephyr/                      Zephyr repository and west manifest
├── modules/hal/
│   ├── cmsis/
│   ├── cmsis_6/
│   └── nxp/
├── apps/
│   ├── README.md
│   ├── mcp_simple/                MCP configuration and client test
│   └── hello_world/
│       ├── CMakeLists.txt
│       ├── prj.conf
│       └── src/main.c
└── builds/hello_world/          generated build files
```

`zephyr/` tracks the `nxp/main` branch of [nxp-upstream/zephyr](https://github.com/nxp-upstream/zephyr) in the local `nxp-main` branch. Its `origin` remote points to the main Zephyr project and its `nxp` remote points to the NXP fork. The checkout and module directories are separate Git repositories. The workspace
root and `apps/` are ordinary directories. west uses `zephyr/west.yml` as its manifest. The board target is `frdm_mcxn947/mcxn947/cpu0`.

## Set up a new Windows computer

The project-owned [west.yml](west.yml) pins the NXP Zephyr commit and imports its module manifest. A fresh west workspace puts this repository beside the `zephyr` and `modules` directories. The steps below assume this repository and its manifest have been published first.

1. Install Python 3.12, Git, CMake, Ninja, gperf, devicetree compiler, and Zephyr SDK 1.0.1 (with the ARM toolchain), following the [Zephyr setup instructions](https://docs.zephyrproject.org/latest/develop/getting_started/index.html). Install NXP LinkServer to flash the FRDM-MCXN947.
2. In PowerShell, create a workspace and clone this repository:

   ```powershell
   mkdir zephyr-workspace
   cd zephyr-workspace
   git clone https://github.com/lcarricart/zephyr-nxp-development.git
   cd zephyr-nxp-development
   py -3.12 -m venv .venv
   . .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m west init -l .
   python -m west update
   python -m pip install @((python -m west packages pip) -split ' ')
   ```

3. Set the SDK path for your machine and connect the board's J17 USB port:

   ```powershell
   $env:ZEPHYR_SDK_INSTALL_DIR = 'C:/path/to/zephyr-sdk-1.0.1'
   ```

Run the build commands below from the project repository. For the MCP example, follow [apps/mcp_simple/README.md](apps/mcp_simple/README.md).

Your existing `C:/zephyr-nxp-development` workspace still uses `zephyr/west.yml` directly, with `zephyr` and `modules` inside the repository directory. It has not been migrated to the fresh-clone layout above. Both manifests select the same Zephyr commit and module revisions for the verified MCP build.

## Build and flash

From the workspace root:

```powershell
.\.venv\Scripts\Activate.ps1
$env:ZEPHYR_SDK_INSTALL_DIR = 'C:/path/to/zephyr-sdk'
west build -p always -b frdm_mcxn947/mcxn947/cpu0 apps/hello_world -d builds/hello_world
west flash -d builds/hello_world
```

The serial console uses 115200 baud, 8 data bits, no parity, and 1 stop bit. The
starter application prints `Hello from the FRDM-MCXN947!`.

The current workspace also configures ccache through an absolute path in
`.west/config`. It is optional; if installed on the new computer, configure its
new path with:

```powershell
west config build.cmake-args '-DCCACHE=C:/path/to/ccache.exe'
```


## Zephyr documentation MCP server

Add this to the MCP configuration of your client (the file location and syntax
depend on the client):

```json
{
  "mcpServers": {
    "zephyr-docs": {
      "url": "https://zephyrproject.mcp.kapa.ai"
    }
  }
}
```

This server provides Zephyr documentation and project information. Building and
flashing use the local Zephyr tools and the runner for your board. See
`zephyr/doc/develop/tools/kapa_ai.rst` for client alternatives.

## Build and flash any Zephyr example

Activate the environment and set the SDK path as shown above. Replace the board
target and example path with those for your hardware and sample:

```powershell
west boards
$westRoot = (python -m west topdir).Trim()
$samplePath = Join-Path $westRoot 'zephyr/samples/<example-path>'
west build -p always -b <board-target> $samplePath -d builds/<example-name>
west flash -d builds/<example-name>
```

Check the board's Zephyr documentation for its target, supported runners,
required flash tools and drivers, and connection instructions. Check the sample's
README for required hardware and configuration. Use a separate build directory
for each example. The Zephyr documentation MCP server helps find these details;
flashing itself uses west and the board's local flash tool.


## MCP server sample on the connected board

See [apps/mcp_simple/README.md](apps/mcp_simple/README.md) for the direct
Ethernet configuration, build, flash, and verification instructions for the
FRDM-MCXN947 at this workspace location.

## Versions used for the MCP build

- Zephyr: NXP fork commit `1b3f4f14ad2002beb743dba17b455a1f0c688639` (local branch `nxp-main` tracks `nxp/main`).
- Zephyr SDK: `1.0.1`; Python: `3.12.10`.
- The selected Zephyr commit's `zephyr/west.yml` records the module revisions; run `python -m west update` to fetch them.
- Build artifacts contain absolute paths. After moving the workspace, use a fresh build directory. Recreate or repair the virtual environment if its launchers still point to the old location.
