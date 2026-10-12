// Initialize the actual native unit / simple NPC, including render and input state.
event_inherited();
name = global.language == 3 ? "路誓行会信使" : "Roadsworn courier";
id_name = "";
dialog_id = "eao_mq01";
avatar = s_peasantmale_13P;
isStaticSave = false;
is_simple = true;
ai_is_on = false;
idle_state = false;
show_town = false;
show_faction = false;
can_talk = true;
can_give_contract = false;
// Use the native interactive mask registration, with the displayed sprite.
scr_unit_interactive_init(sprite_index, sprite_index);

