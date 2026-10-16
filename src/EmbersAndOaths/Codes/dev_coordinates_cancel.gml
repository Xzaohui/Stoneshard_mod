// Cancel only this editor's uncommitted request, not another source/character
// or a changer which already started its native save lifecycle.
if(eao_coord_queued && global.characterDataMap==eao_coord_character && ds_exists(global.characterDataMap,ds_type_map) && !instance_exists(o_smoothRoomChanger)) {
    ds_map_set(global.characterDataMap,"EAO_test_map_pending",0);
}
eao_coord_queued=false;
eao_coord_closing=true;
