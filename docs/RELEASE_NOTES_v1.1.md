<!-- DRAFT, not published: waits for the user's yes. Release title: Pokémon Gunk's FireRed Version v1.1
Asset: pokemon-gunks-firered-v1.1.bps -->

Quick Run, Quick Ball and a reworked DexNav for Pokémon Gunk's FireRed Version.

## New

- **Quick Run**: press R in a battle's action menu to run, exactly as choosing RUN does.
- **Quick Ball**: in wild battles where you can catch, the bottom left of the battle screen shows a ball and how
  many you have. Tap L to throw it; hold L and press Left or Right to pick another ball. It starts on the last ball
  you threw. In the battle menu, L and R no longer open Help.

## DexNav changes

- A search now lasts 10 seconds. If you don't reach the patch in time, the Pokémon gets away and the patch clears.
- The patch keeps shaking, twice a second, until you reach it or it gets away.
- The chain: a wild encounter with a different species resets it, one with the same species keeps it, and running
  from a DexNav battle no longer breaks it.

## Patch it

You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

Apply `pokemon-gunks-firered-v1.1.bps` with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), Floating
IPS, or `py tools/patch/bps.py apply`. Patch the clean retail ROM, not your v1.0 ROM. The patcher refuses any other
ROM. The patched ROM should be:

```
sha1: b852a9774ac46bb0e08051a5c144d437a2de76fd
```

## Notes

- Saves from v1.0 carry over: the save layout is unchanged. A vanilla FireRed save still loads, with its 14 boxes
  converted to 16. Back up your save anyway.
- Tested in the emulator before release: the save-safety suite (power cuts, torn writes, damaged slots), every
  feature check, the 16-box tests, new Quick Ball checks (including a catch that PKHeX finds legal) and DexNav rule
  checks. Tanoby Unown were also checked with PKHeX: all legal.
- Quick Ball follows pokeemerald-expansion's `B_LAST_USED_BALL` and `B_LAST_USED_BALL_CYCLE`.
