if (!global.EAO_dev_enabled) exit;
if (variable_global_exists("characterDataMap") && global.characterDataMap != dev_character_map) { event_user(0); exit; }
if (!instance_exists(o_player) && !instance_exists(o_smoothRoomChanger) && !instance_exists(o_abstract_player) && !instance_exists(o_fastTurnController)) { event_user(0); exit; }
if (dev_reveal && variable_global_exists("fog")) {
    if (!dev_fog_owned) { dev_fog_before = global.fog; dev_fog_owned = true; }
    global.fog = false;
} else if (dev_fog_owned) {
    global.fog = dev_fog_before;
    dev_fog_owned = false;
}
with (o_globalmapFogRender) {
    if (other.dev_reveal) {
        if (!variable_instance_exists(id,"EAO_dev_visible_owned") || !EAO_dev_visible_owned) EAO_dev_visible_before = visible;
        EAO_dev_visible_owned = true;
        visible = false;
    } else if (variable_instance_exists(id,"EAO_dev_visible_owned") && EAO_dev_visible_owned) {
        visible = EAO_dev_visible_before;
        EAO_dev_visible_owned = false;
    }
}
