// evt_FX_QRY_field_late · engine event 71926 · on_state_read · once
// Registry: order-late once linked task is settled (resolve_N7 != none).
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_late", 71926);
eao_fx_qry_late = function() {
    var _r = "none";
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N7")) _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_N7");
    return _r != "none" && variable_global_exists("EAO_fx_qry_seen") && global.EAO_fx_qry_seen;
};
