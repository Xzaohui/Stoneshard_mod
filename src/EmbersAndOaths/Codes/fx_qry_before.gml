// evt_FX_QRY_field_before · engine event 71923 · on_state_read · repeatable
// Registry: reads resolve_N7, writes nothing. Task-open selector; N7 is not
// implemented yet, so the key stays absent and this node stays dormant.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_before", 71923);
eao_fx_qry_before = function() {
    return ds_map_exists(global.characterDataMap, "EAO_resolve_N7") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N7") == "none";
};
