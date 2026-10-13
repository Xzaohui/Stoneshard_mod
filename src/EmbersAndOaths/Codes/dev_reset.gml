if (dev_fog_owned && variable_global_exists("fog")) global.fog = dev_fog_before;
dev_fog_owned = false;
dev_reveal = false;
dev_grid = false;
global.EAO_dev_enabled = false;
with (o_globalmapFogRender) {
    if (variable_instance_exists(id,"EAO_dev_visible_owned") && EAO_dev_visible_owned) {
        visible = EAO_dev_visible_before;
        EAO_dev_visible_owned = false;
    }
}
