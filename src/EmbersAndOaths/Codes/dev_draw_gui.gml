if (!global.EAO_dev_enabled || !dev_panel || !instance_exists(o_player) || instance_exists(o_eao_dev_coordinates)) exit;
// Player-relative inspection card, in the same visible draw pass as the grid.
var _matrix=matrix_get(matrix_world);
// The native outside-room black mask covers cards drawn beyond room bounds.
var _panel_x=clamp(o_player.x-450,0,max(0,room_width-450));
var _panel_y=clamp(o_player.y-235,0,max(0,room_height-368));
matrix_set(matrix_world,matrix_build(_panel_x,_panel_y,0,0,0,0,0.75,0.75,1));
var _font=draw_get_font();var _color=draw_get_color();var _alpha=draw_get_alpha();var _ha=draw_get_halign();var _va=draw_get_valign();
draw_set_font(global.f_dmg);draw_set_halign(fa_left);draw_set_valign(fa_top);
draw_set_alpha(0.82);draw_set_color(c_black);draw_rectangle(10,45,600,253,false);
draw_set_alpha(1);draw_set_color(c_yellow);
draw_text(18,51,global.language == 3 ? "EAO 开发 0.3.26 | F5 面板 | F6 关闭 | F8 坐标直达" : "EAO DEV 0.3.26 | F5 panel | F6 OFF | F8 coordinates");
draw_set_color(c_white);
draw_text(18,77,(global.language == 3 ? "F7 揭雾=" : "F7 reveal=")+string(dev_reveal)+(global.language == 3 ? "  F9 格网=" : "  F9 grid=")+string(dev_grid)+"  F10 HD2D="+string(global.EAO_dev_art));
draw_text(18,103,global.language == 3 ? "地图左键传送 | Shift+F8 回出发点 | F11 场景" : "Map left-click warp | Shift+F8 departure | F11 scenes");
draw_text(18,129,room_get_name(room)+" | cell "+string(floor(o_player.x/26))+","+string(floor(o_player.y/26))+" | world "+string(global.playerGridX)+","+string(global.playerGridY));
// Read-only native-door diagnostics. These never invoke a transition or change
// locks; they expose the logical cell independently of the displayed artwork.
var _door=instance_nearest(o_player.x,o_player.y,o_Doors_all_small);
if (instance_exists(_door) && point_distance(o_player.x,o_player.y,_door.x,_door.y)<=104) {
    draw_text(18,155,"door "+string(floor(_door.x/26))+","+string(floor(_door.y/26))+" -> grid "+string(_door.grid_x)+","+string(_door.grid_y)+" | lock="+string(_door.is_lock)+" a7="+string(_door.alarm[7]));
    draw_text(18,181,"player locks="+string(ds_list_size(o_player.lock_turn))+" a4="+string(o_player.alarm[4])+" | tag="+string(_door.position_tag));
    var _pointed=scr_cursor_get_pointed_instance();
    var _pointed_name=instance_exists(_pointed) ? object_get_name(_pointed.object_index) : "none";
    draw_text(18,207,"hit "+string(_door.bbox_left-_door.x)+","+string(_door.bbox_top-_door.y)+".."+string(_door.bbox_right-_door.x)+","+string(_door.bbox_bottom-_door.y)+" | pointed="+_pointed_name);
}
else if (global.playerGridX >= 39 && global.playerGridX <= 47 && global.playerGridY >= 25 && global.playerGridY <= 40) {
    // Read-only road/map diagnostics for the pilot boundary, never a teleport.
    var _road_data = scr_globaltile_get("Road", global.playerGridX, global.playerGridY);
    draw_text(18,155,"road="+string(_road_data)+" frame="+string(scr_glmap_findRoadTile(global.playerGridX,global.playerGridY)));
    draw_text(18,181,"map="+string(ds_grid_width(global.glmapBatchGridSteppe))+" world="+string(global.worldWidth)+" caravan/cart="+string(global.astarCaravanGrid.width)+"/"+string(global.astarCartGrid.width));
    var _eao_biome=scr_globaltile_get("Biome",global.playerGridX,global.playerGridY);
    draw_text(18,207,_eao_biome=="Sea" ? "biome=Sea coast="+string(scr_globaltile_get("EAO_coast_frame",global.playerGridX,global.playerGridY))+" shore="+string(scr_globaltile_get("ShoreDirection",global.playerGridX,global.playerGridY)) : "biome="+string(_eao_biome)+" road join y="+string(global.EAO_east_road_join_y));
}
// Unplaced architectural asset: an inspection specimen, never a collision or new door.
if (global.EAO_dev_art && room == r_eao_n1_yard) {
    draw_set_alpha(0.88);draw_set_color(c_black);draw_rectangle(12,263,335,568,false);
    draw_set_alpha(1);draw_set_color(c_white);draw_text(20,269,"EXTERIOR SAMPLE / not a doorway");
    draw_sprite(s_eao_hd2d_n1_bellhouse_exterior,0,179,546);
}
draw_set_font(_font);draw_set_color(_color);draw_set_alpha(_alpha);draw_set_halign(_ha);draw_set_valign(_va);
matrix_set(matrix_world,_matrix);
