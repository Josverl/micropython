# virtual .venv

when you start a new shell or teminal ,
you first need to activate the virtual environment

```bash
source ~/micropython/.venv/bin/activate
```

## test while refactoring 

after refactoring a module or function.
valways verify that the old bash tests still pass.
```
(.venv) jos@josverl-sb5:~/micropython/tools/mpremote/tests$ ./run-mpremote-tests.sh 
./test_errno.sh: OK
./test_eval_exec_run.sh: OK
./test_filesystem.sh: OK
./test_fs_tree.sh: OK
./test_mip_local_install.sh: OK
./test_mount.sh: OK
./test_recursive_cp.sh: OK
./test_resume.sh: OK

```

## add new tests 
make sure that you create new pytest based test 

use the existing bash tests as reference.

## connected devices 

you can check if devices are connected using 
`mpflash list --json `

```bash
[
    {
        "serialport": "/dev/ttyACM0",
        "family": "micropython",
        "description": "Raspberry Pi Pico W with RP2040",
        "version": "1.26.0",
        "port": "rp2",
        "cpu": "RP2040",
        "arch": "armv6m",
        "mpy": "v6.3",
        "build": "",
        "location": "/dev/serial/by-path/platform-vhci_hcd.0-usb-0:1:1.0",
        "toml": {},
        "vid": 11914,
        "pid": 5,
        "board": "RPI_PICO_W",
        "board_id": "RPI_PICO_W",
        "variant": ""
    }
]
```
