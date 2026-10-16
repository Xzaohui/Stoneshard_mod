// Owned child of the native prairie generator, User 8 (preset phase).
// The native 90x90 grass/road/wildlife generator and its later player creation
// stay in charge. No live player, arrival coordinates or quest state is changed.
event_inherited();
if (room != r_eao_n2_world) exit;

// Keep the forecourt clear through native flora, grow and mob placement passes.
// This grid only reserves generation space; the ground remains walkable grass.
ds_grid_set_region(markerCollisionGrid, 23, 34, 67, 48, 1);

// Building footprints, independently authored in grid cells. Only the footprint
// blocks movement; there is no rectangular wall or water moat around the area.
var _footprints = [[25,37,33,41], [42,38,48,41], [57,37,65,41]];
for (var _i = 0; _i < array_length(_footprints); _i++) {
    var _rect = _footprints[_i];
    for (var _x = _rect[0]; _x <= _rect[2]; _x++)
        for (var _y = _rect[1]; _y <= _rect[3]; _y++)
            instance_create_depth(_x * 26, _y * 26, 0, o_hut_wall);
}
var _facades = [o_eao_site_building_shed, o_eao_site_building_winch, o_eao_site_building_canal];
var _doors = [o_eao_site_door_shed, o_eao_site_door_winch, o_eao_site_door_canal];
var _markers = [o_eao_site_start_shed, o_eao_site_start_winch, o_eao_site_start_canal];
var _columns = [29,45,61];
for (_i = 0; _i < 3; _i++) {
    var _px = _columns[_i] * 26 + 13;
    with (instance_create_depth(_px, 42 * 26 + 13, 0, _facades[_i])) scr_locationRoomEntityInitSavable(id, false);
    instance_create_depth(_px, 42 * 26 + 13, 0, _doors[_i]);
    with (instance_create_depth(_px, 44 * 26 + 13, 0, _markers[_i])) scr_locationRoomEntityInitSavable(id, false);
}
// Dialogues in the existing three interiors keep their own actors and state.
if (!instance_exists(o_dialog_controller)) instance_create_depth(0, 0, -4000, o_dialog_controller);
