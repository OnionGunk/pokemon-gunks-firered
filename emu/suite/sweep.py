"""Map sweep: Continue into every map with a follower and check the game reaches the field and keeps running.

Usage: py -3 emu/suite/sweep.py <rom.gba> <rom.elf> [first_map_index] [count]

One new game with a Pikachu is saved, the game is power-cycled to its main menu and a savestate taken there.
For each map (but the link rooms), the state is loaded, the save block's continue-game warp is pointed at the map's first warp event
(the game puts the player on it), and CONTINUE is chosen. A map passes when the field comes up within 20 seconds,
the main loop is still running 3 seconds later, and the follower is out (maps where the game hides it, such as
ones the player arrives in on water, count as passes with a note). Results: emu/suite/out/<rom>/sweep.txt.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from features import FLAG_SYS_POKEMON_GET, SPECIES, Features  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))


def maps():
    groups = json.load(open(os.path.join(REPO, "data/maps/map_groups.json")))
    out = []
    for gi, gname in enumerate(groups["group_order"]):
        for mi, mname in enumerate(groups[gname]):
            m = json.load(open(os.path.join(REPO, "data/maps", mname, "map.json")))
            # the link rooms (Cable Club, Union Room) are only entered through a link
            if m.get("warp_events") and gname != "gMapGroup_Link":
                out.append((gi, mi, mname))
    return out


def main():
    rom, elf = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    f = Features(rom, elf)
    g = f.g
    f.new_game(mons=[(SPECIES["PIKACHU"], 50)], flags=[FLAG_SYS_POKEMON_GET], name="sweep")
    g.save()
    g.reboot()
    for _ in range(60):
        if (g.u32(g.a("gMain") + 4) & ~1) == g.a("CB2_MainMenu"):
            break
        g.cmd("press Start 4", "wait 30")
    g.cmd("wait 90", f"save {f.path('sweep_menu.state')}")
    todo = maps()[first:first + count]
    lines = []
    t0 = time.time()
    for gi, mi, name in todo:
        g.cmd(f"load {f.path('sweep_menu.state')}")
        sb1, sb2 = f.sb1(), f.sb2()
        g.cmd(f"write8 {sb1 + 0xC} {gi}", f"write8 {sb1 + 0xD} {mi}", f"write8 {sb1 + 0xE} 0",
              f"write16 {sb1 + 0x10} 65535", f"write16 {sb1 + 0x12} 65535", f"write8 {sb2 + 9} {g.u8(sb2 + 9) | 1}")
        reached = g.wait_field(press="A", max_steps=60, settle=3)
        alive = int(g.cmd(f"alive {g.a('gMain') + 0x24} 180")[0].split()[1])
        follower = f.count_follower_objects()
        ok = reached and alive > 150
        note = "" if follower == 1 else f" (followers: {follower})"
        line = f"{'PASS' if ok else 'FAIL'} {gi:2}.{mi:<3} {name}: field {reached}, frames {alive}{note}"
        if not ok or follower != 1:
            g.cmd(f"shot {f.path('sweep_' + name + '.png')}")
        print(line, flush=True)
        lines.append(line)
    import emu
    emu.stop()
    failed = [l for l in lines if l.startswith("FAIL")]
    summary = f"{len(lines) - len(failed)}/{len(lines)} maps passed in {time.time() - t0:.0f}s"
    print(summary)
    with open(os.path.join(os.path.dirname(f.out), "sweep.txt"), "w") as out:
        out.write("\n".join(lines + [summary]) + "\n")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
