if (!instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue)) exit;
if (global.EAO_dev_enabled) event_user(0);
else {
    global.EAO_dev_enabled = true;
    dev_character_map = global.characterDataMap;
    ds_map_set(global.characterDataMap,"EAO_test_teleport_enabled",1);
    scr_actionsLogAddMessage(global.language == 3 ? "开发模式：F8坐标直达 地图左键传送 Shift+F8回出发点 F7迷雾 F9格网 F6关闭。" : "DEV: F8 coordinates, map left-click warp, Shift+F8 departure, F7 fog, F9 grid, F6 off.");
}
