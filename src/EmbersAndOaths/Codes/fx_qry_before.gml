// evt_FX_QRY_field_before · engine event 71923 · on_state_read · repeatable
// Registry: reads resolve_N7 (default "none" when absent), writes nothing.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_before", 71923);
eao_fx_qry_before = function() {
    var _r = "none";
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N7")) _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_N7");
    return _r == "none";
};
