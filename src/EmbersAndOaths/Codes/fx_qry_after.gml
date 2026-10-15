// evt_FX_QRY_field_after · engine event 71924 · on_state_change · once
// Registry: reads resolve_N7, writes nothing. Task-done selector; a settled
// task only appends the after line, it never rolls back an old conclusion.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_after", 71924);
eao_fx_qry_after = function() {
    return ds_map_exists(global.characterDataMap, "EAO_resolve_N7") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N7") != "none";
};
