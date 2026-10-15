// evt_FX_QRY_field_after · engine event 71924 · on_state_change · once
// Registry: reads resolve_N7 (default "none" when absent), writes nothing.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_after", 71924);
eao_fx_qry_after = function() {
    var _r = "none";
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N7")) _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_N7");
    return _r != "none";
};
