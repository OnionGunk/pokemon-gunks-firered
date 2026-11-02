# Pokémon Gunk's FireRed Version

A quality-of-life hack of Pokémon FireRed, built on [pret's FireRed decompilation](https://github.com/pret/pokefirered).
It keeps the game's difficulty and story as they are and takes the grind and friction out, for long playthroughs.

## Features

- **DexNav.** A key item that lists the grass Pokémon of the place you're in: seen ones by name, unseen ones as
  dashes. Pick one and it hides in a patch of rustling grass nearby; step in to battle it. Every Pokémon it finds
  is a legal wild roll for that spot. Search levels and chains raise the odds of good IVs and shinies.
- **Faster play:** instant text, a faster EXP bar, auto-run (hold B to walk), eggs that hatch twice as fast.
- **Items:** reusable TMs, two registered items (SELECT and R), bag sorting (START in the bag), a prompt to use
  another Repel when one runs out, and an Endless Repel you switch on and off.
- **Pokémon:** IV and EV view in the summary (A on the SKILLS page), Exp. All (half the EXP and the EVs for the
  Pokémon that didn't battle), vitamins up to 252 EVs, and trade evolutions without trading. HM moves work without
  teaching the move, and every PC has a free Move Tutor that remembers and forgets moves.
- **Save safety:** a save cut off by a power loss can no longer load as a mix of two saves (see below).

Oak's aide gives the Endless Repel, the Exp. All and the DexNav along with the Running Shoes in Pewter City. On a
save that is already past Pewter, Mom has them.

Save safety comes first: every build passes an emulator test suite that covers save cycles, power cuts at points
across the flash write, torn writes at every sector, and recovery from a damaged save slot.

### The save fix

FireRed keeps two save slots and writes the older one each time. When it loads, vanilla only checks that each of
a slot's 14 sectors has a good checksum. If the power goes off partway through a save, the slot being written
holds the new save's first sectors and the sectors from two saves ago after them. Every checksum is good, so
vanilla can load that mix. Gunk's FireRed also requires all 14 sectors to come from the same save, and falls back
to the other slot otherwise.

## Play it

Releases ship a **BPS patch**, not a ROM. You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

1. Download the `.bps` file from [Releases](../../releases).
2. Apply it to your ROM with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) (in the browser),
   Floating IPS, or `py tools/patch/bps.py apply <firered.gba> <patch.bps> <out.gba>`.
3. Play the result in any GBA emulator or flashcart. The patcher checks your ROM first and refuses the wrong one.

Saves carry over between releases unless the release notes say otherwise. Back up your save before updating.
A vanilla FireRed save loads in Gunk's FireRed.

## Build it

Follow pret's [`INSTALL.md`](INSTALL.md), then run `make`. A clean build reproduces the release ROM, and
`tools/patch/bps.py make` makes the patch from it. `docs/ENGINE.md` says why this hack uses the decompilation,
and `docs/GUNK_CHANGES.md` lists every change with how it was tested.

## Credits

- [pret](https://github.com/pret/pokefirered) for the FireRed decompilation this hack is built on, and
  [agbcc](https://github.com/pret/agbcc).
- The DexNav idea comes from later Pokémon games and fan hacks; ghoulslash's DexNav for
  [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) was the reference for its design.
- The Repel prompt follows the one in [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).
- [MinimalEffort07/pokefirered](https://github.com/MinimalEffort07/pokefirered) showed that FireRed's unused
  shaking-grass field effect and SaveBlock1's unused bytes are free to use.

Pokémon is © Nintendo, Creatures Inc. and GAME FREAK inc. This is a non-commercial fan project and contains
no ROM data; you need your own legally dumped copy of the game.
