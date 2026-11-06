# Pokémon Gunk's FireRed Version

A quality-of-life hack of Pokémon FireRed, built on [pret's FireRed decompilation](https://github.com/pret/pokefirered).
It keeps the game's difficulty and story as they are and takes the grind and friction out, for long playthroughs.

## Features

- **DexNav.** A key item (use it from the Bag or register it to SELECT) that opens the DexNav screen for the place
  you're in:
  - a title bar with the area's name and how many of its Pokémon you've caught;
  - LAND and WATER tabs (switch with L/R), each a grid of the area's grass or surfing Pokémon: an icon once seen,
    "?" before that, a ball mark once caught;
  - an info panel for the highlighted Pokémon: name and status, where it's found, its level range, search level
    and chain.

  Pick a Pokémon you've seen and it hides nearby, in a patch of rustling grass or rippling water. Step (or Surf)
  into the patch within 10 seconds to battle it. While you look, a bar at the top of the screen shows what's
  hiding: name, level, a shiny mark, nature, ability and a gold star for each perfect IV. Every Pokémon it finds
  is a legal wild roll for that spot. Search levels and chains raise the odds of good IVs and shinies. A GBA has
  one screen, so there's no second-screen DexNav view.
- **Pokémon follow you.** Your lead Pokémon walks behind you, any of the 386 species, shinies in their shiny
  colors. Walk into it to swap places; it waits on the shore while you Surf and hops down ledges after you.
  RETURN in its party menu puts it away, WALK brings it back.
- **Faster play:** instant text, a faster EXP bar, auto-run (hold B to walk), eggs that hatch twice as fast.
- **Items:** reusable TMs, two registered items (SELECT and R), bag sorting (START in the bag), a prompt to use
  another Repel when one runs out, and an Endless Repel you switch on and off.
- **Pokémon:** IV and EV view in the summary (A on the SKILLS page), Exp. All (half the EXP and the EVs for the
  Pokémon that didn't battle), vitamins up to 252 EVs, and trade evolutions without trading. HM moves work without
  teaching the move, and every PC has a free Move Tutor that remembers and forgets moves.
- **16 PC boxes** instead of 14. A save from vanilla FireRed loads, with its boxes kept.
- **Quick Run and Quick Ball:** in battle, R runs and L throws your last-used ball (hold L and press Left/Right
  to pick another). A small icon shows which ball and how many are left.
- **Save safety:** an extra check when loading, so a save slot can only load if all of it comes from one save.

Professor Oak gives the Endless Repel, the Exp. All and the DexNav with the Pokédex, when you bring him his
parcel: before the first gym. On a save that is already past that, Mom has them.

Save safety comes first: every build passes an emulator test suite that covers save cycles, power cuts at points
across the flash write, torn writes at every sector, and recovery from a damaged save slot.

### Save safety

FireRed keeps two save slots and writes the older one each time, so a power cut while saving falls back to
the previous save. The test suite confirms this for vanilla and for Gunk's FireRed: power cuts at 12 points
across the flash write, and torn writes at every one of the 14 sectors, all load the previous save.

Gunk's FireRed adds one more check. Vanilla accepts a slot when each of its 14 sectors has a good checksum;
Gunk's also requires all 14 to carry the same save counter. A normal power cut can't produce a slot that
fails only that check, but a slot holding sectors from two different saves now falls back to the other slot
instead of loading as a mix (the suite's "mixed" test builds one).

## Play it

Releases ship a **BPS patch**, not a ROM. You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

1. Download the `.bps` file from [Releases](../../releases).
2. Apply it to your clean ROM with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) (in the browser),
   Floating IPS, or `py tools/patch/bps.py apply <firered.gba> <patch.bps> <out.gba>`. The patcher checks your ROM
   first and refuses any other one, including an already patched ROM: always patch the clean retail ROM.
3. Check the result against the patched sha1 in the release notes, then play it in any GBA emulator or flashcart.
   Keep the save type at 128 KB flash (emulators pick it from the game code, which stays FireRed's).

Saves carry over between releases unless the release notes say otherwise. Back up your save before updating.
A vanilla FireRed save loads in Gunk's FireRed: its 14 boxes are converted to the 16-box format the first time it
loads (names and wallpapers kept, boxes 15 and 16 empty). After you save in Gunk's FireRed, that save no longer
loads in vanilla FireRed.

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
- Quick Ball follows pokeemerald-expansion's `B_LAST_USED_BALL` and `B_LAST_USED_BALL_CYCLE`.
- [MinimalEffort07/pokefirered](https://github.com/MinimalEffort07/pokefirered): the follower's movement (walkable
  tiles, catching up, swapping places, making way at ledges and shores) is ported from its Walk With Pokémon
  feature, and it showed that FireRed's unused shaking-grass field effect and SaveBlock1's unused bytes are free.
- The follower sprites come from [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion),
  originally from aarant's [followers branch](https://github.com/aarant/pokeemerald/tree/followers-expanded-id),
  and the artists credited there.

Pokémon is © Nintendo, Creatures Inc. and GAME FREAK inc. This is a non-commercial fan project and contains
no ROM data; you need your own legally dumped copy of the game.
