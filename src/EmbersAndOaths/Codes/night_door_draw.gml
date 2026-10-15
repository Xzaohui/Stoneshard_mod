// Respect the native sprite's nonzero origin; keep the visible foot inside
// the interaction cell instead of extending into the next walkable cell.
draw_sprite_ext(s_door, 0, x - sprite_get_width(s_door) * 0.5 + sprite_get_xoffset(s_door), y + 13 - sprite_get_height(s_door) + sprite_get_yoffset(s_door), 1, 1, 0, c_white, 1);
event_inherited();
if (scr_cursor_get_pointed_instance()!=id) exit;
var _font = draw_get_font(); var _color = draw_get_color(); var _alpha = draw_get_alpha();
var _ha = draw_get_halign(); var _va = draw_get_valign();
draw_set_font(global.f_dmg); draw_set_alpha(1); draw_set_halign(fa_center); draw_set_valign(fa_bottom);
var _label_y=y-38;var _half=string_width(name)*0.5;var _top=_label_y-string_height(name);
if (instance_exists(o_player) && x+_half>=o_player.bbox_left && x-_half<=o_player.bbox_right && _label_y>=o_player.bbox_top && _top<=o_player.bbox_bottom) _label_y=min(_label_y,o_player.bbox_top-5);
draw_set_color(c_black); draw_text(x + 1, _label_y + 1, name);
draw_set_color(c_yellow); draw_text(x, _label_y, name);
draw_set_font(_font); draw_set_color(_color); draw_set_alpha(_alpha); draw_set_halign(_ha); draw_set_valign(_va);
