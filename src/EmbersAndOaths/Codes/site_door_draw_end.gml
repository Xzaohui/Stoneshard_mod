// Draw after the facade, whose foreground depth covers the upper door label.
// Keep native door highlight in Draw 0 and interaction ordering unchanged.
if (scr_cursor_get_pointed_instance()!=id) exit;
var _f=draw_get_font();var _c=draw_get_color();var _a=draw_get_alpha();var _h=draw_get_halign();var _v=draw_get_valign();
draw_set_font(global.f_dmg);draw_set_alpha(1);draw_set_halign(fa_center);draw_set_valign(fa_bottom);
var _label_y=y-38;var _half=string_width(name)*0.5;var _top=_label_y-string_height(name);
if (instance_exists(o_player) && x+_half>=o_player.bbox_left && x-_half<=o_player.bbox_right && _label_y>=o_player.bbox_top && _top<=o_player.bbox_bottom) _label_y=min(_label_y,o_player.bbox_top-5);
draw_set_color(c_black);draw_text(x+1,_label_y+1,name);
draw_set_color(c_yellow);draw_text(x,_label_y,name);
draw_set_font(_f);draw_set_color(_c);draw_set_alpha(_a);draw_set_halign(_h);draw_set_valign(_v);
