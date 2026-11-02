"""Feature checks for Gunk's FireRed, in the emulator.

Usage: py -3 emu/suite/features.py <rom.gba> <rom.elf> [check ...]

Each check starts a new game through the ROM's test hook (src/gunk_test.c: the Pokemon, items and flags the
check needs), plays it with button presses, and reads the result from RAM. Screenshots go to
emu/suite/out/<rom name>/features/.
"""
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import FLASH_SIZE, Game  # noqa: E402

ERASED = b"\xff" * FLASH_SIZE
GUNK_TEST_MAGIC = 0x4B4E5547

# constants (include/constants/*.h)
SPECIES = {"BULBASAUR": 1, "ONIX": 95, "KADABRA": 64, "ALAKAZAM": 65, "PIKACHU": 25, "CHARMANDER": 4}
ITEM = {"REPEL": 86, "RARE_CANDY": 68, "PROTEIN": 64, "TM01": 289, "HM01": 339, "ENDLESS_REPEL": 52,
        "EXP_ALL": 53, "DEXNAV": 54, "POTION": 13, "POKE_BALL": 4}
FLAG_SYS_B_DASH = 0x82F
FLAG_GUNK_ENDLESS_REPEL_ON = 0x4A7
MAP_ROUTE1 = (3, 19)
SB1_REGISTERED_ITEM = 0x296
VAR_REPEL_STEP_COUNT = 0x4020
VAR_GUNK_LAST_REPEL = 0x4029
SB1_VARS = 0x1000
SB1_FLAGS = 0x0EE0
SB1_BAG_ITEMS = 0x0310
SB2_OPTIONS = 0x14
SB2_ENCRYPTION_KEY = 0xF20


class Features:
    def __init__(self, rom, elf):
        self.g = Game(rom, elf)
        self.out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out",
                                os.path.splitext(os.path.basename(rom))[0], "features")
        os.makedirs(self.out, exist_ok=True)
        self.results = []

    def path(self, name):
        return os.path.join(self.out, name).replace("\\", "/")

    def shot(self, name):
        self.g.cmd(f"shot {self.path(name)}")

    def record(self, check, ok, detail):
        self.results.append((check, ok, detail))
        print(("PASS " if ok else "FAIL ") + check + ": " + detail, flush=True)

    # --- RAM helpers ---
    def sb1(self):
        return self.g.u32(self.g.a("gSaveBlock1Ptr"))

    def sb2(self):
        return self.g.u32(self.g.a("gSaveBlock2Ptr"))

    def u16(self, addr):
        return struct.unpack("<H", bytes.fromhex(self.g.cmd(f"read {addr} 2")[0].replace(" ", "")))[0]

    def var(self, var):
        return self.u16(self.sb1() + SB1_VARS + (var - 0x4000) * 2)

    def set_var(self, var, value):
        self.g.cmd(f"write16 {self.sb1() + SB1_VARS + (var - 0x4000) * 2} {value}")

    def flag(self, flag):
        return (self.g.u8(self.sb1() + SB1_FLAGS + flag // 8) >> (flag % 8)) & 1

    def bag_count(self, item, pocket_offset=SB1_BAG_ITEMS, slots=42):
        key = self.u16(self.sb2() + SB2_ENCRYPTION_KEY)
        data = bytes.fromhex(self.g.cmd(f"read {self.sb1() + pocket_offset} {slots * 4}")[0].replace(" ", ""))
        for i in range(slots):
            iid, qty = struct.unpack_from("<HH", data, i * 4)
            if iid == item:
                return qty ^ key
        return 0

    # --- setup ---
    def new_game(self, mons=(), items=(), flags=(), name="new"):
        """Power on with an erased flash, set the test hook, play the intro to the bedroom."""
        g = self.g
        g.start()
        g.set_flash(ERASED)
        g.reboot()
        g.cmd("wait 30")
        g.cmd(f"write32 {g.a('gGunkTestMagic')} {GUNK_TEST_MAGIC}")
        for i, (species, level) in enumerate(mons):
            g.cmd(f"write16 {g.a('gGunkTestMons') + i * 4} {species}", f"write16 {g.a('gGunkTestMons') + i * 4 + 2} {level}")
        for i, (item, qty) in enumerate(items):
            g.cmd(f"write16 {g.a('gGunkTestItems') + i * 4} {item}", f"write16 {g.a('gGunkTestItems') + i * 4 + 2} {qty}")
        for i, flag in enumerate(flags):
            g.cmd(f"write16 {g.a('gGunkTestFlags') + i * 2} {flag}")
        for _ in range(80):
            if (g.u32(g.a("gMain") + 4) & ~1) == g.a("CB2_MainMenu"):
                break
            g.cmd("press Start 4", "wait 30")
        if not g.wait_field(press="A", max_steps=1500, settle=5):
            raise RuntimeError("intro never reached the field")
        g.cmd("wait 30")
        self.shot(f"{name}_bedroom.png")

    def warp(self, map_group, map_num, x, y, name="warp"):
        """Save with the game's own "continue game warp" set to (map, x, y), power-cycle and Continue: the game
        then warps there as it does after a white-out (SaveBlock1 continueGameWarp, SaveBlock2 flag bit 0)."""
        g = self.g

        def edit():
            sb1, sb2 = self.sb1(), self.sb2()
            g.cmd(f"write8 {sb1 + 0xC} {map_group}", f"write8 {sb1 + 0xD} {map_num}", f"write8 {sb1 + 0xE} 255",
                  f"write16 {sb1 + 0x10} {x}", f"write16 {sb1 + 0x12} {y}",
                  f"write8 {sb2 + 9} {g.u8(sb2 + 9) | 1}")
        g.save(before_save=edit)
        g.reboot()
        g.boot_continue()
        g.cmd("wait 30")
        self.shot(f"{name}.png")

    # --- checks ---
    def check_header(self):
        title = bytes.fromhex(self.g.cmd("read 0x080000A0 16")[0].replace(" ", ""))
        self.record("header", title[:12] == b"GUNK FR\0\0\0\0\0" and title[12:16] == b"BPRE", repr(title))

    def check_text_speed_default(self):
        speed = self.g.u8(self.sb2() + SB2_OPTIONS) & 7
        self.record("text speed", speed == 2, f"new game text speed {speed} (2 = FAST)")

    def check_follower(self):
        """The lead (Bulbasaur) walks behind the player."""
        g = self.g
        g.cmd("press Left 40", "wait 20", "press Down 8", "wait 30")
        self.shot("follower.png")
        objs = g.a("gObjectEvents")
        found = None
        for i in range(16):
            raw = bytes.fromhex(g.cmd(f"read {objs + i * 0x24} 12")[0].replace(" ", ""))
            active = raw[0] & 1
            gfx, local_id = raw[5], raw[8]
            if active and local_id == 254:
                found = (i, gfx)
        self.record("follower", found is not None and found[1] == 152, f"follower object {found}")

    def check_auto_run(self):
        g = self.g
        flags_addr = g.a("gPlayerAvatar")
        g.cmd("press Right 3")
        running = g.u8(flags_addr) & 0x80
        g.cmd("wait 20", "press Right+B 3")
        walking = g.u8(flags_addr) & 0x80
        g.cmd("wait 20")
        self.record("auto-run", running != 0 and walking == 0,
                    f"dash flag {running:#x} without B, {walking:#x} holding B")

    def check_repel_prompt(self):
        g = self.g
        before = self.bag_count(ITEM["REPEL"])
        self.set_var(VAR_REPEL_STEP_COUNT, 1)
        self.set_var(VAR_GUNK_LAST_REPEL, ITEM["REPEL"])
        g.cmd("press Left 16", "wait 40")
        self.shot("repel_prompt.png")
        g.cmd("press A 4", "wait 60")
        self.shot("repel_used.png")
        g.cmd("press A 4", "wait 30", "press A 4", "wait 30")
        steps = self.var(VAR_REPEL_STEP_COUNT)
        after = self.bag_count(ITEM["REPEL"])
        self.record("repel prompt", steps == 100 and after == before - 1,
                    f"Repels {before} -> {after}, steps {steps}")

    def pos(self):
        sb1 = self.sb1()
        return struct.unpack("<hh", bytes.fromhex(self.g.cmd(f"read {sb1} 4")[0].replace(" ", "")))

    def in_battle(self):
        return (self.g.u32(self.g.a("gMain") + 4) & ~1) == self.g.a("BattleMainCB2")

    def walk_to(self, tx, ty, max_steps=60):
        """Walk (map coords) one tile at a time, stopping early if a battle starts."""
        for _ in range(max_steps):
            x, y = self.pos()
            if (x, y) == (tx, ty) or self.in_battle():
                return
            if x != tx:
                d = "Right" if tx > x else "Left"
            else:
                d = "Down" if ty > y else "Up"
            self.g.cmd(f"press {d} 8", "wait 10")

    def check_auto_run_outdoors(self):
        """Tiles covered holding a direction for 32 frames on open ground: 4 running (8 frames a tile), 2 walking."""
        g = self.g
        x0, _ = self.pos()
        g.cmd("press Right 32", "wait 20")
        x1, _ = self.pos()
        g.cmd("press Right+B 32", "wait 20")
        x2, _ = self.pos()
        ran, walked = x1 - x0, x2 - x1
        self.record("auto-run", ran >= 3 and 1 <= walked <= 2, f"{ran} tiles without B, {walked} holding B")

    def check_endless_repel(self):
        """Lead at level 100 and the Endless Repel on: 30 steps in tall grass, no wild battle."""
        x, y = self.pos()
        battles = 0
        for i in range(30):
            self.g.cmd("press Left 8" if i % 2 == 0 else "press Right 8", "wait 10")
            if self.in_battle():
                battles += 1
                break
        self.record("endless repel", battles == 0 and self.flag(FLAG_GUNK_ENDLESS_REPEL_ON) == 1,
                    f"{battles} wild battles in 30 steps of grass")

    def check_dexnav(self):
        g = self.g
        g.cmd(f"write16 {self.sb1() + SB1_REGISTERED_ITEM} {ITEM['DEXNAV']}")
        g.cmd("press Select 4", "wait 60")
        self.shot("dexnav_list.png")
        g.cmd("press A 4", "wait 60")
        self.shot("dexnav_hiding.png")
        search = g.a("sSearch")
        raw = bytes.fromhex(g.cmd(f"read {search} 12")[0].replace(" ", ""))
        species, sx, sy = struct.unpack_from("<Hhh", raw, 0)
        active = raw[10]
        g.cmd("press A 4", "wait 30", "press A 4", "wait 30")
        self.shot("dexnav_patch.png")
        self.walk_to(sx - 7, sy - 7)
        g.cmd("wait 200")
        self.shot("dexnav_battle.png")
        enemy = struct.unpack("<H", bytes.fromhex(g.cmd(f"read {g.a('gEnemyParty') + 0x20} 2")[0].replace(" ", "")))[0]
        battle = self.in_battle()
        self.record("dexnav", active == 1 and battle, f"searched species {species} at ({sx - 7},{sy - 7}); "
                    f"battle {battle}")


def main():
    rom, elf = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    f = Features(rom, elf)
    t0 = time.time()
    try:
        f.new_game(mons=[(SPECIES["BULBASAUR"], 10)], items=[(ITEM["REPEL"], 3)], flags=[FLAG_SYS_B_DASH],
                   name="basic")
        f.check_header()
        f.check_text_speed_default()
        f.check_follower()
        f.check_repel_prompt()
        f.new_game(mons=[(SPECIES["PIKACHU"], 100)], items=[(ITEM["DEXNAV"], 1)],
                   flags=[FLAG_SYS_B_DASH, FLAG_GUNK_ENDLESS_REPEL_ON], name="route1")
        f.warp(*MAP_ROUTE1, 4, 18, name="route1_warp")
        f.check_auto_run_outdoors()
        f.walk_to(15, 23)
        f.walk_to(15, 25)
        f.check_endless_repel()
        f.walk_to(15, 23)
        f.check_dexnav()
    finally:
        import emu
        emu.stop()
    failed = [r for r in f.results if not r[1]]
    print(f"{len(f.results) - len(failed)}/{len(f.results)} passed in {time.time() - t0:.0f}s")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
