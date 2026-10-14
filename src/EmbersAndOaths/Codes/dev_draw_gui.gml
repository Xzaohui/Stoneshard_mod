if (!global.EAO_dev_enabled || !instance_exists(o_player)) exit;
// Player-relative inspection card, in the same visible draw pass as the grid.
var _matrix=matrix_get(matrix_world);
// The native outside-room black mask covers cards drawn beyond room bounds.
var _panel_x=clamp(o_player.x-450,0,max(0,room_width-450));
var _panel_y=clamp(o_player.y-235,0,max(0,room_height-368));
matrix_set(matrix_world,matrix_build(_panel_x,_panel_y,0,0,0,0,0.75,0.75,1));
var _font=draw_get_font();var _color=draw_get_color();var _alpha=draw_get_alpha();var _ha=draw_get_halign();var _va=draw_get_valign();
draw_set_font(global.f_dmg);draw_set_halign(fa_left);draw_set_valign(fa_top);
draw_set_alpha(0.82);draw_set_color(c_black);draw_rectangle(10,45,600,173,false);
draw_set_alpha(1);draw_set_color(c_yellow);
draw_text(18,51,"EAO DEV 0.3.3 | F6 OFF | F8 map teleport");
draw_set_color(c_white);
draw_text(18,77,"F7 reveal="+string(dev_reveal)+"  F9 grid="+string(dev_grid)+"  F10 HD2D="+string(global.EAO_dev_art));
draw_text(18,103,"F11: N1 x3 > N2 x3 | Shift+F11: return");
draw_text(18,129,room_get_name(room)+" | cell "+string(floor(o_player.x/26))+","+string(floor(o_player.y/26))+" | world "+string(global.playerGridX)+","+string(global.playerGridY));
// Unplaced architectural asset: an inspection specimen, never a collision or new door.
if (global.EAO_dev_art && room == r_eao_n1_yard) {
    draw_set_alpha(0.88);draw_set_color(c_black);draw_rectangle(12,185,335,490,false);
    draw_set_alpha(1);draw_set_color(c_white);draw_text(20,191,"EXTERIOR SAMPLE / not a doorway");
    draw_sprite(s_eao_hd2d_n1_bellhouse_exterior,0,179,468);
}
if (global.EAO_dev_art && (room == r_eao_n2_camp || room == r_eao_n2_winch || room == r_eao_n2_side)) {
    draw_set_alpha(0.88);draw_set_color(c_black);draw_rectangle(12,185,335,490,false);
    draw_set_alpha(1);draw_set_color(c_white);draw_text(20,191,"EXTERIOR SAMPLE / not a doorway");
    if (room == r_eao_n2_camp) draw_sprite(s_eao_hd2d_r01_worker_shed,0,179,468);
    else if (room == r_eao_n2_winch) draw_sprite(s_eao_hd2d_r01_winch_shed,0,179,468);
    else draw_sprite(s_eao_hd2d_r01_canal_entry,0,179,468);
}
draw_set_font(_font);draw_set_color(_color);draw_set_alpha(_alpha);draw_set_halign(_ha);draw_set_valign(_va);
matrix_set(matrix_world,_matrix);
