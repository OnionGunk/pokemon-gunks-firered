# More PC boxes: plan and verdict

**Verdict: not done for v1.0.** FireRed's save layout has no room for even one more box without giving up the
two-slot save safety or rewriting how every boxed Pokémon is stored. The options and numbers follow.

## The layout (src/save.c, include/save.h)

128 KB flash = 32 sectors of 4 KB, each with 3,968 data bytes and a 128-byte footer.

| Sectors | Holds | Double-buffered |
|---|---|---|
| 0-13 | Save slot 1 | yes |
| 14-27 | Save slot 2 | yes |
| 28-29 | Hall of Fame | no |
| 30-31 | Trainer Tower (e-Reader) | no |

Each slot holds 14 sectors: SaveBlock2 (1 sector), SaveBlock1 (4 sectors), PokemonStorage (9 sectors).

| Block | Size | Room in its sectors | Free |
|---|---|---|---|
| SaveBlock2 | 0xF24 = 3,876 | 3,968 | 92 |
| SaveBlock1 | 0x3D68 = 15,720 | 15,872 | 152 |
| PokemonStorage (14 boxes) | 0x83D0 = 33,744 | 35,712 | 1,968 |

One more box costs 30 × 80 (BoxPokemon) + 9 (name) + 1 (wallpaper) = **2,410 bytes**. The whole slot has 2,212
bytes free, spread over three blocks.

## Options considered

1. **Use the free bytes in the slot.** 2,212 < 2,410: not even one box.
2. **Free unused SaveBlock1 fields** (e-Reader/Mystery Gift data, `unused_*` padding, link records). That frees
   about 1-2 KB, so one box at most. It needs the box code to handle a box split across blocks, and old saves stop
   loading. Not worth one box.
3. **Use sectors 30-31** (Trainer Tower e-Reader data, which normal play doesn't write). They aren't
   double-buffered. Boxes there would have no backup copy, so a power cut while saving could lose them. That breaks
   the hack's first rule.
4. **Pack boxed Pokémon tighter** (about 70 bytes instead of 80, by bit-packing the substructures). That gives
   about 16 boxes, so +2. It means re-encoding every boxed Pokémon on save and load, and a bug there corrupts
   every box. That's high risk for a small gain.
5. **Bigger flash.** 128 KB is the largest GBA flash chip; there's nothing bigger to move to.

## If it's wanted later

Option 4 is the only one that keeps both save slots. It would be a separate, heavily tested change with its own
save-suite cases: a full-box round trip, every species and form, eggs, and a Bad Egg checksum.
