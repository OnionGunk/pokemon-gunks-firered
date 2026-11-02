# Gunk's changes for FireRed: verdict list

Each Gunk's Platinum change, what FireRed already has, and what this hack does. "Test" says how it was checked in
the emulator (`emu/`). The save suite (`emu/suite/suite.py`) runs after every build.

Status: **done** = written and checked in the emulator; **written** = in the code, not yet checked.

| # | Change | FireRed (vanilla) | What Gunk's FireRed does | Status | Test |
|---|---|---|---|---|---|
| 0 | Header title | `POKEMON FIRE` | `GUNK FR` (game code stays `BPRE`, so emulators keep their FireRed save type) | written | |
| 1 | Save safety | Two slots; a slot passes when each sector's checksum is good | Also requires all 14 sectors of a slot to carry the same save counter (`src/save.c`), so a torn save falls back to the other slot | written | |
| 2 | Instant text | SLOW / MID / FAST | A fourth speed, INSTANT, prints everything up to the next button wait each frame; new games start on FAST | written | |
| 3 | Faster EXP bar | 1 pixel a frame | 2 pixels a frame | written | |
| 4 | Auto-run | Hold B with the Running Shoes | Runs by default with the Running Shoes; hold B to walk | written | |
| 5 | Repel prompt | "REPEL's effect wore off…" | Offers to use another of the same Repel if the bag has one (last Repel in var 0x4029) | written | |
| 6 | Endless Repel | — | Key item (slot 52, unused in vanilla): on/off, works like a Repel while on (flag 0x4A7) | written | |
| 7 | Reusable TMs | TMs are used up | TMs stay in the TM Case, like HMs | written | |
| 8 | Two registered items | One (SELECT) | The latest on SELECT, the one before on R (var 0x402A). In the field, R no longer opens Help while a second item is registered; L still does | written | |
| 9 | Bag sorting | Items move one at a time with SELECT | START sorts the open pocket by item number | written | |
| 10 | IV/EV view | — | A on the summary's SKILLS page cycles stats → IVs → EVs | written | |
| 11 | Exp. All | Exp. Share only | Key item (slot 53): while on, healthy party members that didn't battle get half a battler's EXP, and the EVs (flag 0x4A8) | written | |
| 12 | Vitamins to 252 | Stop at 100 EVs | Work up to 252 | written | |
| 13 | Trade evolutions | Need a link trade | Kadabra at 36, Machoke, Graveler and Haunter at 37; the trade items (King's Rock, Metal Coat, Dragon Scale, Up-Grade, Deep Sea Tooth/Scale) can be used like stones. Cross-generation targets still wait for the National Pokédex, as in vanilla | written | |
| 14 | HMs without teaching | Need the move | A Pokémon that could learn the move from an HM in the bag can use it; badges still apply; the party menu lists it while there's room | written | |
| 15 | Move Tutor | Move Maniac (Two Island, for mushrooms), Move Deleter (Fuchsia) | Every PC has a free MOVE TUTOR row that remembers level-up moves and forgets moves | written | |
| 16 | Faster egg hatching | An egg cycle every 256 steps | Every 128 steps | written | |
| 17 | More PC boxes | 14 boxes; storage fills its 9 flash sectors | **Skipped**: no room without losing the backup slot; see `docs/PC_BOXES_PLAN.md` | skipped | |
| 18 | DexNav | — | Key item (slot 54): lists the map's grass Pokémon; the chosen one hides in rustling grass nearby. Legal wild rolls; the search level and chain set how many are rolled (best kept). Search data in SaveBlock1's unused 400 bytes | written | |
| 19 | Following Pokémon | — | Planned: movement from MinimalEffort07/pokefirered, sprites from pokeemerald-expansion | todo | |

The three new key items come from Oak's aide in Pewter City with the Running Shoes, or from Mom on a save that is
already past that.
