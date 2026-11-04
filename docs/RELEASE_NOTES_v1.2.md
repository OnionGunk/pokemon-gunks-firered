Talk to your follower, Quick Run, Quick Ball and a reworked DexNav for Pokémon Gunk's FireRed Version.

## New

- **Talk to your follower**: face the Pokémon walking behind you and press A. It answers with a line that depends on
  how it feels: worn out when its HP is under a quarter, otherwise by how much it likes you, from wary to devoted.
- **Quick Run**: press R in a battle's action menu to run, exactly as choosing RUN does.
- **Quick Ball**: in wild battles where you can catch, the bottom left of the battle screen shows a ball and how
  many you have. Tap L to throw it; hold L and press Left or Right to pick another ball. It starts on the last ball
  you threw. In the battle menu, L and R no longer open Help.

## DexNav changes

- A search now lasts 10 seconds. If you don't reach the patch in time, the Pokémon gets away and the patch clears.
- The patch keeps shaking, twice a second, until you reach it or it gets away.
- The chain: a wild encounter with a different species resets it, and one with the same species keeps it.
  Running from a DexNav battle (Run, Teleport or a Poké Doll) resets it to 0 and doesn't raise that species'
  search level.
- With a high search level and a long chain, stepping onto the patch no longer freezes the game for half a second.

## Patch it

You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

Apply `pokemon-gunks-firered-v1.2.bps` with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), Floating
IPS, or `py tools/patch/bps.py apply`. Patch the clean retail ROM, not your v1.0 ROM. The patcher refuses any other
ROM. The patched ROM should be:

```
sha1: f13d86c6d5870be760d87ec58aa21c93a712aa68
```

## Notes

- Saves from v1.0 carry over: the save layout is unchanged. A vanilla FireRed save still loads, with its 14 boxes
  converted to 16. Back up your save anyway.
- Tested in the emulator before release: the story sweep (every story trigger, and every story conversation with a
  person, played on both this ROM and vanilla FireRed, with the same outcomes), the story milestones from Brock to
  the credits, the save-safety suite (power cuts, torn writes, damaged slots), every feature check, the 16-box
  tests, Quick Ball and DexNav rule checks, follower talk checks, and a room whose objects fill every slot. 50
  caught and DexNav Pokémon and 28 Tanoby Unown were checked with PKHeX: all legal.
- In Lorelei's house on Four Island, once all her dolls are out, the room has no space left for your follower: it
  waits outside and is back when you leave.
- Quick Ball follows pokeemerald-expansion's `B_LAST_USED_BALL` and `B_LAST_USED_BALL_CYCLE`.
