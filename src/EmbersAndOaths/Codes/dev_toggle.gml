if (!instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue)) exit;
if (global.EAO_dev_enabled) event_user(0);
else {
    global.EAO_dev_enabled = true;
    dev_character_map = global.characterDataMap;
    scr_actionsLogAddMessage(global.language == 3 ? "开发观察：F7迷雾 F9格网 F10素材 F11场景 Shift+F11返回 F6关闭。" : "DEV: F7 fog, F9 grid, F10 art, F11 scenes, Shift+F11 return, F6 off.");
}
