// Native world grids were created before the late, RNG-preserving extension.
// Grow DS grids and rebuild native backing buffers in place. Keep the struct
// identity so any existing native reference still observes the expanded grid.
var _eao_astars=[global.astarCaravanGrid,global.astarCartGrid,global.roadCollisionGrid];
for (var _eao_a=0;_eao_a<3;_eao_a++) {
    var _eao_astar=_eao_astars[_eao_a];
    var _eao_scale=_eao_a<2 ? 3 : 1;
    var _eao_aw=_eao_nw*_eao_scale;var _eao_ah=_eao_h*_eao_scale;
    var _eao_old_aw=_eao_astar.width;
    var _eao_ds_grids=[_eao_astar.grid,_eao_astar.weight_grid,_eao_astar.temp_grid,_eao_astar.came_from_x,_eao_astar.came_from_y,_eao_astar.cost_so_far];
    for(var _eao_d=0;_eao_d<array_length(_eao_ds_grids);_eao_d++) {
        ds_grid_resize(_eao_ds_grids[_eao_d],_eao_aw,_eao_ah);
        ds_grid_set_region(_eao_ds_grids[_eao_d],_eao_old_aw,0,_eao_aw-1,_eao_ah-1,_eao_d==0 ? _eao_astar.default_value : 0);
    }
    var _eao_old_buffer=_eao_astar.buff_grid;
    _eao_astar.width=_eao_aw;_eao_astar.height=_eao_ah;
    _eao_astar.buff_grid_size=_eao_aw*_eao_ah*4;
    _eao_astar.buff_grid=buffer_create(_eao_astar.buff_grid_size,buffer_fixed,4);
    buffer_fill(_eao_astar.buff_grid,0,buffer_u32,_eao_astar.default_value,_eao_astar.buff_grid_size);
    _eao_astar.buff_grid_ptr=buffer_get_address(_eao_astar.buff_grid);
    for(_eao_x=0;_eao_x<_eao_old_aw;_eao_x++) for(_eao_y=0;_eao_y<_eao_ah;_eao_y++)
        astar_add_cell(_eao_astar,_eao_x,_eao_y,astar_get_weight(_eao_astar,_eao_x,_eao_y),false);
    buffer_delete(_eao_old_buffer);
}
for (_eao_x=40;_eao_x<_eao_nw;_eao_x++) for (_eao_y=0;_eao_y<_eao_h;_eao_y++) {
    _eao_p=ds_grid_get(global.terrainGrid,_eao_x,_eao_y);
    var _eao_path_water=ds_map_find_value(_eao_p,"Water");
    var _eao_cost=scr_glmap_hascollision(_eao_x,_eao_y) || _eao_path_water[0]!="None" ? 1000000 : 4;
    astar_add_cell(global.roadCollisionGrid,_eao_x,_eao_y,_eao_cost);
}
// Native User 9 later populates caravan/cart weights, after fog and paper init.
