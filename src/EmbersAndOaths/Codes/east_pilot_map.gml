// Rebuild only the former border/new region, before native cache/fog/paper init.
var _eao_batches=[global.glmapBatchGridSnow,global.glmapBatchGridSteppe,
    global.glmapBatchGridSea,global.glmapBatchGridWater,global.glmapBatchGridRoad,
    global.glmapBatchGridTree,global.glmapBatchGridEncounter,global.glmapBatchGridSingleTree,
    global.glmapBatchGridLight,global.glmapBatchGridBorders,global.glmapBatchGridPaperSea,
    global.glmapBatchGridPaperWater,global.glmapBatchGridPaperRoad,global.glmapBatchGridPaperTree,
    global.glmapBatchGridPaperEncounter,global.glmapBatchGridPaperSingleTree];
for(var _eao_b=0;_eao_b<array_length(_eao_batches);_eao_b++) {
    ds_grid_resize(_eao_batches[_eao_b],_eao_nw,_eao_h);
    ds_grid_set_region(_eao_batches[_eao_b],40,0,_eao_nw-1,_eao_h-1,-4);
}
// Native ground decals can cover the Steppe batch. Keep their original prefix,
// removing only anchors in the former border/new region, never original x<=39.
var _eao_arrays=[global.glmapBatchArrayGround,global.glmapBatchArrayPaperGround,
    global.glmapBatchArrayMountBottom,global.glmapBatchArrayMountTop,
    global.glmapBatchArrayPaperMountBottom,global.glmapBatchArrayPaperMountTop];
for(var _eao_ar=0;_eao_ar<array_length(_eao_arrays);_eao_ar++) {
    var _eao_input=_eao_arrays[_eao_ar];var _eao_prefix=[];
    for(var _eao_g=0;_eao_g<array_length(_eao_input);_eao_g+=6)
        if(_eao_input[_eao_g+2]<40*52)
            array_push(_eao_prefix,_eao_input[_eao_g],_eao_input[_eao_g+1],_eao_input[_eao_g+2],_eao_input[_eao_g+3],_eao_input[_eao_g+4],_eao_input[_eao_g+5]);
    switch(_eao_ar) {
        case 0:global.glmapBatchArrayGround=_eao_prefix;break;
        case 1:global.glmapBatchArrayPaperGround=_eao_prefix;break;
        case 2:global.glmapBatchArrayMountBottom=_eao_prefix;break;
        case 3:global.glmapBatchArrayMountTop=_eao_prefix;break;
        case 4:global.glmapBatchArrayPaperMountBottom=_eao_prefix;break;
        case 5:global.glmapBatchArrayPaperMountTop=_eao_prefix;break;
    }
}

for(_eao_x=40;_eao_x<_eao_nw;_eao_x++) for(_eao_y=0;_eao_y<_eao_h;_eao_y++) {
    _eao_p=ds_grid_get(global.terrainGrid,_eao_x,_eao_y);
    var _eao_biome=ds_map_find_value(_eao_p,"Biome");
    var _eao_steppe_frame=_eao_biome=="Steppe" ? 15 : 0;
    if(_eao_steppe_frame==0 && _eao_biome!="Mount" && _eao_x<_eao_nw-1 && _eao_y>0 && _eao_y<_eao_h-1) {
        // Native strip bits: NE=1, NW=2, SE=4, SW=8. Extend its soft edge
        // across adjacent ground/shore rather than drawing a rectangular patch.
        var _eao_sn=scr_globaltile_get("Biome",_eao_x,_eao_y-1)=="Steppe";
        var _eao_sw=scr_globaltile_get("Biome",_eao_x-1,_eao_y)=="Steppe";
        var _eao_se=scr_globaltile_get("Biome",_eao_x+1,_eao_y)=="Steppe";
        var _eao_ssouth=scr_globaltile_get("Biome",_eao_x,_eao_y+1)=="Steppe";
        _eao_steppe_frame=(_eao_sn+_eao_se+(scr_globaltile_get("Biome",_eao_x+1,_eao_y-1)=="Steppe")>=2 ? 1 : 0)
            +(_eao_sn+_eao_sw+(scr_globaltile_get("Biome",_eao_x-1,_eao_y-1)=="Steppe")>=2 ? 2 : 0)
            +(_eao_ssouth+_eao_se+(scr_globaltile_get("Biome",_eao_x+1,_eao_y+1)=="Steppe")>=2 ? 4 : 0)
            +(_eao_ssouth+_eao_sw+(scr_globaltile_get("Biome",_eao_x-1,_eao_y+1)=="Steppe")>=2 ? 8 : 0);
    }
    if(_eao_steppe_frame>0) scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_glmap_steppe_strip16,1,_eao_steppe_frame);
    if(_eao_biome=="Sea") {
        var _eao_frame=scr_glmap_findShoreTile(_eao_x,_eao_y);
        if(_eao_frame<0) _eao_frame=15;
        if(_eao_x>=48 || _eao_y<2 || _eao_y>=_eao_h-2) _eao_frame=15;
        scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_glmap_sea_strip16,4,_eao_frame);
        var _eao_shore_room=-1;var _eao_shore_class="";
        switch(_eao_frame) {
            case 1: _eao_shore_room=r_SeaShore_SouthEast;_eao_shore_class="SouthEast";break;
            case 2: _eao_shore_room=r_SeaShore_SouthWest;_eao_shore_class="SouthWest";break;
            case 3: _eao_shore_room=r_SeaShore_South01;_eao_shore_class="south";break;
            case 4: _eao_shore_room=r_SeaShore_NorthEast;_eao_shore_class="NorthEast";break;
            case 5: _eao_shore_room=r_SeaShore_East01;_eao_shore_class="east";break;
            case 7: _eao_shore_room=r_SeaShore_SouthEastU;_eao_shore_class="SouthEastOutside";break;
            case 8: _eao_shore_room=r_SeaShore_NorthWest;_eao_shore_class="NorthWest";break;
            case 10: _eao_shore_room=r_SeaShore_West01;_eao_shore_class="west";break;
            case 11: _eao_shore_room=r_SeaShore_SouthWestU;_eao_shore_class="SouthWestOutside";break;
            case 12:
                var _eao_norths=[r_SeaShore_North01,r_SeaShore_North02,r_SeaShore_North03];
                _eao_shore_room=_eao_norths[(_eao_x+_eao_y) mod 3];break;
        }
        if(_eao_shore_room!=-1) {
            ds_map_set(_eao_p,"room_type",room_get_name(_eao_shore_room));
            ds_map_set(_eao_p,"Collision",false);
            if(_eao_shore_class!="") ds_map_set(_eao_p,"ShoreDirection",_eao_shore_class);
        }
        // These are the native Sea-frame north/west connectivity conventions.
        var _eao_wn=_eao_frame!=1 && _eao_frame!=4 && _eao_frame!=8 && _eao_frame!=12;
        var _eao_ww=_eao_frame!=1 && _eao_frame!=8 && _eao_frame!=10;
        ds_map_set(_eao_p,"Water",["Sea",_eao_wn,_eao_ww]);
    }
    var _eao_water=ds_map_find_value(_eao_p,"Water");
    if(_eao_water[0]=="River") {
        // Native river geometry; endpoint variation is deterministic, no RNG call.
        var _eao_river_frame=_eao_y==29 ? 6 : _eao_y==37 ? 9 : 1;
        scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_griver,3,_eao_river_frame);
    }
    if(scr_glmap_hasRoad(_eao_x,_eao_y)) {
        var _eao_rs=_eao_biome=="Steppe" ? s_groad_steppe : s_groad;
        scr_glmap_addSprite(_eao_x*52,_eao_y*52,_eao_rs,5,scr_glmap_findRoadTile(_eao_x,_eao_y));
        if(_eao_water[0]=="River") scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_gbridge,5,3);
    }
    if(_eao_biome=="Pine") {
        var _eao_tree_frame=3+floor(ds_map_find_value(_eao_p,"seed")) mod 3;
        scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_gptree_shadow,7,_eao_tree_frame);
        scr_glmap_addSprite(_eao_x*52,_eao_y*52,s_gptree,7,_eao_tree_frame);
    }
    if(_eao_biome=="Mount") {
        // Use existing cut native ridge pixels; no new commercial pixels in SML.
        var _eao_nmount=_eao_y>0 && scr_globaltile_get("Biome",_eao_x,_eao_y-1)=="Mount";
        var _eao_smount=_eao_y<_eao_h-1 && scr_globaltile_get("Biome",_eao_x,_eao_y+1)=="Mount";
        var _eao_mv=floor(ds_map_find_value(_eao_p,"presetSeed")) mod 2;
        var _eao_mframe=!_eao_nmount ? _eao_mv : !_eao_smount ? 13+_eao_mv : 5+_eao_mv;
        array_push(global.glmapBatchArrayMountBottom,s_gmount01_4_strip16,_eao_mframe,_eao_x*52,_eao_y*52,1,1);
        var _eao_pmframe=_eao_mframe<2 ? _eao_mframe : _eao_mframe<7 ? _eao_mframe-3 : _eao_mframe-9;
        array_push(global.glmapBatchArrayPaperMountBottom,s_eao_east_ridge_paper,_eao_pmframe,_eao_x*52,_eao_y*52,1,1);
    }
}
// The only original road drawing touched is an actual adjoining native road.
// Its map data and seed remain unchanged; the new east neighbor adds the branch.
if(_eao_join_y!=-1) {
    ds_grid_set(global.glmapBatchGridRoad,39,_eao_join_y,-4);
    ds_grid_set(global.glmapBatchGridPaperRoad,39,_eao_join_y,-4);
    var _eao_wrs=scr_globaltile_get("Biome",39,_eao_join_y)=="Steppe" ? s_groad_steppe : s_groad;
    scr_glmap_addSprite(39*52,_eao_join_y*52,_eao_wrs,5,scr_glmap_findRoadTile(39,_eao_join_y));
}
