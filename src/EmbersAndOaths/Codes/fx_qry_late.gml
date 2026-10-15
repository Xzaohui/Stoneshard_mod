// evt_FX_QRY_field_late · engine event 71926 · on_state_read · once
// Registry: reads nothing, writes nothing. Order-late: the linked task was
// already settled when the keeper was visited (post first, quarry second).
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_late", 71926);
eao_fx_qry_late = function() {
    return ds_map_exists(global.characterDataMap, "EAO_resolve_N7") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N7") != "none" && variable_global_exists("EAO_fx_qry_seen") && global.EAO_fx_qry_seen;
};
