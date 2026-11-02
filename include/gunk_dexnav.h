#ifndef GUARD_GUNK_DEXNAV_H
#define GUARD_GUNK_DEXNAV_H

// Gunk's DexNav, see src/gunk_dexnav.c
void Gunk_DexNavPrepareList(void);
u8 Gunk_DexNavListCount(void);
const u8 *Gunk_DexNavListLabel(u8 i);
void Gunk_DexNavStartSearch(void);
void Gunk_DexNavUpdate(void);
bool8 Gunk_DexNavTryStartBattle(void);
void Gunk_DexNavOnBattleEnd(void);

#endif // GUARD_GUNK_DEXNAV_H
