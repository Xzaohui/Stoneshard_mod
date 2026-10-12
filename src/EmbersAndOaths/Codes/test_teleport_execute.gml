if (!ds_map_exists(global.characterDataMap, "EAO_test_map_pending") || ds_map_find_value(global.characterDataMap, "EAO_test_map_pending") != 1) exit;
if (ds_map_find_value(global.characterDataMap, "EAO_test_teleport_enabled") != 1) { ds_map_set(global.characterDataMap, "EAO_test_map_pending", 0); exit; }
var _player = instance_find(o_player, 0);
if (_player.HP <= 0 || instance_exists(o_dungeon_controller) || scr_getAgredMobsCount(false, false, true) != 0) {
    ds_map_set(global.characterDataMap, "EAO_test_map_pending", 0);
    scr_actionsLogAddMessage(global.language == 3 ? "当前不能测试传送，请在战斗外的地表或室内使用。" : "Test teleport is unavailable in combat or a dungeon.");
    exit;
}
if (instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue)) exit;
// Close through the original journal/map exit before waiting for turn locks.
if (instance_exists(o_globalmap)) {
    if (instance_exists(o_journal)) { with (o_journal) event_user(2); }
    else { with (o_globalmap) event_user(15); }
    exit;
}
if (!ds_list_empty(_player.lock_turn) || scr_unitTurnGetTime()) exit;
var _target_x = ds_map_find_value(global.characterDataMap, "EAO_test_map_x");
var _target_y = ds_map_find_value(global.characterDataMap, "EAO_test_map_y");
var _target_room = scr_globaltile_get_room(_target_x, _target_y);
ds_map_set(global.characterDataMap, "EAO_test_map_pending", 0);
if (scr_globalmapIsBorder(_target_x, _target_y) || !room_exists(_target_room)) exit;
// Re-clicking the current tile also reloads it, so a stranded 0.2.2 player
// can recover through the native transition without editing a save file.
// Save the source first, then commit coordinates in our private changer event.
var _changer = scr_smoothRoomChange(_target_room, [4, 10], -1, true);
if (instance_exists(_changer)) {
    ds_map_set(global.characterDataMap, "EAO_test_map_commit", 1);
    ds_map_set(global.characterDataMap, "EAO_test_map_restore", 0);
    ds_map_set(global.characterDataMap, "EAO_test_map_source_room", room_get_name(room));
    ds_map_set(global.characterDataMap, "EAO_test_map_source_x", _player.x);
    ds_map_set(global.characterDataMap, "EAO_test_map_source_y", _player.y);
    ds_map_set(global.characterDataMap, "EAO_test_map_source_grid_x", global.playerGridX);
    ds_map_set(global.characterDataMap, "EAO_test_map_source_grid_y", global.playerGridY);
}
