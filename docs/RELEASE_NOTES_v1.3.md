<!-- DRAFT, not published: waits for the user's yes. Release title: Pokémon Gunk's FireRed Version v1.3
Asset: pokemon-gunks-firered-v1.3.bps. The patched sha1 and the test counts get filled in from the final build. -->

A real DexNav screen, Surf searches and a search bar for Pokémon Gunk's FireRed Version.

## New

- **The DexNav screen.** Use the DexNav (from the Bag, or SELECT once registered) and a full screen opens for the
  place you're in:
  - a title bar with the area's name and how many of its Pokémon you've caught;
  - LAND, WATER and OTHER tabs (switch with L/R), each a grid of that area's Pokémon: an icon once you've seen it,
    "?" before that, a ball mark once caught. OTHER lists the Pokémon you fish for or find with Rock Smash;
  - an info panel for the highlighted Pokémon: name and status, how it's found (tall grass, surfing, Old, Good or
    Super Rod, Rock Smash), its level range, search level and chain.

  Pick a grass or water Pokémon you've seen to search for it. You can't search for one you haven't seen yet, and
  the OTHER tab is for reference: it tells you which rod or Rock Smash finds each one.
- **Surf searches.** Water Pokémon hide in a patch of rippling water nearby. Surf onto it within 10 seconds to
  battle it.
- **The search bar.** While a search runs, a bar across the top of the screen shows the Pokémon that's hiding:
  name and level, a shiny mark, its search level and chain, nature, ability, a gold star for each perfect IV, and
  what it holds. The Pokémon you battle is exactly the one the bar shows.
- **Held items from searches.** A searched Pokémon can hold its species' own wild items, and the odds grow with
  the search level and chain: from 50% and 5% (the usual odds) up to 75% for the common item and 20% for the rare
  one.
- **Follower reactions.** Talk to your follower and it reacts by mood, with an emote, its cry or both; a note
  shows when it's steady and dots when it's tired. It goes back into its ball while you surf and during story
  scenes, and comes out again after.

## Notes

- Saves from v1.0 and v1.2 carry over: the save layout is unchanged.
- The DexNav now picks the Pokémon when the search starts, instead of when you step into the patch. The odds are
  the same: search levels and chains add rolls, and the best one is kept, a shiny first.
- In this hack, L/R open the DexNav screen's tabs, so FireRed's L/R Help is off while the screen is open.
- A GBA has one screen, so there's no second-screen DexNav view.

## Patch it

You need your own dump of **Pokémon FireRed (USA) 1.0**:

```
sha1: 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc
```

Apply `pokemon-gunks-firered-v1.3.bps` with [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/), Floating
IPS, or `py tools/patch/bps.py apply`. Patch the clean retail ROM. The patcher refuses any other ROM. The patched
ROM should be:

```
sha1: (filled in from the final build)
```
