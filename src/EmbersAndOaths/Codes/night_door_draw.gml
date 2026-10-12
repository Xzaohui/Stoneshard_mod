draw_sprite_ext(s_door, 0, x - 13, y, 1, 1, 0, c_white, 1);
event_inherited();
var _font = draw_get_font(); var _color = draw_get_color(); var _alpha = draw_get_alpha();
var _ha = draw_get_halign(); var _va = draw_get_valign();
draw_set_font(global.f_dmg); draw_set_alpha(1); draw_set_halign(fa_center); draw_set_valign(fa_bottom);
draw_set_color(c_black); draw_text(x + 1, y - 37, name);
draw_set_color(c_yellow); draw_text(x, y - 38, name);
draw_set_font(_font); draw_set_color(_color); draw_set_alpha(_alpha); draw_set_halign(_ha); draw_set_valign(_va);
