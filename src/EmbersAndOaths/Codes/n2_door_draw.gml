// HD2D doorway artwork is stamped by the floor, below the player. This object
// keeps the aligned hit mask, native highlight, mouse events and transition.
if (variable_global_exists("EAO_dev_enabled") && global.EAO_dev_enabled && !global.EAO_dev_art) {
    draw_sprite_ext(s_door,0,x-sprite_get_width(s_door)*0.5+sprite_get_xoffset(s_door),y+13-sprite_get_height(s_door)+sprite_get_yoffset(s_door),1,1,0,c_white,1);
}
// Native Create selects the sprlight path with the anchor sprite. Select the
// native shader path for this draw only so it outlines the floor artwork.
// Restore both fields before any simulation; the native highlight guards stay.
var _anchor_sprite=sprite_index;
var _anchor_shader=shaderHighlight;
if (!variable_global_exists("EAO_dev_enabled") || !global.EAO_dev_enabled || global.EAO_dev_art) {
    sprite_index=s_eao_hd2d_r01_doorway_open;
    shaderHighlight=true;
}
event_inherited();
sprite_index=_anchor_sprite;
shaderHighlight=_anchor_shader;
if (scr_cursor_get_pointed_instance()==id) {
    var _font=draw_get_font();var _color=draw_get_color();var _alpha=draw_get_alpha();
    var _ha=draw_get_halign();var _va=draw_get_valign();
    draw_set_font(global.f_dmg);draw_set_alpha(1);draw_set_halign(fa_center);draw_set_valign(fa_bottom);
    var _label_y=y-38;var _half=string_width(name)*0.5;var _top=_label_y-string_height(name);
    if (instance_exists(o_player) && x+_half>=o_player.bbox_left && x-_half<=o_player.bbox_right && _label_y>=o_player.bbox_top && _top<=o_player.bbox_bottom) _label_y=min(_label_y,o_player.bbox_top-5);
    draw_set_color(c_black);draw_text(x+1,_label_y+1,name);
    draw_set_color(c_yellow);draw_text(x,_label_y,name);
    draw_set_font(_font);draw_set_color(_color);draw_set_alpha(_alpha);draw_set_halign(_ha);draw_set_valign(_va);
}
