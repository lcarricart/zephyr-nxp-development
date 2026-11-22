# Applications

Place each Zephyr application in its own directory in `apps`. Each can have
its own `CMakeLists.txt`, `prj.conf`, sources, and board overlays.

From the workspace root, activate the environment and build the starter app
for the FRDM-MCXN947 CPU0:

```powershell
.\.venv\Scripts\Activate.ps1
$env:ZEPHYR_SDK_INSTALL_DIR = 'C:/Users/luchi/zephyr-sdk-1.0.1'
west build -b frdm_mcxn947/mcxn947/cpu0 apps/hello_world -d builds/hello_world
west flash -d builds/hello_world
```

Use a different build directory for each application. Flashing programs the
connected board; connect and configure its debug probe before running it.

The CMSIS, CMSIS 6, and NXP HAL projects have been initialized for the starter
build. Other Zephyr features may require additional west projects.

## Generate an SBOM

An SBOM records the software included in a particular build, including its
Zephyr and module dependencies. It is useful to include alongside an example
when copying the application to another repository. It describes that build;
it does not include the dependencies themselves or guarantee that the app can
be rebuilt from the application folder alone.

For this workspace's Zephyr checkout, add the following line to the
application's `prj.conf` before building:

```conf
CONFIG_BUILD_OUTPUT_META=y
```

Then, from the workspace root with the environment activated, build and
generate the SPDX documents inside the application folder:

```powershell
west build -b frdm_mcxn947/mcxn947/cpu0 apps/hello_world -d builds/hello_world
west spdx -d builds/hello_world -s apps/hello_world/sbom
```

Replace the application, build directory, board, and output directory for other
examples. The `sbom` directory will be included when you copy the application
folder. Keep the generated documents together: they can refer to each other.
Generation uses SPDX 2.3 by default. Review the documents before publishing,
including their file paths and license information. Regenerate the SBOM after
changing the app, board, configuration, or dependencies, so it matches the
build you intend to share; generation can overwrite existing documents in the
output directory.

For reproducibility, also record the Zephyr and module revisions used for the
build, along with the board and SDK version. `west manifest --freeze` can help
record manifest revisions, but it requires the relevant projects to be cloned
and uses their `manifest-rev` branches, which may differ from checked-out or
locally modified files. An SBOM alone is not a locked workspace manifest. See Zephyr's
[SBOM documentation](https://docs.zephyrproject.org/latest/develop/west/zephyr-cmds.html#software-bill-of-materials-west-spdx)
for more options, including header analysis.
