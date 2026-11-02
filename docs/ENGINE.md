# Engine choice

Gunk's FireRed is built on **pret's `pokefirered` decompilation** (https://github.com/pret/pokefirered),
compiled with **agbcc** (https://github.com/pret/agbcc) and the arm-none-eabi binutils.

## The options

| Base | Full source | Reproducible build | Notes |
|---|---|---|---|
| pret `pokefirered` | Yes, 100 % decompiled C | Yes: a clean build matches the retail ROM byte for byte (sha1 `41cb23d8…`) | Same decomp the LeafGreen sibling uses (`make leafgreen`). |
| FRLG-capable expansion (rh-hideout family) | Yes | Builds, but never matches retail | Brings a modern battle engine (Gen 9 mechanics, new species and moves). That changes battles and difficulty, which Gunk's hacks don't do, and it changes the save layout. |
| FireRed Engine Upgrade (CFRU) | No: C/asm inserted into a retail ROM with a Python inserter | Only as a binary insertion into a ROM, with free-space offsets | It also changes battle mechanics by default. It can't produce a vanilla build to compare with, and the repo would hold a patch toolchain, not the game's source. |

## Why pokefirered

- **Save safety first.** With the vanilla game's source we can see exactly what each save block holds
  (`include/global.h`, `src/save.c`) and prove a change leaves the layout alone. A vanilla build that matches the
  retail sha1 is the control for every save test.
- **No difficulty or story changes.** The decomp is the vanilla game, so nothing changes unless we change it.
  The expansion and CFRU both bring new battle mechanics by default.
- **Reproducible.** Anyone with their own FireRed (USA) 1.0 dump can build from the repo. `make compare` checks
  the toolchain first.
- **Shared with LeafGreen.** Both hacks use the same decomp, so the code can be shared through their public repos.

DexNav and following Pokémon are not in the decomp. We port them from the open implementations in the expansion
projects and credit them (see the README).

## Base ROM

`baserom.gba` = Pokémon FireRed Version (USA) 1.0, sha1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
(`firered.sha1`). Gitignored, never committed.
