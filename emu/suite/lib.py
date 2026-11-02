"""Game-level helpers for the FireRed test suite: symbols from the build's ELF, field and menu navigation,
in-game saving, power cycles and flash (SRAM) images.

Flash layout (src/save.c): 32 sectors of 4 KB. Sectors 0-13 are save slot 1, 14-27 slot 2, 28-29 Hall of Fame,
30-31 Trainer Tower. Each sector ends in a footer: id u16 @0xFF4, checksum u16 @0xFF6, signature u32 @0xFF8
(0x08012025), counter u32 @0xFFC. A save writes the slot `counter % 2`, all 14 sectors, ids 0..13 in order.
"""
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import emu  # noqa: E402

NM = r"C:\msys64\ucrt64\bin\arm-none-eabi-nm.exe"
SECTOR = 0x1000
SLOT_SECTORS = 14
SIGNATURE = 0x08012025
FLASH_SIZE = 0x20000


def symbols(elf):
    """name -> address for every symbol in the ELF (static ones too), cached next to it."""
    cache = elf + ".syms.json"
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(elf):
        return json.load(open(cache))
    out = subprocess.run([NM, elf], capture_output=True, text=True, check=True).stdout
    syms = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3:
            syms.setdefault(parts[2], int(parts[0], 16))
    json.dump(syms, open(cache, "w"))
    return syms


def footers(flash):
    """[(sector, id, counter, signature_ok, checksum_ok)] for sectors 0-27 of a flash image."""
    rows = []
    for s in range(2 * SLOT_SECTORS):
        b = flash[s * SECTOR:(s + 1) * SECTOR]
        sid, chk, sig, cnt = struct.unpack_from("<HHII", b, 0xFF4)
        rows.append((s, sid, cnt, sig == SIGNATURE, chk))
    return rows


class Game:
    def __init__(self, rom, elf):
        self.rom = rom
        self.sym = symbols(elf)

    # --- emulator plumbing ---
    def start(self):
        emu.start(self.rom)
        self.cmd("speed 6400")

    def cmd(self, *cmds, timeout=600):
        out = emu.run(list(cmds), timeout=timeout, echo=False)
        errors = [l for l in out if l.startswith("ERROR")]
        if errors:
            raise RuntimeError("; ".join(errors))
        return out[:-1]  # drop the "frame N" line

    def a(self, name):
        return self.sym[name]

    def u8(self, addr):
        return int(self.cmd(f"read {addr} 1")[0], 16)

    def u32(self, addr):
        b = bytes.fromhex(self.cmd(f"read {addr} 4")[0].replace(" ", ""))
        return struct.unpack("<I", b)[0]

    def frame(self):
        return int(emu.run(["wait 0"], echo=False)[-1].split()[1])

    def flash(self):
        path = os.path.join(emu.DIR, "flash.bin")
        self.cmd(f"dump SRAM 0 {FLASH_SIZE} {path}")
        return open(path, "rb").read()

    def set_flash(self, data):
        assert len(data) == FLASH_SIZE
        path = os.path.join(emu.DIR, "flash_in.bin")
        open(path, "wb").write(data)
        self.cmd(f"poke SRAM 0 {path}")

    # --- game state ---
    def field_ready(self):
        """The player can walk: overworld main loop, no script running, controls unlocked."""
        cb2 = self.u32(self.a("gMain") + 4)
        return (cb2 & ~1) == self.a("CB2_Overworld") and self.u8(self.a("sLockFieldControls")) == 0 \
            and self.u8(self.a("sGlobalScriptContextStatus")) != 0

    def wait_field(self, press="A", max_steps=400, settle=3):
        """Press <press> every 20 frames until the field has been ready for <settle> checks in a row."""
        ok = 0
        for _ in range(max_steps):
            if self.field_ready():
                ok += 1
                if ok >= settle:
                    return True
                self.cmd("wait 20")
            else:
                ok = 0
                self.cmd(f"press {press} 4" if press else "wait 4", "wait 16")
        return False

    def save_counter(self):
        return self.u32(self.a("gSaveCounter"))

    def open_save_dialog(self):
        """Start menu -> SAVE -> 'Would you like to save?' (stops with the yes/no box up)."""
        self.cmd("press Start 4", "wait 30")
        n = self.u8(self.a("sNumStartMenuItems"))
        order = bytes.fromhex(self.cmd(f"read {self.a('sStartMenuOrder')} {n}")[0].replace(" ", ""))
        target = order.index(self.STARTMENU_SAVE)
        for _ in range(16):
            pos = self.u8(self.a("sStartMenuCursorPos"))
            if pos == target:
                break
            self.cmd("press Down 4" if pos < target else "press Up 4", "wait 6")
        assert self.u8(self.a("sStartMenuCursorPos")) == target
        self.cmd("press A 4", "wait 60")

    STARTMENU_SAVE = 4  # enum StartMenuOption in src/start_menu.c

    def dialog_cb(self):
        return self.u32(self.a("sSaveDialogCB")) & ~1

    def save(self, crash_after=None):
        """Save through the Start menu. crash_after=N power-cycles N frames after the flash write starts
        (returns then, without waiting for the save to finish). Returns the frames the write took."""
        self.open_save_dialog()
        do_save = self.a("SaveDialogCB_DoSave")
        for _ in range(400):
            if self.dialog_cb() == do_save:
                break
            self.cmd("press A 4", "wait 10")
        else:
            raise RuntimeError("save dialog never reached DoSave")
        start = self.frame()
        if crash_after is not None:
            self.cmd(f"wait {crash_after}", "reboot")
            return None
        # DoSave returns after TrySavingData finishes; the dialog then moves on
        for _ in range(2000):
            if self.dialog_cb() != do_save:
                break
            self.cmd("wait 2")
        took = self.frame() - start
        if not self.wait_field(press="B"):
            raise RuntimeError("field did not come back after saving")
        return took

    def boot_continue(self):
        """From a power-on: skip the intro, CONTINUE on the main menu, wait for the field."""
        for _ in range(60):
            cb2 = self.u32(self.a("gMain") + 4) & ~1
            if cb2 == self.a("CB2_MainMenu"):
                break
            self.cmd("press Start 4", "wait 30")
        else:
            raise RuntimeError("main menu never came up")
        self.cmd("wait 60")
        status = self.u8(self.a("gSaveFileStatus"))
        if not self.wait_field(press="A"):
            raise RuntimeError("Continue did not reach the field")
        return status

    def reboot(self):
        self.cmd("reboot")
