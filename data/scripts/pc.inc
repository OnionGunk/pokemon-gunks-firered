EventScript_PC::
	goto_if_questlog EventScript_ReleaseEnd
	lockall
	goto_if_set FLAG_SYS_PC_STORAGE_DISABLED, EventScript_PCDisabled
	setvar VAR_0x8004, HELPCONTEXT_PC
	special Script_SetHelpContext
	setvar VAR_0x8004, 0
	special AnimatePcTurnOn
	playse SE_PC_ON
	msgbox Text_BootedUpPC
	goto EventScript_PCMainMenu
	end

@ For when the player first arrives on One Island
EventScript_PCDisabled::
	msgbox OneIsland_PokemonCenter_1F_Text_UsualPCServicesUnavailable
	releaseall
	end

EventScript_PCMainMenu::
	message Text_AccessWhichPC
	waitmessage
	special CreatePCMenu
	waitstate
	special Gunk_TranslatePCMenuResult
	goto EventScript_ChoosePCMenu
	end

EventScript_ChoosePCMenu::
	switch VAR_RESULT
	case 0, EventScript_AccessPokemonStorage
	case 1, EventScript_AccessPlayersPC
	case 2, EventScript_AccessProfOaksPC
	case 3, EventScript_AccessHallOfFame
	case 4, EventScript_TurnOffPC
	case 5, EventScript_GunkMoveTutor
	case SCR_MENU_CANCEL, EventScript_TurnOffPC
	end

@ Gunk's: a free Move Tutor on every PC. It remembers level-up moves (like the Move Maniac on Two Island)
@ and forgets moves (like the Move Deleter in Fuchsia City).
EventScript_GunkMoveTutor::
	playse SE_PC_LOGIN
	msgbox Text_GunkMoveTutorRemember, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, EventScript_GunkMoveTutorChooseMonRemember
	msgbox Text_GunkMoveTutorForget, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, EventScript_GunkMoveTutorChooseMonForget
	goto EventScript_PCMainMenu
	end

EventScript_GunkMoveTutorChooseMonRemember::
	msgbox Text_GunkMoveTutorWhichMonRemember
	special ChooseMonForMoveRelearner
	waitstate
	goto_if_ge VAR_0x8004, PARTY_SIZE, EventScript_PCMainMenu
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, EventScript_GunkMoveTutorEggRemember
	goto_if_eq VAR_0x8005, 0, EventScript_GunkMoveTutorNoMoves
	msgbox Text_GunkMoveTutorWhichMoveRemember
	special TeachMoveRelearnerMove
	waitstate
	goto_if_eq VAR_0x8004, 0, EventScript_GunkMoveTutorChooseMonRemember
	goto EventScript_PCMainMenu
	end

EventScript_GunkMoveTutorEggRemember::
	msgbox Text_GunkMoveTutorEgg
	goto EventScript_GunkMoveTutorChooseMonRemember
	end

EventScript_GunkMoveTutorNoMoves::
	msgbox Text_GunkMoveTutorNoMoves
	goto EventScript_GunkMoveTutorChooseMonRemember
	end

EventScript_GunkMoveTutorChooseMonForget::
	msgbox Text_GunkMoveTutorWhichMonForget
	special ChoosePartyMon
	waitstate
	goto_if_ge VAR_0x8004, PARTY_SIZE, EventScript_PCMainMenu
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, EventScript_GunkMoveTutorEggForget
	special GetNumMovesSelectedMonHas
	goto_if_eq VAR_RESULT, 1, EventScript_GunkMoveTutorOnlyMove
	msgbox Text_GunkMoveTutorWhichMoveForget
	fadescreen FADE_TO_BLACK
	special SelectMoveDeleterMove
	fadescreen FADE_FROM_BLACK
	goto_if_eq VAR_0x8005, MAX_MON_MOVES, EventScript_GunkMoveTutorChooseMonForget
	special BufferMoveDeleterNicknameAndMove
	msgbox Text_GunkMoveTutorConfirmForget, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_GunkMoveTutorChooseMonForget
	special MoveDeleterForgetMove
	playfanfare MUS_MOVE_DELETED
	waitfanfare
	msgbox Text_GunkMoveTutorForgotten
	goto EventScript_PCMainMenu
	end

EventScript_GunkMoveTutorEggForget::
	msgbox Text_GunkMoveTutorEgg
	goto EventScript_GunkMoveTutorChooseMonForget
	end

EventScript_GunkMoveTutorOnlyMove::
	special BufferMoveDeleterNicknameAndMove
	msgbox Text_GunkMoveTutorOnlyMove
	goto EventScript_GunkMoveTutorChooseMonForget
	end

Text_GunkMoveTutorRemember::
	.string "MOVE TUTOR: Should a POKéMON\n"
	.string "remember a move it used to know?$"

Text_GunkMoveTutorForget::
	.string "Should a POKéMON forget a move?$"

Text_GunkMoveTutorWhichMonRemember::
	.string "Which POKéMON should remember\n"
	.string "a move?$"

Text_GunkMoveTutorWhichMoveRemember::
	.string "Which move should it remember?$"

Text_GunkMoveTutorNoMoves::
	.string "That POKéMON has no move to\n"
	.string "remember.$"

Text_GunkMoveTutorEgg::
	.string "An EGG doesn't know any moves.$"

Text_GunkMoveTutorWhichMonForget::
	.string "Which POKéMON should forget\n"
	.string "a move?$"

Text_GunkMoveTutorWhichMoveForget::
	.string "Which move should be forgotten?$"

Text_GunkMoveTutorConfirmForget::
	.string "Should {STR_VAR_1} forget\n"
	.string "{STR_VAR_2}?$"

Text_GunkMoveTutorForgotten::
	.string "{STR_VAR_1} forgot {STR_VAR_2}.$"

Text_GunkMoveTutorOnlyMove::
	.string "{STR_VAR_1} only knows one move,\n"
	.string "so it can't forget it.$"

EventScript_AccessPlayersPC::
	playse SE_PC_LOGIN
	msgbox Text_AccessedPlayersPC
	special PlayerPC
	waitstate
	goto EventScript_PCMainMenu
	end

EventScript_AccessPokemonStorage::
	playse SE_PC_LOGIN
	call_if_unset FLAG_SYS_NOT_SOMEONES_PC, EventScript_AccessSomeonesPC
	call_if_set FLAG_SYS_NOT_SOMEONES_PC, EventScript_AccessBillsPC
	msgbox Text_OpenedPkmnStorage
	special ShowPokemonStorageSystemPC
	waitstate
	setvar VAR_0x8004, HELPCONTEXT_PC
	special Script_SetHelpContext
	goto EventScript_PCMainMenu
	end

EventScript_AccessSomeonesPC::
	msgbox Text_AccessedSomeonesPC
	return

EventScript_AccessBillsPC::
	msgbox Text_AccessedBillsPC
	return

EventScript_TurnOffPC::
	setvar VAR_0x8004, 0
	playse SE_PC_OFF
	special AnimatePcTurnOff
	special SetHelpContextForMap
	releaseall
	end

EventScript_AccessHallOfFame::
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_TurnOffPC
	playse SE_PC_LOGIN
	setvar VAR_0x8004, HELPCONTEXT_PC_MISC
	special BackupHelpContext
	special Script_SetHelpContext
	special HallOfFamePCBeginFade
	waitstate
	special RestoreHelpContext
	goto EventScript_ChoosePCMenu
	end

EventScript_AccessProfOaksPC::
	goto_if_unset FLAG_SYS_POKEDEX_GET, EventScript_TurnOffPC
	playse SE_PC_LOGIN
	msgbox Text_AccessedProfOaksPC
	msgbox Text_HavePokedexRated, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ExitOaksPC
	setflag FLAG_OAKS_RATING_IS_VIA_PC
	call PokedexRating_EventScript_Rate
	clearflag FLAG_OAKS_RATING_IS_VIA_PC
	goto EventScript_ExitOaksPC
	end

EventScript_ExitOaksPC::
	msgbox Text_ClosedLinkToProfOaksPC
	goto EventScript_PCMainMenu
	end
