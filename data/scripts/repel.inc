@ Gunk's: when a Repel wears off and the bag still holds one of the same kind, offer to use it.
@ The Endless Repel covers for a worn-off Repel, so it skips the prompt.
EventScript_RepelWoreOff::
	goto_if_set FLAG_GUNK_ENDLESS_REPEL_ON, EventScript_RepelWoreOffMessage
	checkitem VAR_GUNK_LAST_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, EventScript_RepelWoreOffMessage
	lockall
	bufferitemname STR_VAR_1, VAR_GUNK_LAST_REPEL
	msgbox Text_RepelWoreOffUseAnother, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_RepelWoreOffDone
	removeitem VAR_GUNK_LAST_REPEL, 1
	special Gunk_RestartRepel
	playse SE_REPEL
	msgbox Text_UsedAnotherRepel
	waitse
EventScript_RepelWoreOffDone::
	closemessage
	releaseall
	end

EventScript_RepelWoreOffMessage::
	msgbox Text_RepelWoreOff, MSGBOX_SIGN
	end

Text_RepelWoreOff::
	.string "REPEL's effect wore off…$"

Text_RepelWoreOffUseAnother::
	.string "REPEL's effect wore off…\n"
	.string "Use another {STR_VAR_1}?$"

Text_UsedAnotherRepel::
	.string "{PLAYER} used the\n"
	.string "{STR_VAR_1}.$"
