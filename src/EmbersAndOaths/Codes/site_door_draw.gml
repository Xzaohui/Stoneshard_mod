// Facade supplies the permanent opening; inherit native highlight/hit testing.
event_inherited();
var _f=draw_get_font();var _c=draw_get_color();var _h=draw_get_halign();var _v=draw_get_valign();
draw_set_font(global.f_dmg);draw_set_halign(fa_center);draw_set_valign(fa_top);
draw_set_color(c_black);draw_text(x+1,y+14,name);
draw_set_color(c_yellow);draw_text(x,y+13,name);
draw_set_font(_f);draw_set_color(_c);draw_set_halign(_h);draw_set_valign(_v);
