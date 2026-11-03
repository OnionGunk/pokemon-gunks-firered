First release of Pokémon Gunk's FireRed Version: FireRed with the grind and friction taken out, the story and
difficulty kept as they are.

## Features

- **DexNav**: a key item that lists the grass Pokémon of the place you're in. Pick one and it hides in rustling
  grass nearby. Search levels and chains raise the odds of good IVs and shinies; every Pokémon it finds is a
  normal, legal wild roll for that spot.
- **Following Pokémon**: your lead Pokémon walks behind you, any of the 386 species, shinies in their shiny colors.
  Walk into it to swap places. RETURN in its party menu puts it away, WALK brings it back.
- **16 PC boxes** instead of 14.
- **Faster play**: instant text, a faster EXP bar, auto-run (hold B to walk), eggs that hatch twice as fast.
- **Items**: reusable TMs, two registered items (SELECT and R), bag sorting (START in the bag), a prompt to use
  another Repel when one runs out, and an Endless Repel you switch on and off.
- **Pokémon**: IV and EV view in the summary (A on the SKILLS page), Exp. All, vitamins up to 252 EVs, trade
  evolutions without trading, HM moves without teaching them, and a free Move Tutor on every Pokémon Center PC.
- **Save safety**: a save slot only loads if all of it comes from one save.

Professor Oak gives the Endless Repel, the Exp. All and the DexNav with the Pokédex, when you bring him his
parcel: before the first gym. On a save that is already past that, Mom has them.

## Patch it

You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

Apply `pokemon-gunks-firered-v1.0.bps` with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), Floating
IPS, or `py tools/patch/bps.py apply`. Patch the clean retail ROM. The patcher refuses any other ROM. The patched
ROM should be:

```
sha1: dc08dd0551dd92ddd2e962cc08d79aff108e5cc4
```

## Notes

- **Saves from vanilla FireRed load.** Their 14 PC boxes are converted to the new 16-box format the first time
  they load, with box names, wallpapers and every Pokémon kept; boxes 15 and 16 start empty. Once you save in Gunk's
  FireRed, that save won't load in vanilla FireRed any more. Back up your save first.
- Tested in the emulator before release:
  - save safety: power cuts across the whole save write, torn writes at every sector, and damaged slots;
  - every feature;
  - a vanilla save with 420 boxed Pokémon converting byte for byte;
  - every map's arrival with a follower out;
  - all 256 story triggers, compared with vanilla;
  - the eight gyms through the Champion, the Hall of Fame and the credits;
  - a PKHeX legality check: 27 caught Pokémon, from random encounters, DexNav searches and chains to a shiny,
    were all legal, and so were their PC-box copies.
- Credits: pret's pokefirered decompilation; the DexNav after ghoulslash's design in pokeemerald-expansion;
  following Pokémon from MinimalEffort07's pokefirered, with sprites from pokeemerald-expansion.
