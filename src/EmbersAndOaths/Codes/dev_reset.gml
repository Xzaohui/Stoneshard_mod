if (dev_fog_owned && variable_global_exists("fog")) global.fog = dev_fog_before;
dev_fog_owned = false;
dev_reveal = false;
dev_grid = false;
global.EAO_dev_enabled = false;
// Cancel an uncommitted developer request, never a transition already saving.
if (variable_global_exists("characterDataMap") && ds_exists(global.characterDataMap,ds_type_map)) {
    ds_map_set(global.characterDataMap,"EAO_test_map_pending",0);
    ds_map_set(global.characterDataMap,"EAO_test_teleport_enabled",0);
}
global.EAO_dev_return_keep = false;
global.EAO_dev_warp_keep = false;
dev_coord_submitting=false;
dev_coord_text="";
dev_coord_error="";
dev_coord_queued=false;
with(o_eao_dev_coordinates) instance_destroy();
with (o_globalmapInteractiveNormal) {
    if (variable_instance_exists(id,"EAO_dev_map_owned") && EAO_dev_map_owned) {
        // A later owner must not be overwritten on reset.
        if (guiInteractiveEvent==10) {
            if (!EAO_dev_map_left_before) {
                var _left_index=ds_list_find_index(guiInteractiveStatesList,2);
                if (_left_index!=-1) ds_list_delete(guiInteractiveStatesList,_left_index);
                guiInteractiveStatesCount=ds_list_size(guiInteractiveStatesList);
            }
            scr_guiInteractiveEventUpdate(id,15);
        }
        EAO_dev_map_owned=false;
    }
}
with (o_globalmapFogRender) {
    if (variable_instance_exists(id,"EAO_dev_visible_owned") && EAO_dev_visible_owned) {
        visible = EAO_dev_visible_before;
        EAO_dev_visible_owned = false;
    }
}
