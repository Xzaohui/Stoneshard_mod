// Explicit developer action: no path walking, travel time or spell cost.
if (!global.EAO_dev_enabled || !instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue)) exit;
var _player = instance_find(o_player,0);
if (_player.HP <= 0 || instance_exists(o_dungeon_controller)) exit;
if (!ds_list_empty(_player.lock_turn) || scr_unitTurnGetTime()) {
    scr_actionsLogAddMessage(global.language == 3 ? "开发传送：请等待当前动作结束。" : "DEV teleport: wait for the current action to finish.");
    exit;
}
var _home = keyboard_check(vk_shift) || keyboard_check_pressed(vk_shift);
var _x = -1;
var _y = -1;
if (_home) {
    if (!ds_map_exists(global.characterDataMap,"EAO_dev_warp_origin_room")) {
        scr_actionsLogAddMessage(global.language == 3 ? "尚未记录开发传送出发点。" : "No developer departure point has been recorded.");
        exit;
    }
    _x = ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_grid_x");
    _y = ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_grid_y");
} else {
    // Windows development-only modal; empty/Cancel is always a no-op.
    var _text = get_string(global.language == 3 ? "开发传送：输入世界坐标 x,y（如 41,37）。留空取消。" : "DEV teleport: world coordinates x,y (e.g. 41,37). Empty cancels.", "");
    _text = string_replace_all(_text," ","");
    if (_text == "") exit;
    var _comma = string_pos(",",_text);
    var _length = string_length(_text);
    if (_length > 9 || _comma <= 1 || _comma >= _length) {
        scr_actionsLogAddMessage(global.language == 3 ? "坐标格式应为两个非负整数：x,y。" : "Use two non-negative integers: x,y.");
        exit;
    }
    var _left = string_copy(_text,1,_comma-1);
    var _right = string_copy(_text,_comma+1,_length-_comma);
    if (string_digits(_left) != _left || string_digits(_right) != _right) {
        scr_actionsLogAddMessage(global.language == 3 ? "坐标格式应为两个非负整数：x,y。" : "Use two non-negative integers: x,y.");
        exit;
    }
    _x = real(_left);
    _y = real(_right);
}
// Bounds BEFORE calling native grid lookup. The executor revalidates the tile.
if (_x < 0 || _y < 0 || _x >= global.worldWidth || _y >= global.worldHeight) {
    scr_actionsLogAddMessage(global.language == 3 ? "目标超出当前世界范围。" : "Target is outside the current world.");
    exit;
}
ds_map_set(global.characterDataMap,"EAO_test_teleport_enabled",1);
ds_map_set(global.characterDataMap,"EAO_test_map_x",_x);
ds_map_set(global.characterDataMap,"EAO_test_map_y",_y);
ds_map_set(global.characterDataMap,"EAO_test_map_home",_home);
ds_map_set(global.characterDataMap,"EAO_test_map_pending",1);
