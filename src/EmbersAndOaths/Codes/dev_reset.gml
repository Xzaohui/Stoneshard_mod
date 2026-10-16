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
with (o_globalmapFogRender) {
    if (variable_instance_exists(id,"EAO_dev_visible_owned") && EAO_dev_visible_owned) {
        visible = EAO_dev_visible_before;
        EAO_dev_visible_owned = false;
    }
}
