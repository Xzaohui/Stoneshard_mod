// This native confirm-panel child remains present until every triggering
// key/button is released, so the input cannot reach world movement/skills.
if (!global.EAO_dev_enabled || !instance_exists(eao_coord_owner)
    || !instance_exists(o_player) || instance_exists(o_smoothRoomChanger)
    || global.characterDataMap!=eao_coord_character) {
    event_user(1); instance_destroy(); exit;
}
// Rebuild only if the native GUI size changed; this also positions the child
// buttons and preserves their native hit areas when the display is resized.
scr_guiLayoutOffsetUpdate(id,(global.cameraWidth-sprite_width)/2,(global.cameraHeight-sprite_height)/2);
if(eao_coord_closing) {
    if(!keyboard_check(vk_anykey) && !mouse_check_button(mb_any)) instance_destroy();
    exit;
}
if(!keyboard_check(vk_f8)) eao_coord_armed=true;
if(eao_coord_armed && keyboard_check_pressed(vk_f8)) { event_user(1); exit; }
// Backspace is handled by GameMaker's text buffer. Ctrl+A explicitly clears
// this small coordinate entry, without touching a native player's key map.
if(keyboard_check(vk_control) && keyboard_check_pressed(ord("A"))) keyboard_string="";
eao_coord_text=keyboard_string;
// Shorten only the display. The parser must see the complete input, including
// an invalid suffix after a long run of spaces; truncation could make it valid.
var _shown=string_copy(eao_coord_text,1,20)+(string_length(eao_coord_text)>20 ? "..." : "");
addText=(eao_coord_text=="" ? (global.language==3 ? "输入坐标；Enter确认，Esc取消" : "Type x,y; Enter accepts, Esc cancels") : _shown+" |")
    +(eao_coord_error=="" ? "" : "\n"+eao_coord_error);
if(eao_coord_armed && keyboard_check_pressed(vk_return)) event_user(2);
