if (!global.EAO_dev_enabled || !dev_grid || !instance_exists(o_player) || !instance_exists(o_controller)) exit;
if (!variable_instance_exists(o_controller,"newgrid")) exit;
var _old_c=draw_get_color();var _old_a=draw_get_alpha();
var _cx=floor(o_player.x/26);var _cy=floor(o_player.y/26);
for(var _x=max(0,_cx-12);_x<min(floor(room_width/26),_cx+13);_x++) {
    for(var _y=max(0,_cy-10);_y<min(floor(room_height/26),_cy+11);_y++) {
        draw_set_alpha(0.45);draw_set_color(astar_get_cell(o_controller.newgrid,_x,_y)==0 ? c_lime : c_red);
        draw_rectangle(_x*26,_y*26,_x*26+25,_y*26+25,true);
    }
}
draw_set_color(c_yellow);draw_set_alpha(1);draw_circle(o_player.x,o_player.y,5,true);
draw_set_color(_old_c);draw_set_alpha(_old_a);
