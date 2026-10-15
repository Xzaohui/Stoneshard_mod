// evt_FX_QRY_field_early · engine event 71925 · on_state_read · once
// Registry: reads nothing, writes nothing. Order-early: the keeper was
// visited while the linked task was still open (quarry first, post second).
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_early", 71925);
eao_fx_qry_early = function() {
    return ds_map_exists(global.characterDataMap, "EAO_resolve_N7") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N7") == "none" && variable_global_exists("EAO_fx_qry_seen") && global.EAO_fx_qry_seen;
};
