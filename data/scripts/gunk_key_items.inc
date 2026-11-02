@ Gunk's: the Endless Repel and the Exp. All. Oak's aide hands them over with the Running Shoes in Pewter City;
@ on a save that is already past that, Mom has them.
PewterCity_EventScript_GunkAideGivesKeyItems::
	goto_if_set FLAG_GUNK_GOT_KEY_ITEMS, EventScript_GunkKeyItemsEnd
	msgbox Text_GunkAideAlsoGives
	goto EventScript_GunkGiveKeyItems

PalletTown_PlayersHouse_1F_EventScript_GunkMomGivesKeyItems::
	goto_if_set FLAG_GUNK_GOT_KEY_ITEMS, EventScript_GunkKeyItemsEnd
	msgbox Text_GunkMomHasKeyItems
EventScript_GunkGiveKeyItems::
	giveitem ITEM_ENDLESS_REPEL
	goto_if_eq VAR_RESULT, FALSE, EventScript_GunkKeyItemsEnd
	giveitem ITEM_EXP_ALL
	goto_if_eq VAR_RESULT, FALSE, EventScript_GunkKeyItemsEnd
	setflag FLAG_GUNK_EXP_ALL_ON
	setflag FLAG_GUNK_GOT_KEY_ITEMS
	msgbox Text_GunkExplainKeyItems
EventScript_GunkKeyItemsEnd::
	return

Text_GunkAideAlsoGives::
	.string "PROF. OAK also asked me to give\n"
	.string "you these two.$"

Text_GunkMomHasKeyItems::
	.string "Oh, {PLAYER}! PROF. OAK's AIDE\n"
	.string "left these for you.$"

Text_GunkExplainKeyItems::
	.string "The ENDLESS REPEL keeps weak wild\n"
	.string "POKéMON away for as long as it's on.\p"
	.string "With the EXP. ALL on, POKéMON that\n"
	.string "didn't battle get half the EXP.\p"
	.string "Use either one from the KEY ITEMS\n"
	.string "pocket to switch it on or off.$"
