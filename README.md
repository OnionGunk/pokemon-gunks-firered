# Pokémon Gunk's FireRed Version

A quality-of-life hack of Pokémon FireRed, built on [pret's FireRed decompilation](https://github.com/pret/pokefirered).
It keeps the game's difficulty and story as they are and takes the grind and friction out, for long playthroughs.

## Features

- **DexNav.** Professor Oak gives it to you with the Pokédex. Use it from the Bag (or register it to SELECT) and
  its screen shows the area's Pokémon on LAND, WATER and OTHER tabs (switch with L/R): an icon once seen, "?"
  before that, a ball mark once caught, and for the highlighted one how it's found, its levels, search level and
  chain. Pick a grass or water Pokémon you've seen and it hides nearby in rustling grass or rippling water; step or
  Surf into the patch within 10 seconds to battle it. While you look, a bar at the top shows what's hiding: level,
  shiny, nature, ability, perfect IVs and held item. Searches roll legal wild encounters, and search levels and
  chains raise the odds of good IVs, shinies and held items. OTHER lists the area's fishing and Rock Smash
  Pokémon by rod.
- **Area info:** START on the DexNav screen shows the area's encounter odds and levels for grass, water, each rod
  and Rock Smash, where the roaming legendary is now, and what your Repel lets through.
- **Pokémon follow you.** Your lead walks behind you, any of the 386 species, shinies in their shiny colors. Talk to
  it and it reacts by mood; it goes back into its ball while you Surf and during story scenes. RETURN in its party
  menu puts it away, WALK brings it back.
- **16 PC boxes** (14 in the original game). A vanilla FireRed save loads, with its boxes kept.
- **Faster play:** instant text, a faster EXP bar, auto-run (hold B to walk), eggs that hatch twice as fast.
- **Quick Run and Quick Ball** in wild battles: press R to run, or L to throw your last-used ball, shown with how
  many are left. Hold L and press Left or Right to pick another ball.
- **Items:** reusable TMs, two registered items (SELECT and R), bag sorting (START in the Bag), a prompt to use
  another Repel when one runs out, and an Endless Repel toggle.
- **Pokémon:** IV and EV view in the summary (A on the SKILLS page), Exp. All, vitamins up to 252 EVs, and trade
  evolutions without trading. HM moves work without teaching the move, and every PC has a free Move Tutor.

Oak gives the Endless Repel, the Exp. All and the DexNav when you bring him his parcel, before the first gym. On a
save that's already past that, Mom has them.

Save safety comes first: every build passes an emulator test suite that covers save cycles, power cuts at points
across the flash write, torn writes at every sector and damaged-slot recovery. Gunk's FireRed also refuses to load
a save slot whose sectors come from two different saves, falling back to the other slot instead.
[`docs/GUNK_CHANGES.md`](docs/GUNK_CHANGES.md) lists every change and how it was tested.

## Play it

Releases ship a **BPS patch**, not a ROM. You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

1. Download the `.bps` file from [Releases](../../releases).
2. Apply it to your clean ROM with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) (in the browser),
   Floating IPS, or `py tools/patch/bps.py apply <firered.gba> <patch.bps> <out.gba>`. The patcher checks your ROM
   first and refuses any other one, including an already patched ROM.
3. Play the result in any GBA emulator or flashcart, with the save type at 128 KB flash (emulators pick it from the
   game code, which stays FireRed's).

Saves carry over between releases unless the release notes say otherwise. Back up your save before updating. A
vanilla FireRed save loads too; once you save in Gunk's FireRed, it no longer loads in vanilla.

**PokeDaisy users:** the companion app addresses game memory directly. Use a PokeDaisy build that lists this
exact release, or turn the companion off; a mismatched build could crash the game.

## Build it

Follow pret's [`INSTALL.md`](INSTALL.md), then run `make`. A clean build reproduces the release ROM, and
`tools/patch/bps.py make` makes the patch from it. [`docs/ENGINE.md`](docs/ENGINE.md) says why this hack uses the
decompilation.

## Credits

- [pret](https://github.com/pret/pokefirered) for the FireRed decompilation this hack is built on, and
  [agbcc](https://github.com/pret/agbcc).
- The DexNav idea comes from later Pokémon games and fan hacks; ghoulslash's DexNav for
  [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) was the reference for its design.
- The Repel prompt follows the one in [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion),
  and Quick Ball follows its `B_LAST_USED_BALL` and `B_LAST_USED_BALL_CYCLE`.
- [MinimalEffort07/pokefirered](https://github.com/MinimalEffort07/pokefirered): the follower's movement (walkable
  tiles, catching up, swapping places, making way at ledges and shores) is ported from its Walk With Pokémon
  feature, and it showed that FireRed's unused shaking-grass field effect and SaveBlock1's unused bytes are free.
- The follower sprites come from [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion),
  originally from aarant's [followers branch](https://github.com/aarant/pokeemerald/tree/followers-expanded-id),
  and the artists credited there.

Pokémon is © Nintendo, Creatures Inc. and GAME FREAK inc. This is a non-commercial fan project and contains
no ROM data; you need your own legally dumped copy of the game.
