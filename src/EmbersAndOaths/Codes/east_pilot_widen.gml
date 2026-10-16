// EAO GEO-02 east pilot: runs at the start of scr_globalmapCacheInit, i.e. inside
// o_globalmap_controller User 9, after vanilla generation, ResizeGrid and the
// random-sequence verification. No random calls here.
if (variable_global_exists("terrainGrid") && ds_exists(global.terrainGrid, ds_type_grid) && (!variable_global_exists("EAO_east_grid") || global.EAO_east_grid != global.terrainGrid))
{
    global.EAO_east_grid = global.terrainGrid;
    var _eao_ow = ds_grid_width(global.terrainGrid);
    var _eao_h = ds_grid_height(global.terrainGrid);
    var _eao_nw = _eao_ow + 8;
    var _eao_ox = 77;
    var _eao_oy = 22;
    if (variable_global_exists("borderOffsetPoint") && is_struct(global.borderOffsetPoint)) { _eao_ox = global.borderOffsetPoint.x; _eao_oy = global.borderOffsetPoint.y; }
    var _eao_px = 117 - _eao_ox; // (40,37) native steppe
    var _eao_py = 59 - _eao_oy;
    ds_grid_resize(global.terrainGrid, _eao_nw, _eao_h);
    for (var _eao_x = _eao_ow; _eao_x < _eao_nw; _eao_x++)
    {
        for (var _eao_y = 0; _eao_y < _eao_h; _eao_y++)
        {
            var _eao_t = ds_map_create();
            ds_map_add(_eao_t, "x", _eao_x);
            ds_map_add(_eao_t, "y", _eao_y);
            ds_map_add(_eao_t, "Collision", true);
            ds_map_add(_eao_t, "Type", "Wild");
            ds_map_add(_eao_t, "Subtype", "WildFree");
            ds_map_add(_eao_t, "Preset", "N/A");
            ds_map_add(_eao_t, "Forest", 0);
            ds_map_add(_eao_t, "Road", ["None", false, false, -4]);
            ds_map_add(_eao_t, "seed", (_eao_x * 131 + _eao_y * 17) mod 10000);
            ds_map_add(_eao_t, "Trade_Seed", (_eao_x * 37 + _eao_y * 101) mod 10000);
            ds_map_add(_eao_t, "presetSeed", (_eao_x * 53 + _eao_y * 7) mod 10000);
            ds_map_add(_eao_t, "growSeed", (_eao_x * 11 + _eao_y * 29) mod 10000);
            ds_map_add(_eao_t, "mobsSeed", (_eao_x * 19 + _eao_y * 3) mod 10000);
            ds_map_add(_eao_t, "containersSeed", (_eao_x * 23 + _eao_y * 41) mod 10000);
            ds_map_add(_eao_t, "Savezone", false);
            ds_map_add(_eao_t, "DecorationType", "N/A");
            ds_map_add(_eao_t, "Decoration", "N/A");
            ds_map_add(_eao_t, "Biome", "Sea");
            ds_map_add(_eao_t, "MapZone", "None");
            ds_map_add(_eao_t, "Water", ["Sea", false, false]);
            ds_map_add(_eao_t, "room_type", room_get_name(r_sea));
            ds_map_add(_eao_t, "EAO_east", 1);
            ds_grid_set(global.terrainGrid, _eao_x, _eao_y, _eao_t);
        }
    }
    // The two former border columns become interior: keep them closed except the pilot pair.
    for (_eao_x = max(0, _eao_ow - 2); _eao_x < _eao_ow; _eao_x++)
        for (_eao_y = 0; _eao_y < _eao_h; _eao_y++)
        {
            var _eao_c = ds_grid_get(global.terrainGrid, _eao_x, _eao_y);
            if (is_real(_eao_c) && _eao_c >= 0 && ds_exists(_eao_c, ds_type_map)) ds_map_set(_eao_c, "Collision", true);
        }
    for (var _eao_i = 0; _eao_i < 2; _eao_i++)
    {
        var _eao_p = ds_grid_get(global.terrainGrid, _eao_px + _eao_i, _eao_py);
        if (!(is_real(_eao_p) && _eao_p >= 0 && ds_exists(_eao_p, ds_type_map))) continue;
        ds_map_set(_eao_p, "Collision", false);
        if (ds_map_exists(_eao_p, "EAO_east")) { ds_map_set(_eao_p, "Biome", "Steppe"); ds_map_set(_eao_p, "Water", ["None", false, false]); ds_map_set(_eao_p, "room_type", room_get_name(r_steppe)); }
        if (_eao_i == 1) ds_map_set(_eao_p, "room_type", "r_eao_n2_sites");
    }
    global.EAO_east_pilot = [_eao_px, _eao_py, _eao_px + 1, _eao_py];
    global.worldWidth = _eao_nw;
    global.glmapEndX = global.worldWidth - 3;
    global.border_dr = new Vector2(global.worldWidth, global.worldHeight);
    // Old saves: fog/paper strings are column-major (index = x * H + y), so the
    // added columns are exactly a zero suffix.
    if (global.is_load_game)
    {
        var _eao_old = _eao_ow * _eao_h;
        var _eao_pad = string_repeat("0", (_eao_nw - _eao_ow) * _eao_h);
        if (is_string(global.globalmapFogString) && string_length(global.globalmapFogString) == _eao_old) global.globalmapFogString += _eao_pad;
        if (is_string(global.globalmapPaperString) && global.globalmapPaperString != "N/A" && string_length(global.globalmapPaperString) == _eao_old) global.globalmapPaperString += _eao_pad;
    }
    __show_debug_message("EAO east pilot: world " + string(_eao_ow) + "x" + string(_eao_h) + " -> " + string(_eao_nw) + "; pilot " + string(_eao_px) + "," + string(_eao_py));
}
