DexNav searches in caves and buildings for Pokémon Gunk's FireRed Version.

## New

- **Searches off the grass.** Until now a land search only hid its Pokémon in tall grass, so it never started in
  caves or buildings. Now it works wherever wild Pokémon appear on foot: Mt. Moon, Rock Tunnel, Pokémon Tower, the
  Power Plant, the Pokémon Mansion, Seafoam Islands, Victory Road, Cerulean Cave, Mt. Ember, the Sevii Islands'
  caves and the Tanoby Chambers. Off the grass the patch is a puff of dust: "Dust is stirring nearby…".
- **Found: Cave / Indoors.** The DexNav screen's info panel says where a cave or building Pokémon is found.
- **Patches you can reach.** A land patch goes on a tile you can walk to (no wall, fence, ledge or water in the
  way) when there is one in range, so a search in a maze-like cave doesn't hide behind a wall.

## Notes

- Saves from v1.0, v1.2 and v1.3 carry over: the save layout is unchanged.
- DexNav Unown come from each Tanoby chamber's own letters, like wild ones, and every DexNav catch type stays legal
  in PKHeX.
- A new emulator test plays one game from New Game to the Hall of Fame with button presses (the starter, the
  rival, the parcel, every leader, the Elite Four and the Champion), using the DexNav, Quick Ball, Quick Run and
  the follower on the way. Another checks the DexNav on every wild map.

## Tested

On the v1.4 test build (the release game plus a test hook):

- The playthrough from New Game to the Hall of Fame: 43/43 checks.
- The DexNav on every wild map: 267/267 (the list matches the map's table, and a land or water search starts).
- DexNav catches checked in PKHeX: 72 land, 82 Unown (Tanoby, wild and DexNav) and 16 water, all legal.
- The emulator suite: save cycles and power cuts 35/35, features 33/33, Quick Ball 10/10 and on later turns 6/6,
  DexNav screen 16/16, items 4/4, Safari 3/3, the peek bar 12/12, rules 6/6, boxes 16/16, menus 9/9, followers
  16/16, story milestones against vanilla 11/11, and the story sweep the same as vanilla. The talk sweep differs from
  vanilla in one place, as in v1.2 and v1.3: the Dunsparce Tunnel prospector, whom the vanilla run skips.
- A DexNav search costs at most 5 frames.

## Patch it

You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

Apply `pokemon-gunks-firered-v1.4.bps` with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), Floating
IPS, or `py tools/patch/bps.py apply`. Patch the clean retail ROM. The patcher refuses any other ROM. The patched
ROM should be:

```
sha1: af5a08659cc4b473ae7d1a321e86487bbc30b679
```
