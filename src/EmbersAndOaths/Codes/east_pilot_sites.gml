// EAO GEO-02 east pilot (End Step, before the test-teleport bridge). Active only when
// r_eao_n2_sites is entered as the world tile's own room, never via the N2 door.
if (room == r_eao_n2_sites && variable_global_exists("EAO_east_pilot") && global.playerGridX == global.EAO_east_pilot[2] && global.playerGridY == global.EAO_east_pilot[3])
{
    if (!instance_exists(o_player))
    {
        var _eao_sp = instance_find(o_abstract_player, 0);
        if (instance_exists(_eao_sp)) { _eao_sp.x = 4 * 26 + 13; _eao_sp.y = 19 * 26 + 13; }
    }
    else if (!instance_exists(o_tile_transition))
    {
        for (var _eao_y = 5; _eao_y <= 32; _eao_y++)
        {
            with (instance_create_depth(3 * 26 + 13, _eao_y * 26 + 13, 0, o_tile_transition)) { image_angle = 90; dX = -1; dY = 0; }
            with (instance_create_depth(48 * 26 + 13, _eao_y * 26 + 13, 0, o_tile_transition)) { image_angle = -90; dX = 1; dY = 0; }
        }
        for (var _eao_x = 5; _eao_x <= 46; _eao_x++)
        {
            with (instance_create_depth(_eao_x * 26 + 13, 4 * 26 + 13, 0, o_tile_transition)) { image_angle = 0; dX = 0; dY = -1; }
            with (instance_create_depth(_eao_x * 26 + 13, 33 * 26 + 13, 0, o_tile_transition)) { image_angle = 180; dX = 0; dY = 1; }
        }
    }
}
