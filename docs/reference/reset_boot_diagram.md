
# MicroPython reset and boot flow

This diagram summarizes reset entry points and the startup sequence described in
the reset/boot reference.
```mermaid
---
config:
  
  flowchart:
    curve: monotoneX
---

flowchart TD

    COLD["Cold start (power on)"]
    RESET_BTN["Reset button"]
    M_RESET["machine.reset()"]


    %% order of the main stages 
    HW --> VM
    BOOT --> APPSTAGE --> REPLSTAGE
    %% SOFT_RESET --> VM_RESET


    COLD --> HARD
    RESET_BTN --> HARD
    M_RESET --> MCU_RESET

%%-------------------------------------------------------------------
    subgraph HW["Hardware stage"]
        HARD["hardware re-init"] 
        MCU_RESET["MCU reset"]
        HARD --> MCU_RESET
        MCU_RESET --> VM_INIT

        HARD  <-.- C10@{ shape: text, label: "Set all internal hardware states to their power-on state" }
        MCU_RESET  <-.- C11@{ shape: text, label: "Restart the CPU, re-initializes most peripherals, and clears the RAM." }
    end

    style HW fill:darkgreen,stroke:gold
    style VM fill:darkblue,stroke:gold
    
%%-------------------------------------------------------------------
    subgraph VM["MicroPyton VM"]

        VM_INIT@{ shape: text, label: "VM init" }
        VM_RESET@{ shape: text, label: "VM reset" }
        SAFE_MODE@{ shape: card, label: "Safe mode ? STM32 and renesas-ra only" }

        VM_INIT --> VM_RESET
        VM_RESET--> SAFE_MODE

        SAFE_MODE -- NORMAL --> BOOT
        SAFE_MODE -- SAFE --> REPL  
%%-------------------------------------------------------------------
        subgraph BOOT["Boot stage"]
            %%HAS_PBOOT(["_boot.py ?"])
            RUN_PBOOT@{ shape: card, label: "if exist: exec _boot.py" }
            %%HAS_BOOT(["boot.py ?"])
            RUN_BOOT@{ shape: card, label: "if exist: exec boot.py" }
        end
        RUN_PBOOT --> RUN_BOOT --> HAS_MAIN

%%-------------------------------------------------------------------
        subgraph APPSTAGE["Application stage"]
            HAS_MAIN@{ shape: card, label: "if exist: main.py, AND NOT in raw REPL"}

            subgraph YOURAPP["Your Application"]
                RUNMAIN["exec main.py"]
                A@{ shape: processes, label: "imported modules" }
            end
            style YOURAPP fill:#701705,stroke:gold
        end
        %% SOFT_RESET --> VM_RESET
        %%HAS_PBOOT -- Yes --> RUN_PBOOT --> HAS_BOOT
        %%HAS_PBOOT -- No --> HAS_BOOT
        %%HAS_BOOT -- Yes --> RUN_BOOT  --> HAS_MAIN
        %%HAS_BOOT -- No --> HAS_MAIN
        HAS_MAIN -- No --> REPL
        HAS_MAIN -- Yes --> RUNMAIN --> REPL
%%-------------------------------------------------------------------
        subgraph REPLSTAGE["REPL"]
            TO_RESET@{ shape: start }
            REPL["Interactive REPL"]
            RAWREPL["RAW REPL"]
            %% PASTEMODE["Paste mode"]
        end
        style REPLSTAGE fill:#706B05,stroke:gold


        REPL e1@-- CTRL-A -->  RAWREPL
        REPL e2@-- CTRL-D --> TO_RESET
        RAWREPL e3@-- CTRL-B --> REPL
        RAWREPL e4@-- CTRL-D --> TO_RESET
        TO_RESET e5@--> VM_RESET
        
        e1@{ curve: catmullRom }
        e2@{ curve: natural }
        e3@{ curve: catmullRom }
        e4@{ curve: natural }
        e5@{ curve: natural }
    
        %% Paste mode not relevant for boot flow, but included for completeness
        %% REPL -- CTRL-E --> PASTEMODE
        %% PASTEMODE -- CTRL-D --> REPL
        %% PASTEMODE -- CTRL-C --> REPL
    end


```

## Notes

- Hard reset entry points include cold power-on, reset button, and
	`machine.reset()`.
- Soft reset entry points include `machine.soft_reset()` and `Ctrl-D` at REPL.
- `_boot.py` runs first (frozen in firmware), then `boot.py`, then `main.py`.
- If `main.py` is missing, or it exits, the REPL starts.
- A soft reset triggered from raw REPL mode skips `main.py` startup.
- Startup entry points on the filesystem are ``boot.py`` and ``main.py``.
- If a frozen module named ``main.py`` exists, it is run first and cannot be
    overridden by filesystem ``main.py`` or ``main.mpy``.
- For regular imports, frozen modules are usually overrideable by filesystem
    modules because filesystem paths are searched before ``.frozen`` by default
    ``sys.path`` order.
- ``boot.mpy``/``main.mpy`` on the filesystem are not auto-executed as startup
    entry points.
- To use ``.mpy`` at startup, import pre-compiled modules from ``boot.py`` or
    ``main.py``, or freeze modules named ``boot.py``/``main.py`` into firmware.

- Port-specific startup-script selection hooks:
    ``pyb.main(filename)`` is supported on stm32 and renesas-ra, and
    ``machine.main(filename)`` is supported on cc3200/WiPy. These are intended to
    be called from ``boot.py`` to choose which script is run in the main stage.

- Built-in safe-boot mode (skip ``boot.py``/``main.py``) is documented on:
    stm32/pyboard, renesas-ra, and wipy/cc3200.
    On esp32 and rp2, documentation describes factory reset/reflash recovery
    rather than a built-in safe-boot script-skip mode.


