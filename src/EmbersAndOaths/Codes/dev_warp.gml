// Explicit developer action: no path walking, travel time or spell cost.
if(!dev_coord_submitting && instance_exists(o_eao_dev_coordinates)) exit;
dev_coord_queued=false;
dev_coord_error=global.language==3 ? "当前不可传送，请先结束动作。" : "Finish the current action first.";
if (!global.EAO_dev_enabled || !instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue)) exit;
var _player = instance_find(o_player,0);
if (_player.HP <= 0 || instance_exists(o_dungeon_controller)) exit;
if (!ds_list_empty(_player.lock_turn) || scr_unitTurnGetTime()) {
    scr_actionsLogAddMessage(global.language == 3 ? "开发传送：请等待当前动作结束。" : "DEV teleport: wait for the current action to finish.");
    exit;
}
var _home = !dev_coord_submitting && (keyboard_check(vk_shift) || keyboard_check_pressed(vk_shift));
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
    if(!dev_coord_submitting) {
        // Parentage is part of can_press's native movement/skill gate. Never
        // nest this editor inside another native confirmation dialog.
        if(instance_exists(o_confirm_panel)) exit;
        var _input=scr_guiCreateContainer(global.guiBaseContainerVisible,o_eao_dev_coordinates);
        _input.eao_coord_owner=id;
        exit;
    }
    var _text = dev_coord_text;
    _text = string_replace_all(_text," ","");
    if (_text == "") { dev_coord_error=global.language==3 ? "请输入 x,y；Esc取消。" : "Enter x,y; Esc cancels."; exit; }
    var _comma = string_pos(",",_text);
    var _length = string_length(_text);
    if (_length > 9 || _comma <= 1 || _comma >= _length) {
        dev_coord_error=global.language==3 ? "格式：两个非负整数 x,y" : "Use two non-negative integers: x,y";
        exit;
    }
    var _left = string_copy(_text,1,_comma-1);
    var _right = string_copy(_text,_comma+1,_length-_comma);
    if (string_digits(_left) != _left || string_digits(_right) != _right) {
        dev_coord_error=global.language==3 ? "格式：两个非负整数 x,y" : "Use two non-negative integers: x,y";
        exit;
    }
    _x = real(_left);
    _y = real(_right);
}
// Bounds BEFORE calling native grid lookup. The executor revalidates the tile.
if (_x < 0 || _y < 0 || _x >= global.worldWidth || _y >= global.worldHeight) {
    dev_coord_error=global.language==3 ? "目标超出当前世界范围。" : "Target is outside the current world.";
    exit;
}
ds_map_set(global.characterDataMap,"EAO_test_teleport_enabled",1);
ds_map_set(global.characterDataMap,"EAO_test_map_x",_x);
ds_map_set(global.characterDataMap,"EAO_test_map_y",_y);
ds_map_set(global.characterDataMap,"EAO_test_map_home",_home);
ds_map_set(global.characterDataMap,"EAO_test_map_pending",1);
dev_coord_error="";
dev_coord_queued=true;
