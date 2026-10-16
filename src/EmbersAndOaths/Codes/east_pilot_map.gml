// Runs once, inside the existing 42 -> 50 generated-world extension guard,
// before native cache/fog/paper initialization. No random state or saves touched.
var _eao_batches = [global.glmapBatchGridSnow, global.glmapBatchGridSteppe,
    global.glmapBatchGridSea, global.glmapBatchGridWater, global.glmapBatchGridRoad,
    global.glmapBatchGridTree, global.glmapBatchGridEncounter, global.glmapBatchGridSingleTree,
    global.glmapBatchGridLight, global.glmapBatchGridBorders, global.glmapBatchGridPaperSea,
    global.glmapBatchGridPaperWater, global.glmapBatchGridPaperRoad, global.glmapBatchGridPaperTree,
    global.glmapBatchGridPaperEncounter, global.glmapBatchGridPaperSingleTree];
for (var _eao_b = 0; _eao_b < array_length(_eao_batches); _eao_b++) {
    var _eao_batch = _eao_batches[_eao_b];
    var _eao_bw = ds_grid_width(_eao_batch);
    ds_grid_resize(_eao_batch, _eao_nw, _eao_h);
    if (_eao_bw < _eao_nw) ds_grid_set_region(_eao_batch, _eao_bw, 0, _eao_nw-1, _eao_h-1, -4);
}
// The closed appended columns are sea in the terrain data as well as on the map.
// Use the native full-sea frames, including its separate paper sprite.
for (_eao_x = _eao_ow; _eao_x < _eao_nw; _eao_x++)
    for (_eao_y = 0; _eao_y < _eao_h; _eao_y++)
        scr_glmap_addSprite(_eao_x*52, _eao_y*52, s_glmap_sea_strip16, 4, 15);

// Only the two opened pilot cells get a road. North/south still lead into closed
// border cells, so remove those stale connections. The western connection is
// present only when the original neighboring tile actually has a road.
var _eao_west_road = scr_glmap_hasRoad(_eao_px-1, _eao_py);
for (_eao_i = 0; _eao_i < 2; _eao_i++) {
    _eao_p = ds_grid_get(global.terrainGrid, _eao_px+_eao_i, _eao_py);
    ds_map_set(_eao_p, "Road", ["Road", false, _eao_i == 1 || _eao_west_road, -4]);
    var _eao_layers = [global.glmapBatchGridSteppe, global.glmapBatchGridSea,
        global.glmapBatchGridPaperSea, global.glmapBatchGridWater, global.glmapBatchGridPaperWater,
        global.glmapBatchGridRoad, global.glmapBatchGridPaperRoad, global.glmapBatchGridBorders];
    for (var _eao_l = 0; _eao_l < array_length(_eao_layers); _eao_l++)
        ds_grid_set(_eao_layers[_eao_l], _eao_px+_eao_i, _eao_py, -4);
    scr_glmap_addSprite((_eao_px+_eao_i)*52, _eao_py*52, s_glmap_steppe_strip16, 1, 15);
}
// Native adjacency chooses the end/straight/junction frame and addSprite writes
// the matching discovered and paper batches. Do not paint a disconnected line.
for (_eao_i = (_eao_west_road ? -1 : 0); _eao_i < 2; _eao_i++) {
    var _eao_rx = _eao_px+_eao_i;
    ds_grid_set(global.glmapBatchGridRoad, _eao_rx, _eao_py, -4);
    ds_grid_set(global.glmapBatchGridPaperRoad, _eao_rx, _eao_py, -4);
    var _eao_road_sprite = scr_globaltile_get("Biome", _eao_rx, _eao_py) == "Steppe" ? s_groad_steppe : s_groad;
    scr_glmap_addSprite(_eao_rx*52, _eao_py*52, _eao_road_sprite, 5, scr_glmap_findRoadTile(_eao_rx, _eao_py));
}
